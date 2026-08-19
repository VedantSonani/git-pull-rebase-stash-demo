# Scenario 08 — `git stash`

## Objective

Demonstrate how `git stash` temporarily stores uncommitted changes so the working tree becomes clean.

This scenario covers:

* Uncommitted changes
* `git status`
* `git diff`
* `git stash`
* `git stash list`
* `git stash pop`
* Restoring uncommitted work

The reference guide describes the basic stash workflow as temporarily hiding uncommitted changes, performing another Git operation with a clean working tree, and then restoring the changes with `git stash pop`.

---

# Starting State

Make sure the repository is clean:

```bash id="f7x8m2"
git status
```

Expected:

```text id="8d0p3x"
On branch main
nothing to commit, working tree clean
```

For this scenario, there is no need for a local/remote divergence yet.

The repository can simply be:

```text id="5k3v1q"
A --- B --- C
          ↑
         main
```

---

# Step 1 — Make an Uncommitted Change

Open:

```text id="s9h4j7"
app/config.py
```

Find:

```python id="r2k6m1"
MAX_RETRIES = 3
```

Change it to:

```python id="n8p5q4"
MAX_RETRIES = 5
```

Do **not** commit the change.

Your working tree is now:

```text id="y1c7v3"
Last commit
    ↓
MAX_RETRIES = 3

Working tree
    ↓
MAX_RETRIES = 5
```

---

# Step 2 — Check the Working Tree

Run:

```bash id="b6m9x2"
git status
```

You should see:

```text id="q4v8k1"
Changes not staged for commit:
    modified: app/config.py
```

This confirms that the change is currently uncommitted.

---

# Step 3 — Inspect the Change

Run:

```bash id="p3r7w5"
git diff
```

You should see:

```diff id="z6t2n9"
- MAX_RETRIES = 3
+ MAX_RETRIES = 5
```

At this point:

```text id="d8f4h2"
Repository
   │
   ├── committed history
   │
   └── uncommitted working-tree change
```

---

# Step 4 — Stash the Change

Run:

```bash id="m5q9s1"
git stash
```

Git temporarily stores your uncommitted changes.

You should see output similar to:

```text id="v2k7p6"
Saved working directory and index state WIP on main: ...
```

---

# Step 5 — Check the Working Tree

Run:

```bash id="x4n8c3"
git status
```

Expected:

```text id="j9w5r2"
On branch main
nothing to commit, working tree clean
```

The working tree is now clean.

Your change has not been deleted.

It has been stored in the stash.

---

# Step 6 — View the Stash

Run:

```bash id="q7m3v8"
git stash list
```

You should see something similar to:

```text id="h2k9p4"
stash@{0}: WIP on main: <commit>
```

`stash@{0}` is the most recent stash.

---

# Step 7 — Inspect the Stashed Change

You can inspect the stash with:

```bash id="n5x1c7"
git stash show
```

For a full patch:

```bash id="r8v4m2"
git stash show -p
```

You should see the change:

```diff id="b3k7q9"
- MAX_RETRIES = 3
+ MAX_RETRIES = 5
```

This demonstrates that the change still exists even though the working tree is clean.

---

# Step 8 — Perform Another Git Operation

Now that the working tree is clean, you can perform operations that may require a clean working tree.

For example:

```bash id="w6p2n8"
git pull --rebase
```

If there are no remote changes, Git may simply report:

```text id="v9k3m5"
Current branch main is up to date.
```

The important point is that the operation can proceed without your uncommitted changes getting in the way.

---

# Step 9 — Restore the Stashed Changes

Run:

```bash id="c4x7n1"
git stash pop
```

Git applies the stashed changes back to your working tree.

You should see output similar to:

```text id="q8m2v6"
On branch main
Changes not staged for commit:
    modified: app/config.py
```

---

# Step 10 — Verify the Change

Run:

```bash id="p5r9k3"
git status
```

You should again see:

```text id="s1x6w4"
Changes not staged for commit:
    modified: app/config.py
```

Then:

```bash id="m7n2q8"
git diff
```

You should see:

```diff id="z4c9v1"
- MAX_RETRIES = 3
+ MAX_RETRIES = 5
```

Your original uncommitted change has been restored.

---

# Step 11 — Check the Stash List

Run:

```bash id="x8p3k5"
git stash list
```

Normally, after a successful:

```bash id="j6m1r9"
git stash pop
```

the stash entry is removed.

So the list may be empty:

```text id="a2v7c4"
```

This is an important distinction between:

```bash id="w9n5q2"
git stash pop
```

and:

```bash id="d3k8m6"
git stash apply
```

`pop` applies the stash and normally removes it.

`apply` applies the stash but keeps the stash entry.

---

# Step 12 — Optional: Demonstrate `git stash apply`

If you want to demonstrate the difference:

First create another change:

```text id="f4q8m2"
MAX_RETRIES = 5
```

Change it to:

