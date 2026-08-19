# Scenario 06 — Rebase Conflict

## Objective

Demonstrate what happens when `git pull --rebase` encounters conflicting changes while replaying a local commit.

This scenario covers:

* Diverged history
* `git pull --rebase`
* Rebase conflict
* Conflict markers
* `git status`
* `git add`
* `git rebase --continue`
* Difference between merge and rebase conflict resolution

During a rebase conflict, the conflict is resolved and the rebase is continued with `git rebase --continue`, not with `git commit`.

---

# Starting State

Make sure the working tree is clean:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

For this scenario, start with local and remote pointing to the same commit:

```text
A --- B --- C
          ↑
     local + remote
```

`C` is the common ancestor.

---

# Step 1 — Create a Remote Change

Go to GitHub.

Open:

```text
app/app.py
```

Find:

```python
VERSION = "1.0"
```

Change it to:

```python
VERSION = "2.0"
```

Commit directly on GitHub.

Example commit message:

```text
Update version remotely
```

The remote branch is now:

```text
A --- B --- C --- D
                    ↑
                  remote
```

Your local branch still points to `C`:

```text
A --- B --- C
            ↑
          local
```

---

# Step 2 — Create a Conflicting Local Commit

Do **not** pull the remote change yet.

In your local repository, open:

```text
app/app.py
```

Change the same original line:

```python
VERSION = "1.0"
```

to:

```python
VERSION = "3.0"
```

Now stage and commit:

```bash
git add app/app.py
git commit -m "Update version locally"
```

The histories have diverged:

```text
        D   ← remote
       /
A --- B --- C
           \
            E   ← local
```

Where:

```text
C = common ancestor
D = remote commit
E = local commit
```

The important detail is that both `D` and `E` modify the same line.

---

# Step 3 — Verify the Divergence

Run:

```bash
git fetch
```

Then:

```bash
git log --oneline --graph --decorate --all
```

You should conceptually have:

```text
        D   ← origin/main
       /
A --- B --- C
           \
            E   ← HEAD -> main
```

---

# Step 4 — Run `git pull --rebase`

Run:

```bash
git pull --rebase
```

Git starts the rebase.

Conceptually, it performs:

```text
fetch
  ↓
temporarily remove local commit E
  ↓
move local branch to D
  ↓
replay E on top of D
```

The temporary state is approximately:

```text
A --- B --- C --- D
                    ↑
                  local
```

Git then attempts to replay `E`.

---

# Step 5 — Rebase Encounters the Conflict

The local commit `E` contains:

```python
VERSION = "3.0"
```

The new base `D` contains:

```python
VERSION = "2.0"
```

Git cannot automatically determine which version should be used.

You should receive an error similar to:

```text
CONFLICT (content): Merge conflict in app/app.py
error: could not apply <commit>... Update version locally
```

Git pauses the rebase.

---

# Step 6 — Check the Repository

Run:

```bash
git status
```

Git should indicate that a rebase is currently in progress.

You should also see that:

```text
app/app.py
```

contains an unresolved conflict.

---

# Step 7 — Inspect the Conflict

Open:

```text
app/app.py
```

You should see conflict markers similar to:

```python
<<<<<<< HEAD
VERSION = "2.0"
=======
VERSION = "3.0"
>>>>>>> <local-commit>
```

The meaning is:

```text
<<<<<<< HEAD
Version from the current rebased base
=======
Version from the local commit being replayed
>>>>>>> local commit
```

The exact commit identifier in the final marker will vary.

---

# Step 8 — Resolve the Conflict

For this demo, choose:

```python
VERSION = "3.0"
```

Remove all conflict markers.

The file should contain:

```python
APP_NAME = "Git Demo App"
VERSION = "3.0"
ENVIRONMENT = "development"
```

There should be no:

```text
<<<<<<<
=======
>>>>>>>
```

remaining in the file.

---

# Step 9 — Stage the Resolution

Run:

```bash
git add app/app.py
```

Check:

```bash
git status
```

Git should now recognize that the conflict has been resolved.

However, the rebase is **not finished yet**.

---

# Step 10 — Continue the Rebase

Run:

```bash
git rebase --continue
```

This tells Git:

> The conflict for the current commit has been resolved. Continue replaying the rebase.

Git will complete the replay if there are no additional conflicts.

---

# Step 11 — If Git Opens an Editor

