# Scenario 04 — Abort a Conflicted `git pull`

## Objective

Demonstrate how to safely cancel an in-progress merge after `git pull` produces a conflict.

This scenario covers:

* `git pull`
* Merge conflict
* `git status`
* `git merge --abort`
* Returning to the state before the merge
* Difference between merge abort and rebase abort

The reference guide specifically states that `git merge --abort` cancels a conflicted merge caused by `git pull` and restores the repository to its state immediately before the pull.

---

# Starting State

The working tree must be clean:

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

Change:

```python
VERSION = "1.0"
```

to:

```python
VERSION = "2.0"
```

Commit directly on GitHub:

```text
Update version remotely
```

The remote is now:

```text
A --- B --- C --- D
                    ↑
                  remote
```

Your local repository is still:

```text
A --- B --- C
            ↑
          local
```

---

# Step 2 — Create a Conflicting Local Commit

Do not pull yet.

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
A --- B --- C --- D    <- remote
           \
            E          <- local
```

Where:

```text
C = common ancestor
D = remote commit
E = local commit
```

---

# Step 3 — Start the Merge

Run:

```bash
git pull
```

Git performs:

```text
git fetch
    ↓
git merge
```

Because both sides modified the same line, Git should produce a conflict:

```text
Auto-merging app/app.py
CONFLICT (content): Merge conflict in app/app.py
Automatic merge failed; fix conflicts and then commit the result.
```

The repository is now in an **in-progress merge**.

---

# Step 4 — Check the Repository

Run:

```bash
git status
```

You should see information indicating that a merge is in progress and that `app/app.py` has conflicts.

The file should contain conflict markers similar to:

```python
<<<<<<< HEAD
VERSION = "3.0"
=======
VERSION = "2.0"
>>>>>>> origin/main
```

At this point, **do not resolve the conflict**.

The purpose of this scenario is to demonstrate how to abandon the merge.

---

# Step 5 — Inspect the State Before Aborting

Run:

```bash
git log --oneline --graph --decorate --all
```

Also run:

```bash
git status
```

Git is currently in a partially merged state.

The working file contains conflict markers:

```text
<<<<<<<
=======
>>>>>>>
```

This is not the state you want to leave the repository in.

---

# Step 6 — Abort the Merge

Run:

```bash
git merge --abort
```

Git cancels the in-progress merge.

You should no longer have conflict markers in `app/app.py`.

---

# Step 7 — Check the Repository

Run:

```bash
git status
```

The repository should no longer report an active merge.

You should have your original local branch state back:

```text
A --- B --- C --- E    <- local
           \
            D          <- remote
```

The exact orientation shown by `git log --graph` may differ, but the important point is:

```text
The merge attempt has been cancelled.
Your local commit E still exists.
The remote commit D still exists.
No merge commit was created.
```

---

# Step 8 — Verify Your Local Commit

Run:

```bash
git log --oneline --decorate -5
```

Your local commit should still be present:

```text
E Update version locally
C ...
B ...
A ...
```

The important thing is that `git merge --abort` did **not** delete your existing local commit.

It only cancelled the in-progress merge.

---

# Step 9 — Verify the Remote Commit

Run:

```bash
git fetch
```

Then:

```bash
git log --oneline --graph --decorate --all
```

You should still have two branches of history:

```text
        D  <- origin/main
       /
A --- B --- C
           \
            E  <- main
```

Again:

* `C` = common ancestor
* `D` = remote commit
* `E` = local commit

The merge commit does not exist because the merge was aborted.

---

# What Happened?

Before `git pull`:

```text
A --- B --- C --- D    <- remote
           \
            E          <- local
```

Git attempted:

```text
git pull
    ↓
git fetch
    ↓
git merge
    ↓
CONFLICT
```

The repository entered an in-progress merge.

Instead of resolving it:

```bash
git add app/app.py
git commit
```

we cancelled it:

```bash
git merge --abort
```

The result:

```text
A --- B --- C --- D    <- remote
           \
            E          <- local
```

The diverged history remains, but the incomplete merge is gone.

---

# Why Use `git merge --abort`?

Use it when:

* You started a merge accidentally.
* The conflict is too complicated to resolve immediately.
* You want to restart the operation.
* You want to return to the state before the merge began.

The reference guide describes this as returning the branch, working directory, and index to the state immediately before the failed pull.

---

# `git merge --abort` vs `git rebase --abort`

These commands are for different operations.

### During `git pull`

```bash
git pull
```

If it produces a merge conflict:

```bash
git merge --abort
```

### During `git pull --rebase`

```bash
git pull --rebase
```

If it produces a rebase conflict:

```bash
git rebase --abort
```

The guide explicitly warns that these are not interchangeable.

---

# Important Demonstration

At the conflict, show:

```bash
git status
```

Then show the conflict markers in:

```text
app/app.py
```

Then run:

```bash
git merge --abort
```

Immediately run:

```bash
git status
```

and:

```bash
git log --oneline --graph --decorate --all
```

This makes the effect of `git merge --abort` visible.

---

# Test Case

| Test | Action                          | Expected Result                  |
| ---- | ------------------------------- | -------------------------------- |
| 1    | Create remote commit            | Remote moves ahead               |
| 2    | Create conflicting local commit | Histories diverge                |
| 3    | `git pull`                      | Merge starts                     |
| 4    | Same line changed               | Merge conflict                   |
| 5    | `git status`                    | Merge shown as in progress       |
| 6    | Inspect `app.py`                | Conflict markers visible         |
| 7    | `git merge --abort`             | Merge cancelled                  |
| 8    | `git status`                    | No merge in progress             |
| 9    | `git log --graph`               | Local and remote remain diverged |
| 10   | Check local commit              | Local commit still exists        |

---

# Key Learning

A conflicted `git pull` does not mean you must immediately resolve the conflict.

You can safely cancel the merge with:

```bash
git merge --abort
```

The mental model is:

```text
git pull
   ↓
fetch
   ↓
merge
   ↓
CONFLICT
   ↓
git merge --abort
   ↓
back to pre-merge state
```

This is different from a rebase conflict:

```text
git pull --rebase
   ↓
rebase
   ↓
CONFLICT
   ↓
git rebase --abort
```