```text id="r7c3n9"
MAX_RETRIES = 10
```

Then:

```bash id="k1v6p4"
git stash
```

Check:

```bash id="b8m2x5"
git stash list
```

Now apply it without removing the stash:

```bash id="q3n7c1"
git stash apply
```

Check:

```bash id="w5r9k2"
git stash list
```

The stash should still exist.

This is useful if you want to reuse the same stash more than once.

For the main demo, however, use `git stash pop` because it represents the normal stash → update → restore workflow from the reference guide.

---

# Step 13 — Understand What `git stash` Does

Before stash:

```text id="y6m2p8"
A --- B --- C
          ↑
         HEAD

Working tree:
MAX_RETRIES = 5
```

Run:

```bash id="j4x8q1"
git stash
```

The working tree becomes clean:

```text id="c7v3n9"
A --- B --- C
          ↑
         HEAD

Working tree:
clean

Stash:
MAX_RETRIES = 5
```

Then:

```bash id="z2k6r4"
git stash pop
```

The changes are reapplied:

```text id="p8m5x1"
A --- B --- C
          ↑
         HEAD

Working tree:
MAX_RETRIES = 5
```

The change is still **uncommitted**.

---

# Important Point

`git stash` does **not** create a normal commit on your current branch.

After:

```bash id="v4q1n8"
git stash
```

your branch's visible history remains unchanged.

The stash is a separate temporary storage mechanism for your working changes.

---

# Stash Does Not Mean "Commit"

Compare:

### Commit

```bash id="m9c2x7"
git add app/config.py
git commit -m "Update retry configuration"
```

Result:

```text id="k5r8p3"
A --- B --- C --- D
```

Your change becomes part of branch history.

---

### Stash

```bash id="q6n1v4"
git stash
```

Result:

```text id="t3x7m2"
A --- B --- C
```

The branch history does not move.

Your working change is temporarily stored.

---

# Practical Use Case

Imagine you are working on:

```text id="r4k8p1"
Feature A
```

and suddenly need to update your branch before continuing.

You have:

```text id="y2m6q9"
Uncommitted Feature A changes
```

Instead of committing incomplete work, you can:

```bash id="h5v9c3"
git stash
```

Then:

```bash id="n7x2m4"
git pull --rebase
```

Then:

```bash id="p1q6k8"
git stash pop
```

Your unfinished work is restored on top of the updated code.

---

# Complete Stash Workflow

```text id="c8m3v7"
Uncommitted changes
        ↓
    git stash
        ↓
  Clean working tree
        ↓
   Git operation
        ↓
   git stash pop
        ↓
Uncommitted changes restored
```

For example:

```bash id="x4p8n2"
git stash
git pull --rebase
git stash pop
```

---

# Stash and Rebase

The reference guide specifically presents this workflow:

```bash id="m7q1v5"
git stash
git pull --rebase
git stash pop
```

The purpose is:

```text id="a9k3r6"
stash
 ↓
clean working tree
 ↓
pull --rebase
 ↓
restore changes
```

It also introduces the shortcut:

```bash id="f2x6m8"
git pull --rebase --autostash
```

which automates the stash → rebase → pop sequence.

---

# Important: `git stash pop` Can Conflict

Stashing does **not** guarantee that the changes can later be reapplied cleanly.

For example:

```text id="c5n9r2"
Remote:
MAX_RETRIES = 10

Stash:
MAX_RETRIES = 5
```

If the remote changes the same part of the file while your changes are stashed:

```bash id="v8m4q1"
git stash
git pull --rebase
git stash pop
```

the rebase may complete successfully, but `git stash pop` can then produce a conflict.

That scenario will be demonstrated separately.

---

# Test Case

| Test | Action                | Expected Result                        |
| ---- | --------------------- | -------------------------------------- |
| 1    | Modify `config.py`    | Uncommitted change                     |
| 2    | `git status`          | Working tree is dirty                  |
| 3    | `git diff`            | Change visible                         |
| 4    | `git stash`           | Working tree becomes clean             |
| 5    | `git status`          | Nothing to commit                      |
| 6    | `git stash list`      | Stash entry visible                    |
| 7    | `git stash show -p`   | Stashed changes visible                |
| 8    | Perform Git operation | Operation can proceed with clean tree  |
| 9    | `git stash pop`       | Changes restored                       |
| 10   | `git status`          | Original changes are uncommitted again |
| 11   | `git diff`            | Original changes visible               |

---

# Key Learning

`git stash` is useful when you have **unfinished, uncommitted work** that you temporarily need to put aside.

The core workflow is:

```bash id="n2v6x9"
git stash
git pull --rebase
git stash pop
```

The important mental model is:

```text id="r5m8k3"
        Working Tree
             │
             │ git stash
             ↓
        Clean Tree
             │
             │ Git operation
             ↓
        Updated Tree
             │
             │ git stash pop
             ↓
      Your work restored
```
