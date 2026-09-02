# Scenario 09 — `git pull --rebase --autostash`

## Objective

Demonstrate how Git can automatically stash uncommitted changes before a rebase and reapply them afterward.

This scenario covers:

* Uncommitted changes
* `git pull --rebase --autostash`
* Automatic stash
* Rebase
* Automatic stash reapplication
* Successful autostash
* Potential conflict when the stash is reapplied

The reference guide describes `git pull --rebase --autostash` as the automatic equivalent of:

```bash
git stash
git pull --rebase
git stash pop
```

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

Start with:

```text
A --- B --- C
          ↑
     local + remote
```

`C` is the last common commit.

---

# Part 1 — Successful Autostash

This first part demonstrates the normal case where the stashed changes can be reapplied cleanly.

---

## Step 1 — Create a Remote Commit

Go to GitHub.

Open:

```text
app/utils.py
```

Add a new helper function at the bottom:

```python
def get_category_count(products):
    return len(products)
```

Commit directly on GitHub.

Example commit message:

```text
Add category count helper
```

The remote is now ahead:

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

## Step 2 — Create Uncommitted Local Changes

Do not commit anything locally.

Open:

```text
app/config.py
```

Change:

```python
TIMEOUT_SECONDS = 30
```

to:

```python
TIMEOUT_SECONDS = 45
```

Now check:

```bash
git status
```

You should see:

```text
Changes not staged for commit:
    modified: app/config.py
```

Your state is now:

```text
Remote:

A --- B --- C --- D

Local:

A --- B --- C
            ↑
          main

Working tree:
TIMEOUT_SECONDS = 45
```

---

## Step 3 — Run Autostash

Run:

```bash
git pull --rebase --autostash
```

Git can temporarily stash the uncommitted change, perform the rebase, and then reapply the change.

Conceptually:

```text
Automatic stash
       ↓
git pull --rebase
       ↓
Remote commit becomes base
       ↓
Reapply local changes
```

---

# Step 4 — Understand the Rebase

Before:

```text
A --- B --- C --- D    ← remote
            \
             local
             
Working tree:
TIMEOUT_SECONDS = 45
```

Git temporarily stores the working-tree change.

Then it updates the branch:

```text
A --- B --- C --- D
                    ↑
                  main
```

There are no committed local changes to replay in this example.

The remote commit is now part of the local branch.

---

# Step 5 — Autostash Is Reapplied

Git then reapplies the automatically stashed change:

```python
TIMEOUT_SECONDS = 45
```

Because GitHub changed `app/utils.py` while your local change was in `app/config.py`, there is no overlap.

The operation should complete successfully.

---

# Step 6 — Verify

Run:

```bash
git status
```

You should see:

```text
Changes not staged for commit:
    modified: app/config.py
```

Your uncommitted change has been restored.

Now:

```bash
git log --oneline --graph --decorate --all
```

You should have a linear history:

```text
* D   (HEAD -> main)
* C
* B
* A
```

And:

```bash
git diff
```

should show:

```diff
- TIMEOUT_SECONDS = 30
+ TIMEOUT_SECONDS = 45
```

---

# Part 2 — Autostash Conflict

Now we will deliberately create a conflict during the automatic stash reapplication.

This is important because:

```bash
git pull --rebase --autostash
```

does **not** guarantee that your uncommitted changes can be reapplied without conflicts.

---

# Step 1 — Return to a Clean State

First commit or discard the previous demonstration change.

If you want to keep it:

```bash
git add app/config.py
git commit -m "Update timeout configuration"
```

Then push if required:

```bash
git push
```

Make sure:

```bash
git status
```

shows:

```text
nothing to commit, working tree clean
```

---

# Step 2 — Create a Remote Change to the Same Line

Go to GitHub.

Open:

```text
app/config.py
```

Change:

```python
TIMEOUT_SECONDS = 45
```

to:

```python
TIMEOUT_SECONDS = 60
```

Commit directly on GitHub.

Example:

```text
Increase timeout remotely
```

The remote now contains:

```text
TIMEOUT_SECONDS = 60
```

Your local repository still contains:

```text
TIMEOUT_SECONDS = 45
```

---

# Step 3 — Create an Uncommitted Local Change

Do not commit the change.

In your local repository, change:

```python
TIMEOUT_SECONDS = 45
```

to:

```python
TIMEOUT_SECONDS = 90
```

Now:

```bash
git status
```

should show:

```text
modified: app/config.py
```

You now have:

```text
GitHub:
TIMEOUT_SECONDS = 60

Local uncommitted:
TIMEOUT_SECONDS = 90
```

---

# Step 4 — Run Autostash

Run:

```bash
git pull --rebase --autostash
```

Git conceptually performs:

```text
stash
  ↓
pull --rebase
  ↓
rebase succeeds
  ↓
stash pop
```

The rebase itself can complete successfully.

The conflict may occur during the final automatic stash reapplication.

---

# Step 5 — Observe the Conflict

Git may report something similar to:

```text
CONFLICT (content): Merge conflict in app/config.py
```

