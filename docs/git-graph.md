# Git History Visual Guide

This document contains the Git history patterns used throughout the practical demo.

---

## 1. Linear History

Normal development:

```text
A --- B --- C --- D
```

Each commit is based directly on the previous commit.

---

## 2. Diverged History

A local developer and the remote both create commits:

```text
A --- B --- C --- D   ← remote
            \
             E         ← local
```

The histories have diverged.

This is the starting point for demonstrating the difference between `git pull` and `git pull --rebase`.

---

## 3. Standard `git pull`

A standard pull is effectively:

```bash
git fetch
git merge
```

When local and remote histories have diverged:

```text
A --- B --- C --- D   <- remote
            \    /
             E - M     <- local after git pull
```

`M` is the merge commit created when Git combines the two histories.

The result preserves both lines of development but introduces an additional merge commit.

---

## 4. `git pull --rebase`

Instead of creating a merge commit, `git pull --rebase` replays the local commits on top of the updated remote branch.

Before:

```text
A --- B --- C --- D    ← remote
            \
             E          ← local
```

After:

```text
A --- B --- C --- D --- E'
```

`E'` represents the local change replayed on top of `D`.

The resulting history is linear.

---

## 5. Comparing `git pull` and `git pull --rebase`

### `git pull`

```text
git fetch
    ↓
git merge
```

Possible result:

```text
A --- B --- C --- D   <- remote
            \    /
             E - M     <- local after git pull
```

### `git pull --rebase`

```text
git fetch
    ↓
git rebase
```

Result:

```text
A --- B --- C --- D --- E'
```

### Key difference

```text
git pull
    → merge remote and local history
    → may create a merge commit

git pull --rebase
    → move local commits on top of remote
    → keeps history linear
```

---

## 6. Merge Conflict

A merge conflict can occur when the local and remote changes overlap.

Example:

```text
Remote:
VERSION = "2.0"

Local:
VERSION = "3.0"
```

If both changes modify the same part of `app/app.py`:

```bash
git pull
```

Git may stop with:

```text
CONFLICT
```

The file may contain conflict markers:

```text
<<<<<<< HEAD
VERSION = "3.0"
=======
VERSION = "2.0"
>>>>>>> origin/main
```

Resolve the file manually.

Then:

```bash
git add app/app.py
git commit
```

For a conflict caused by a normal `git pull`, the merge is completed with `git commit`.

---

## 7. Aborting a Merge

If the merge conflict should not be resolved:

```bash
git merge --abort
```

Workflow:

```text
git pull
   ↓
CONFLICT
   ↓
git merge --abort
   ↓
Return to state before merge
```

This cancels the in-progress merge and restores the branch and working directory to the state they had before the merge started.

---

## 8. Rebase Conflict

A rebase applies local commits one at a time.

Example:

```text
        D   <- remote
       /
A --- B
       \
        E   <- local
```

Running:

```bash
git pull --rebase
```

causes Git to fetch the remote changes and replay the local commit.

If the local commit conflicts with the remote change:

```text
git pull --rebase
        ↓
CONFLICT
```

Resolve the conflicting file:

```bash
git add app/app.py
```

Then continue the rebase:

```bash
git rebase --continue
```

### Important

During a rebase conflict:

```bash
git rebase --continue
```

is used to continue the replay.

Do **not** use:

```bash
git commit
```

to manually create the commit.

---

## 9. Aborting a Rebase

If the rebase should be cancelled:

```bash
git rebase --abort
```

Workflow:

```text
git pull --rebase
        ↓
    CONFLICT
        ↓
git rebase --abort
        ↓
Return to state before rebase
```

This restores the branch and working directory to the state they had before the rebase began.

---

## 10. Merge Abort vs Rebase Abort

The command depends on the operation currently in progress.

| Situation                           | Command              |
| ----------------------------------- | -------------------- |
| Conflict during `git pull` / merge  | `git merge --abort`  |
| Conflict during `git pull --rebase` | `git rebase --abort` |

Do not interchange these commands.

---

## 11. Stash Workflow

`git stash` temporarily stores uncommitted changes.

Example:

```text
Working tree
    ↓
Uncommitted changes
    ↓
git stash
    ↓
Clean working tree
```

Check the repository:

```bash
git status
```

Then inspect the stash:

```bash
git stash list
```

After completing the required Git operation:

```bash
git stash pop
```

The previously stashed changes are reapplied.

Complete workflow:

```text
Uncommitted work
       ↓
git stash
       ↓
Clean working tree
       ↓
git pull --rebase
       ↓
git stash pop
       ↓
Uncommitted work restored
```

---

## 12. Why Stash Is Useful Before Rebase

Suppose you have uncommitted changes:

```text
A --- B --- C
          +
     uncommitted work
```

You need to update from the remote.

You can temporarily store the work:

```bash
git stash
```

Now:

```text
A --- B --- C
```

The working tree is clean.

You can then run:

```bash
git pull --rebase
```

and restore the changes afterward:

```bash
git stash pop
```

---

## 13. Stash Pop Can Conflict

A successful rebase does **not** guarantee that `git stash pop` will succeed without conflicts.

Example:

Remote change:

```python
VERSION = "2.0"
```

Your stashed change:

```python
VERSION = "3.0"
```

Workflow:

```text
git stash
      ↓
git pull --rebase
      ↓
Rebase succeeds
      ↓
git stash pop
      ↓
CONFLICT
```