Depending on your Git configuration, `git rebase --continue` may open an editor asking you to confirm the commit message.

Keep the existing commit message:

```text
Update version locally
```

Save and close the editor.

The rebase should then continue.

---

# Step 12 — Verify the Result

Run:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

Then:

```bash
git log --oneline --graph --decorate --all
```

You should now have a linear history:

```text
* E'  ← local
* D   ← origin/main
* C
* B
* A
```

The original local commit `E` has been replayed as a new commit `E'`.

---

# Before the Rebase

```text
        D   ← remote
       /
A --- B --- C
           \
            E   ← local
```

`C` is the common ancestor.

---

# During the Rebase

Git temporarily removes `E`:

```text
A --- B --- C --- D
                    ↑
              current base
```

Then Git attempts to replay `E`.

Because `D` and `E` modified the same line:

```text
CONFLICT
```

---

# After Resolving the Conflict

Git creates the replayed commit:

```text
A --- B --- C --- D --- E'
```

The history is now linear.

---

# Why Is It `E'` Instead of `E`?

The original commit was:

```text
C --- E
```

The rebased commit is:

```text
D --- E'
```

Because its parent changed from `C` to `D`, Git creates a new commit.

The changes introduced by the commit can be the same, but the commit itself has a different identity.

---

# Critical Difference From a Merge Conflict

This scenario is important because the commands after resolving the conflict are different.

## Merge Conflict

Created by:

```bash
git pull
```

Resolution:

```bash
git add app/app.py
git commit
```

The guide identifies this as a merge operation and therefore uses a normal commit to complete it.

---

## Rebase Conflict

Created by:

```bash
git pull --rebase
```

Resolution:

```bash
git add app/app.py
git rebase --continue
```

Do **not** run:

```bash
git commit
```

during the rebase.

The reference guide explicitly states that `git rebase --continue` must be used to continue the replay.

---

# What Happens If There Are Multiple Local Commits?

Rebase can encounter multiple conflicts because local commits are replayed **one at a time**.

For example:

```text
        D   ← remote
       /
A --- B --- C
           \
            E --- F   ← local
```

Git attempts:

```text
D
↓
replay E
↓
resolve conflict
↓
git rebase --continue
↓
replay F
↓
possibly another conflict
↓
resolve
↓
git rebase --continue
```

Eventually:

```text
A --- B --- C --- D --- E' --- F'
```

This is one of the important differences between merge and rebase conflict handling. The guide notes that rebase conflicts are resolved one commit at a time as each local commit is replayed.

---

# Useful Commands During the Conflict

Check the current state:

```bash
git status
```

See the conflicting files:

```bash
git diff
```

Stage the resolved file:

```bash
git add app/app.py
```

Continue:

```bash
git rebase --continue
```

Abort everything:

```bash
git rebase --abort
```

View the history:

```bash
git log --oneline --graph --decorate --all
```

---

# Important Rule

While a rebase is in progress:

```text
Resolve conflict
      ↓
git add
      ↓
git rebase --continue
```

Do not manually create the commit with:

```bash
git commit
```

Git is responsible for creating the replayed commit.

---

# Test Case

| Test | Action                          | Expected Result             |
| ---- | ------------------------------- | --------------------------- |
| 1    | Create remote change            | Remote moves ahead          |
| 2    | Create conflicting local commit | Local moves ahead           |
| 3    | `git fetch`                     | Remote commit visible       |
| 4    | `git pull --rebase`             | Rebase starts               |
| 5    | Same line modified              | Rebase conflict             |
| 6    | `git status`                    | Rebase shown as in progress |
| 7    | Inspect `app.py`                | Conflict markers visible    |
| 8    | Resolve conflict                | Final content selected      |
| 9    | `git add app/app.py`            | Conflict staged             |
| 10   | `git rebase --continue`         | Local commit replayed       |
| 11   | `git log --graph`               | Linear history              |
| 12   | `git status`                    | Working tree clean          |

---

# Key Learning

A rebase conflict occurs while Git is **replaying a local commit**.

The workflow is:

```text
git pull --rebase
       ↓
fetch
       ↓
rebase
       ↓
replay local commit
       ↓
CONFLICT
       ↓
resolve file
       ↓
git add
       ↓
git rebase --continue
       ↓
replay complete
```

The resulting history is:

```text
A --- B --- C --- D --- E'
```

rather than a merge history containing an additional merge commit.