The important distinction is:

```text
Rebase:
    completed

Autostash reapplication:
    conflict
```

The conflict is not necessarily a rebase conflict.

It can be a conflict caused by applying your previously stashed working-tree changes.

---

# Step 6 — Check the Repository

Run:

```bash
git status
```

Git will show the conflicting file:

```text
app/config.py
```

Open it.

You may see:

```python
<<<<<<< Updated upstream
TIMEOUT_SECONDS = 60
=======
TIMEOUT_SECONDS = 90
>>>>>>> Stashed changes
```

The exact wording can vary.

The important parts are:

```text
Updated upstream
```

and:

```text
Stashed changes
```

---

# Step 7 — Resolve the Conflict

For this demonstration, choose:

```python
TIMEOUT_SECONDS = 90
```

Remove the conflict markers.

The final configuration should contain:

```python
DEBUG = True
LOG_LEVEL = "INFO"
MAX_RETRIES = 3
TIMEOUT_SECONDS = 90
```

---

# Step 8 — Stage the Resolution

Run:

```bash
git add app/config.py
```

Then:

```bash
git status
```

The conflict should be resolved.

There is no rebase to continue if the rebase itself has already completed.

Do **not** automatically run:

```bash
git rebase --continue
```

just because the original command contained `--rebase`.

First check:

```bash
git status
```

to determine whether a rebase is actually still in progress.

---

# Manual Equivalent

The automatic workflow:

```bash
git pull --rebase --autostash
```

is conceptually equivalent to:

```bash
git stash
git pull --rebase
git stash pop
```

The manual version makes it easier to see exactly where a conflict occurs.

---

# Compare the Two Workflows

## Manual

```text
Uncommitted changes
        ↓
git stash
        ↓
Clean working tree
        ↓
git pull --rebase
        ↓
Rebase
        ↓
git stash pop
        ↓
Possible conflict
```

## Automatic

```text
Uncommitted changes
        ↓
git pull --rebase --autostash
        ↓
Automatic stash
        ↓
Rebase
        ↓
Automatic stash pop
        ↓
Possible conflict
```

---

# Important Difference

`--autostash` is a **convenience feature**.

It does not change the fundamental Git behavior.

It simply automates:

```bash
git stash
```

and:

```bash
git stash pop
```

around the rebase.

The reference guide explicitly presents this as the shortcut for the manual stash → pull --rebase → pop workflow.

---

# Successful Case

```text
Remote change:
app/utils.py

Local uncommitted change:
app/config.py

        ↓

git pull --rebase --autostash

        ↓

Rebase succeeds

        ↓

Stash reapplies cleanly

        ↓

Working tree contains local change
```

---

# Conflict Case

```text
Remote change:
app/config.py
TIMEOUT_SECONDS = 60

Local uncommitted change:
app/config.py
TIMEOUT_SECONDS = 90

        ↓

git pull --rebase --autostash

        ↓

Automatic stash

        ↓

Rebase succeeds

        ↓

Automatic stash pop

        ↓

CONFLICT
```

---

# Test Cases

| Test | Local State                       | Remote State               | Command                         | Expected Result                       |
| ---- | --------------------------------- | -------------------------- | ------------------------------- | ------------------------------------- |
| 1    | Clean                             | Clean                      | `git pull --rebase --autostash` | Nothing changes                       |
| 2    | Uncommitted change in `config.py` | Change in `utils.py`       | `git pull --rebase --autostash` | Rebase + clean stash restore          |
| 3    | Uncommitted change in `config.py` | Same area changed remotely | `git pull --rebase --autostash` | Possible stash reapplication conflict |
| 4    | Conflict after autostash          | Same file/lines            | `git status`                    | Conflict visible                      |
| 5    | Resolve conflict                  | —                          | `git add`                       | Conflict resolved                     |

---

# Important Questions to Ask During the Demo

### Does autostash commit my changes?

No.

The changes remain uncommitted after they are reapplied.

---

### Does autostash prevent conflicts?

No.

It only temporarily moves uncommitted changes out of the way.

The changes can still conflict when reapplied.

---

### Can the rebase succeed but the overall command still encounter a conflict?

Yes.

The rebase and the stash reapplication are separate stages:

```text
rebase
  ↓
stash reapplication
```

The rebase can finish successfully while applying the stashed changes causes a conflict.

---

### Why use autostash?

It saves you from manually running:

```bash
git stash
git pull --rebase
git stash pop
```

when you have uncommitted changes that you want to keep.

---

# Key Learning

The mental model for:

```bash
git pull --rebase --autostash
```

is:

```text
             Uncommitted work
                    ↓
             Automatic stash
                    ↓
              Pull + rebase
                    ↓
             Updated branch
                    ↓
          Automatic stash pop
                    ↓
             ┌──────┴──────┐
             │             │
          No conflict    Conflict
             │             │
          Work restored   Resolve
```

The command automates the workflow, but it does not eliminate the possibility of conflicts when your uncommitted changes overlap with changes introduced by the update.