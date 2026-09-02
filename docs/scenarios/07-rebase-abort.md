# Scenario 07 — Abort a Rebase Conflict

## Objective

Demonstrate how to cancel an in-progress rebase when a conflict occurs.

This scenario covers:

* `git pull --rebase`
* Rebase conflict
* `git status`
* `git rebase --abort`
* Returning to the state before the rebase
* Difference between `git rebase --abort` and `git merge --abort`

The reference guide states that `git rebase --abort` cancels an in-progress rebase and restores the branch and working directory to the state they had before the rebase started.

---

# Starting State

Make sure the repository is clean:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

We want local and remote to initially point to the same commit:

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

Your local branch remains:

```text
A --- B --- C
            ↑
          local
```

---

# Step 2 — Create a Conflicting Local Commit

Do not pull the remote change yet.

In your local repository, open:

```text
app/app.py
```

Change:

```python
VERSION = "1.0"
```

to:

```python
VERSION = "3.0"
```

Stage and commit:

```bash
git add app/app.py
git commit -m "Update version locally"
```

The histories have now diverged:

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

Both `D` and `E` modify the same line.

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

You should have a structure similar to:

```text
        D   ← origin/main
       /
A --- B --- C
           \
            E   ← HEAD -> main
```

---

# Step 4 — Start the Rebase

Run:

```bash
git pull --rebase
```

Git begins the rebase.

Conceptually:

```text
fetch
  ↓
temporarily remove E
  ↓
move local branch to D
  ↓
replay E
```

Git attempts to apply the changes from `E` on top of `D`.

Because both commits modify the same line, a conflict occurs.

You should see something similar to:

```text
CONFLICT (content): Merge conflict in app/app.py
error: could not apply <commit>... Update version locally
```

---

# Step 5 — Check the Rebase State

Run:

```bash
git status
```

Git should indicate that:

```text
rebase in progress
```

and that:

```text
app/app.py
```

has an unresolved conflict.

At this point, **do not resolve the conflict**.

The purpose of this scenario is to cancel the rebase.

---

# Step 6 — Inspect the Conflict

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

The repository is currently in an incomplete rebase state.

---

# Step 7 — Abort the Rebase

Run:

```bash
git rebase --abort
```

Git cancels the entire rebase operation.

---

# Step 8 — Check the Repository

Run:

```bash
git status
```

The rebase should no longer be in progress.

The working tree should be clean:

```text
On branch main
nothing to commit, working tree clean
```

---

# Step 9 — Verify the Local Commit

Run:

```bash
git log --oneline --decorate -5
```

Your original local commit should still exist:

```text
E Update version locally
C ...
B ...
A ...
```

The local commit has **not** been deleted.

The rebase was simply cancelled.

---

# Step 10 — Verify the Remote Commit

Run:

```bash
git fetch
```

Then:

```bash
git log --oneline --graph --decorate --all
```

You should again have the diverged state:

```text
        D   ← origin/main
       /
A --- B --- C
           \
            E   ← main
```

No rebased commit has been created.

No merge commit has been created.

---

# What Happened?

Before starting the rebase:

```text
        D   ← remote
       /
A --- B --- C
           \
            E   ← local
```

Then:

```bash
git pull --rebase
```

Git attempted:

```text
fetch
  ↓
remove E temporarily
  ↓
move to D
  ↓
replay E
  ↓
CONFLICT
```

At this point:

```text
rebase in progress
```

Instead of resolving the conflict:

```bash
git add app/app.py
git rebase --continue
```

we cancelled the entire operation:

```bash
git rebase --abort
```

The repository returns to:

```text
        D   ← remote
       /
A --- B --- C
           \
            E   ← local
```

---

# Why Use `git rebase --abort`?

Use it when:

* The rebase conflict is too complicated.
* You want to restart the operation.
* You started the rebase accidentally.
* You do not want to continue replaying the local commits.
* You want to return to the state before the rebase started.

The reference guide specifically describes `git rebase --abort` as restoring the branch and working directory to their state before the rebase began.

---

# `git merge --abort` vs `git rebase --abort`

The command depends on what Git is currently doing.

## Merge in progress

If you ran:

```bash
git pull
```

and it produced a merge conflict:

```bash
git merge --abort
```

Use:

```text
git merge --abort
```

---

## Rebase in progress

If you ran:

```bash
git pull --rebase
```

and it produced a rebase conflict:

```bash
git rebase --abort
```

Use:

```text
git rebase --abort
```

The two commands cancel different operations.

---

# Visual Comparison

### Merge abort

```text
git pull
   ↓
merge
   ↓
CONFLICT
   ↓
git merge --abort
   ↓
before merge
```

### Rebase abort

```text
git pull --rebase
   ↓
rebase
   ↓
CONFLICT
   ↓
git rebase --abort
   ↓
before rebase
```

---

# Important Demonstration

At the conflict, first run:

```bash
git status
```

Show that Git reports a rebase in progress.

Then open:

```text
app/app.py
```

and show the conflict markers.

Now run:

```bash
git rebase --abort
```

Then immediately run:

```bash
git status
```

and:

```bash
git log --oneline --graph --decorate --all
```

This makes it obvious that the rebase was completely cancelled.

---

# Test Case

| Test | Action                          | Expected Result              |
| ---- | ------------------------------- | ---------------------------- |
| 1    | Create remote change            | Remote moves ahead           |
| 2    | Create conflicting local commit | Local moves ahead            |
| 3    | `git fetch`                     | Remote commit visible        |
| 4    | `git pull --rebase`             | Rebase starts                |
| 5    | Same line changed               | Rebase conflict              |
| 6    | `git status`                    | Rebase in progress           |
| 7    | Inspect `app.py`                | Conflict markers visible     |
| 8    | `git rebase --abort`            | Rebase cancelled             |
| 9    | `git status`                    | No rebase in progress        |
| 10   | `git log --graph`               | Original divergence restored |
| 11   | Check local commit              | Local commit still exists    |

---

# Key Learning

A rebase can be cancelled safely with:

```bash
git rebase --abort
```

The mental model is:

```text
git pull --rebase
       ↓
    CONFLICT
       ↓
git rebase --abort
       ↓
return to pre-rebase state
```

The original local commit remains intact.

The remote commit remains intact.

The incomplete rebase is removed.