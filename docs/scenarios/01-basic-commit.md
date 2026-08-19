# Scenario 01 — Basic Commit

## Objective

Demonstrate how a local change moves through:

```text
Working Tree
     ↓
Staging Area
     ↓
Local Repository
```

This scenario covers:

* `git status`
* `git diff`
* `git add`
* `git commit`
* `git log`

---

## Starting State

The repository should be clean:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

Initial history:

```text
A --- B --- C
```

---

## Step 1 — Make a Change

Open:

```text
app/config.py
```

Change:

```python
MAX_RETRIES = 3
```

to:

```python
MAX_RETRIES = 5
```

At this point, the change exists only in the working tree.

---

## Step 2 — Check Repository Status

Run:

```bash
git status
```

Expected:

```text
Changes not staged for commit:
    modified: app/config.py
```

The file has changed, but it has not been staged.

---

## Step 3 — Inspect the Change

Run:

```bash
git diff
```

You should see something similar to:

```diff
- MAX_RETRIES = 3
+ MAX_RETRIES = 5
```

`git diff` shows changes that are currently in the working tree but have not been staged.

---

## Step 4 — Stage the Change

Run:

```bash
git add app/config.py
```

Check the status:

```bash
git status
```

Expected:

```text
Changes to be committed:
    modified: app/config.py
```

The change has now moved from:

```text
Working Tree
     ↓
Staging Area
```

---

## Step 5 — Inspect the Staged Change

Run:

```bash
git diff --staged
```

You should again see:

```diff
- MAX_RETRIES = 3
+ MAX_RETRIES = 5
```

This is useful for demonstrating the difference between:

```bash
git diff
```

and:

```bash
git diff --staged
```

---

## Step 6 — Create the Commit

Run:

```bash
git commit -m "Update retry configuration"
```

Expected output will be similar to:

```text
[main abc1234] Update retry configuration
 1 file changed, 1 insertion(+), 1 deletion(-)
```

The change is now stored as a commit in the local repository.

---

## Step 7 — Verify the Commit

Run:

```bash
git status
```

Expected:

```text
nothing to commit, working tree clean
```

Then:

```bash
git log --oneline --graph --decorate -5
```

You should see the new commit:

```text
* abc1234 (HEAD -> main) Update retry configuration
* C
* B
* A
```

---

## Step 8 — Understand What Happened

The complete flow was:

```text
Edit app/config.py
       ↓
Working Tree
       ↓
git add app/config.py
       ↓
Staging Area
       ↓
git commit
       ↓
Local Repository
```

Nothing has been sent to GitHub yet.

To share this commit with the remote:

```bash
git push
```

---

## Important Demonstration Point

A commit is **local**.

Running:

```bash
git commit
```

does not automatically update GitHub.

The remote is updated only when you explicitly run:

```bash
git push
```

---

## Test Case

| Test | Action                  | Expected Result             |
| ---- | ----------------------- | --------------------------- |
| 1    | Modify `config.py`      | Working tree becomes dirty  |
| 2    | `git status`            | Shows unstaged modification |
| 3    | `git diff`              | Shows working-tree changes  |
| 4    | `git add app/config.py` | Change becomes staged       |
| 5    | `git diff --staged`     | Shows staged change         |
| 6    | `git commit -m "..."`   | New local commit created    |
| 7    | `git status`            | Working tree is clean       |
| 8    | `git log --oneline`     | New commit is visible       |

---

## Reset for Next Scenario

If you want to return to the state before this scenario:

```bash
git reset --hard HEAD~1
```

**Warning:** This removes the commit and its changes from the current branch.

For the main demo, it is usually better to keep this commit and use it as the starting point for the next scenarios.
