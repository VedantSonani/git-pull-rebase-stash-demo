# Scenario 03 — Standard `git pull` Conflict

## Objective

Demonstrate what happens when `git pull` encounters conflicting changes between the local branch and the remote branch.

This scenario covers:

* Diverged history
* `git pull`
* Merge conflict
* Conflict markers
* `git status`
* Resolving a merge conflict
* `git add`
* `git commit`

For a normal `git pull` conflict, the underlying operation is a merge. Therefore, after resolving the conflict, the merge is completed with `git commit`.

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

We want the local and remote branches to initially point to the same commit:

```text
A --- B --- C
          ↑
       local
       remote
```

`C` is the last common commit.

---

# Step 1 — Create the Remote Change

Go to the GitHub repository.

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

Commit the change directly on GitHub.

Use a commit message such as:

```text
Update application version remotely
```

The remote branch is now:

```text
A --- B --- C --- D
                    ↑
                  remote
```

Your local branch is still:

```text
A --- B --- C
            ↑
          local
```

---

# Step 2 — Create a Conflicting Local Change

Do **not** pull the remote change yet.

In your local repository, open:

```text
app/app.py
```

Change the same line:

```python
VERSION = "1.0"
```

to:

```python
VERSION = "3.0"
```

Now your local working tree contains:

```python
VERSION = "3.0"
```

while GitHub contains:

```python
VERSION = "2.0"
```

---

# Step 3 — Commit the Local Change

Check the change:

```bash
git status
```

Stage it:

```bash
git add app/app.py
```

Commit it:

```bash
git commit -m "Update application version locally"
```

Now the histories have diverged:

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

---

# Step 4 — Verify the Divergence

Run:

```bash
git fetch
```

Then:

```bash
git log --oneline --graph --decorate --all
```

Conceptually, you should have:

```text
        D   ← origin/main
       /
A --- B --- C
           \
            E   ← HEAD -> main
```

The important point is that both branches contain a commit that the other branch does not have.

---

# Step 5 — Run `git pull`

Run:

```bash
git pull
```

Git effectively performs:

```text
git fetch
    ↓
git merge
```

Because both local and remote branches contain unique changes, Git attempts to merge them.

Since both commits modified the same line in `app/app.py`, Git cannot automatically determine which version should be kept.

You should receive a conflict similar to:

```text
Auto-merging app/app.py
CONFLICT (content): Merge conflict in app/app.py
Automatic merge failed; fix conflicts and then commit the result.
```

---

# Step 6 — Check the Repository Status

Run:

```bash
git status
```

You should see something similar to:

```text
You have unmerged paths.

Unmerged paths:
    both modified:   app/app.py
```

Git is now in the middle of a merge.

---

# Step 7 — Inspect the Conflict

Open:

```text
app/app.py
```

Git will insert conflict markers.

The file will contain something similar to:

```python
<<<<<<< HEAD
VERSION = "3.0"
=======
VERSION = "2.0"
>>>>>>> origin/main
```

The markers mean:

```text
<<<<<<< HEAD
Your local version
=======
Remote version
>>>>>>> origin/main
```

The exact marker text can vary depending on the branch configuration.

---

# Step 8 — Resolve the Conflict

For this demo, choose:

```python
VERSION = "2.0"
```

Remove all conflict markers.

The final section of `app/app.py` should simply contain:

```python
APP_NAME = "Git Demo App"
VERSION = "2.0"
ENVIRONMENT = "development"
```

There should be no:

```text
<<<<<<<
=======
>>>>>>>
```

left in the file.

---

# Step 9 — Stage the Resolution

Run:

```bash
git add app/app.py
```

Then:

```bash
git status
```

Git should now indicate that the conflict has been resolved and that the merge is ready to be committed.

---

# Step 10 — Complete the Merge

Run:

```bash
git commit
```

Git will normally provide a merge commit message.

You can also use:

```bash
git commit -m "Merge remote changes and resolve version conflict"
```

The merge is now complete.

---

# Step 11 — Inspect the History

Run:

```bash
git log --oneline --graph --decorate --all
```

You should now have a structure similar to:

```text
*   M Merge remote changes and resolve version conflict
|\
| * D Update application version remotely
* | E Update application version locally
|/
* C
```

The important relationship is:

```text
C = common ancestor
D = remote commit
E = local commit
M = merge commit
```

---

# Step 12 — Verify the Working Tree

Run:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

The conflict has been completely resolved.

---

# What Happened?

Before the pull:

```text
        D   ← remote
       /
A --- B --- C
           \
            E   ← local
```

Both branches had moved forward independently from `C`.

When you ran:

```bash
git pull
```

Git performed:

```text
git fetch
     ↓
git merge
```

The merge encountered a conflict because:

```text
Remote:
VERSION = "2.0"

Local:
VERSION = "3.0"
```

Git could not automatically decide which value should be used.

After resolving the conflict:

```text
git add app/app.py
git commit
```

Git created a merge commit.

---

# Important Difference From Rebase

For this scenario:

```bash
git pull
```

caused a **merge conflict**.

After resolving:

```bash
git add app/app.py
git commit
```

Do **not** use:

```bash
git rebase --continue
```

That command belongs to a conflict occurring during a rebase.

The guide explicitly distinguishes these two conflict-resolution flows.

---

# Conflict Resolution Flow

```text
git pull
    ↓
fetch
    ↓
merge
    ↓
CONFLICT
    ↓
git status
    ↓
open conflicting file
    ↓
resolve conflict markers
    ↓
git add <file>
    ↓
git commit
    ↓
merge completed
```

---

# Test Case

| Test | Action                          | Expected Result               |
| ---- | ------------------------------- | ----------------------------- |
| 1    | Create remote change            | GitHub moves ahead            |
| 2    | Create conflicting local change | Local branch diverges         |
| 3    | `git fetch`                     | Remote information downloaded |
| 4    | `git pull`                      | Merge starts                  |
| 5    | Same lines changed              | Merge conflict                |
| 6    | `git status`                    | Shows unmerged file           |
| 7    | Resolve `app/app.py`            | Conflict markers removed      |
| 8    | `git add app/app.py`            | Conflict marked resolved      |
| 9    | `git commit`                    | Merge completed               |
| 10   | `git log --graph`               | Merge commit visible          |

---

# Key Learning

A standard:

```bash
git pull
```

is effectively:

```text
git fetch + git merge
```

When local and remote changes overlap, the merge may stop for manual conflict resolution.

The resolution flow is:

```bash
git add <resolved-file>
git commit
```

This is different from a rebase conflict, where the continuation command is:

```bash
git rebase --continue
```