The conflict happens because Git is trying to apply the old uncommitted change to the newly updated code.

The rebase itself has already finished.

---

## 14. Resolving a Stash Conflict

If:

```bash
git stash pop
```

produces a conflict:

```text
CONFLICT
```

Inspect the repository:

```bash
git status
```

Open the conflicting file and resolve the conflict markers.

Then stage the resolved file:

```bash
git add app/app.py
```

At this point, the stash application has been resolved.

There is no:

```bash
git rebase --continue
```

because the rebase has already completed.

---

## 15. `git pull --rebase --autostash`

Instead of manually running:

```bash
git stash
git pull --rebase
git stash pop
```

Git provides:

```bash
git pull --rebase --autostash
```

Conceptually:

```text
Automatic stash
      ↓
git pull --rebase
      ↓
Automatic stash pop
```

This is useful when you have uncommitted changes but want Git to temporarily move them out of the way.

---

## 16. Autostash Can Still Conflict

`--autostash` does not guarantee a conflict-free operation.

Example:

```text
Remote:
VERSION = "2.0"

Local uncommitted work:
VERSION = "3.0"
```

Run:

```bash
git pull --rebase --autostash
```

Git effectively performs:

```text
stash
  ↓
pull --rebase
  ↓
rebase succeeds
  ↓
stash pop
  ↓
CONFLICT
```

The conflict is caused by reapplying the stashed changes.

---

## 17. Three Different Conflict Situations

The practical demo contains three important types of conflicts.

### A. Merge conflict

```bash
git pull
```

Conflict resolution:

```bash
git add <file>
git commit
```

---

### B. Rebase conflict

```bash
git pull --rebase
```

Conflict resolution:

```bash
git add <file>
git rebase --continue
```

---

### C. Stash conflict

```bash
git stash pop
```

Conflict resolution:

```bash
git add <file>
```

The rebase is not continued because it has already finished.

---

## 18. Complete Practical Demo

The recommended demonstration sequence is:

```text
01. Create initial project
        ↓
02. git add
        ↓
03. git commit
        ↓
04. git push
        ↓
05. Create remote change on GitHub
        ↓
06. Create local change
        ↓
07. git pull
        ↓
08. Observe merge
        ↓
09. Create merge conflict
        ↓
10. Resolve merge conflict
        ↓
11. Demonstrate git merge --abort
        ↓
12. Create divergence again
        ↓
13. git pull --rebase
        ↓
14. Observe linear history
        ↓
15. Create rebase conflict
        ↓
16. Resolve conflict
        ↓
17. git rebase --continue
        ↓
18. Demonstrate git rebase --abort
        ↓
19. Create uncommitted changes
        ↓
20. git stash
        ↓
21. git pull --rebase
        ↓
22. git stash pop
        ↓
23. Create stash conflict
        ↓
24. Resolve stash conflict
        ↓
25. Demonstrate --autostash
```

---

## 19. Commands Used in the Demo

### Inspect repository

```bash
git status
git log --oneline
git log --oneline --graph --all
git diff
```

### Commit changes

```bash
git add <file>
git commit -m "message"
git push
```

### Pull

```bash
git pull
```

### Abort merge

```bash
git merge --abort
```

### Pull with rebase

```bash
git pull --rebase
```

### Continue rebase

```bash
git add <file>
git rebase --continue
```

### Abort rebase

```bash
git rebase --abort
```

### Stash

```bash
git stash
git stash list
git stash pop
```

### Autostash

```bash
git pull --rebase --autostash
```

---

## 20. Quick Decision Guide

### You have committed local changes

```text
Remote changed?
     ↓
Yes
     ↓
git pull --rebase
```

---

### You have uncommitted changes

Option 1:

```bash
git stash
git pull --rebase
git stash pop
```

Option 2:

```bash
git pull --rebase --autostash
```

---

### `git pull` caused a conflict

```bash
git add <resolved-file>
git commit
```

Or cancel:

```bash
git merge --abort
```

---

### `git pull --rebase` caused a conflict

```bash
git add <resolved-file>
git rebase --continue
```

Or cancel:

```bash
git rebase --abort
```

---

### `git stash pop` caused a conflict

```bash
git add <resolved-file>
```

Resolve the conflict and continue with your normal workflow.

---

## 21. Golden Rule

Never rebase commits that have already been pushed and shared with other developers.

Rebase is safest for local, unpushed commits.

```text
Local + unpushed
        ↓
     Rebase
        ↓
     Safe

Already pushed/shared
        ↓
     Avoid rebase
```

---

## 22. Final Mental Model

```text
                    Git Update
                        │
             ┌──────────┴──────────┐
             │                     │
          git pull          git pull --rebase
             │                     │
           merge                 rebase
             │                     │
        merge conflict       rebase conflict
             │                     │
       git commit           git rebase --continue
             │                     │
       merge --abort         rebase --abort


        Uncommitted Changes
                │
                ↓
            git stash
                │
                ↓
          clean working tree
                │
                ↓
         pull --rebase
                │
                ↓
          git stash pop
                │
         ┌──────┴──────┐
         │             │
       clean        conflict
         │             │
       done        resolve
                       │
                   git add
```

The purpose of this repository is not to build a real application. The application files exist only to create **controlled Git states** that make commits, divergence, merging, rebasing, conflicts, aborts, stashing, and autostashing easy to demonstrate.
