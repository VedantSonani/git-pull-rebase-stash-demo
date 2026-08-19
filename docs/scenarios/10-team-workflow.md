# Scenario 10 — Complete Team Workflow

## Objective

Demonstrate a realistic day-to-day Git workflow where:

* The remote branch has new commits.
* You have local uncommitted work.
* You need to update your branch.
* You temporarily stash your work.
* You pull with rebase.
* You restore your work.
* You handle a possible conflict.

This scenario combines the concepts covered throughout the practical demo.

---

# Starting State

Make sure your repository is clean:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

Start from:

```text
A --- B --- C
          ↑
     local + remote
```

`C` is the last common commit.

---

# Step 1 — Create a Remote Commit

Go to GitHub.

Open:

```text
app/utils.py
```

Add:

```python
def get_app_info():
    return "Git Demo App"
```

Commit directly on GitHub:

```text
Add application info helper
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

# Step 2 — Create Local Uncommitted Work

Do not pull yet.

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

Do not commit it.

Check:

```bash
git status
```

Expected:

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

Working tree:
MAX_RETRIES = 5
```

---

# Step 3 — Try `git pull --rebase`

Run:

```bash
git pull --rebase
```

Depending on the exact Git state and configuration, Git may refuse to proceed because you have local uncommitted changes.

You may see an error similar to:

```text
error: cannot pull with rebase: You have unstaged changes.
error: please commit or stash them.
```

The important lesson is:

> Your uncommitted work needs to be temporarily moved out of the way before the rebase can proceed.

The reference guide explicitly recommends using `git stash` or `git pull --rebase --autostash` when uncommitted changes prevent a rebase.

---

# Step 4 — Stash the Work

Run:

```bash
git stash
```

Now check:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

The state is now:

```text
A --- B --- C --- D    ← remote
           \
            local     ← still at C

Stash:
MAX_RETRIES = 5
```

---

# Step 5 — Pull with Rebase

Run:

```bash
git pull --rebase
```

Since the working tree is clean, Git can update the branch.

The branch becomes:

```text
A --- B --- C --- D
                    ↑
                  local
```

Because you did not have a local commit, there is nothing to replay.

---

# Step 6 — Restore Your Work

Run:

```bash
git stash pop
```

Git reapplies:

```python
MAX_RETRIES = 5
```

Since the remote developer changed `app/utils.py` and your work is in `app/config.py`, there is no overlap.

The final state is:

```text
A --- B --- C --- D
                    ↑
                  local

Working tree:
MAX_RETRIES = 5
```

Check:

```bash
git status
```

You should see:

```text
modified: app/config.py
```

Your work has been restored.

---

# Step 7 — Commit Your Work

Once you are satisfied with the restored changes:

```bash
git add app/config.py
```

Then:

```bash
git commit -m "Update retry configuration"
```

Now:

```text
A --- B --- C --- D --- E
                        ↑
                      local
```

Your commit is now based on the latest remote commit.

---

# Step 8 — Push

Run:

```bash
git push
```

The remote now contains:

```text
A --- B --- C --- D --- E
                        ↑
                   local + remote
```

The branch is synchronized.

---

# Complete Workflow

The entire workflow was:

```text
Remote developer pushes
        ↓
Remote moves ahead
        ↓
You have uncommitted work
        ↓
git pull --rebase
        ↓
Git needs a clean working tree
        ↓
git stash
        ↓
git pull --rebase
        ↓
Remote changes applied
        ↓
git stash pop
        ↓
Your work restored
        ↓
git add
        ↓
git commit
        ↓
git push
```

---

# Part 2 — The Same Workflow with Autostash

The manual process:

```bash
git stash
git pull --rebase
git stash pop
```

can be shortened to:

```bash
git pull --rebase --autostash
```

The reference guide explicitly describes `--autostash` as performing the stash → pull --rebase → pop sequence automatically.

---

# Step 1 — Return to a Clean State

Make sure:

```bash
git status
```

shows:

```text
nothing to commit, working tree clean
```

---

# Step 2 — Create Another Remote Change

Go to GitHub.

Open:

```text
data/products.json
```

Add another product:

```json
{
  "id": 5,
  "name": "USB-C Hub",
  "price": 2500,
  "category": "Accessories"
}
```

Commit:

```text
Add USB-C hub product
```

Remote moves ahead:

```text
A --- B --- C --- D --- E
                        ↑
                      remote
```

Your local branch is still behind:

```text
A --- B --- C --- D
                    ↑
                  local
```

---

# Step 3 — Create Uncommitted Local Work

Open:

```text
app/config.py
```

Change:

```python
LOG_LEVEL = "INFO"
```

to:

```python
LOG_LEVEL = "DEBUG"
```

Do not commit.

Check:

```bash
git status
```

---

# Step 4 — Use Autostash

Instead of:

```bash
git stash
git pull --rebase
git stash pop
```

run:

```bash
git pull --rebase --autostash
```

Git performs the equivalent workflow automatically:

```text
Automatic stash
      ↓
Pull
      ↓
Rebase
      ↓
Automatic stash pop
```

---

# Step 5 — Verify

Run:

```bash
git status
```

Your local uncommitted change should be back:

```text
modified: app/config.py
```

Check:

```bash
git diff
```

You should see:

```diff
- LOG_LEVEL = "INFO"
+ LOG_LEVEL = "DEBUG"
```

And:

```bash
git log --oneline --graph --decorate --all
```

should show the local branch updated to the latest remote commit.

---

# Part 3 — Team Conflict Scenario

Now we deliberately create the harder case.

The remote developer and your uncommitted work will modify the same area.

---

# Step 1 — Create a Remote Change

On GitHub, change:

```python
TIMEOUT_SECONDS = 30
```

to:

```python
TIMEOUT_SECONDS = 60
```

Commit:

```text
Increase timeout remotely
```

---

# Step 2 — Create Conflicting Local Work

In your local repository, without committing, change:

```python
TIMEOUT_SECONDS = 30
```

to:

```python
TIMEOUT_SECONDS = 90
```

Now:

```text
GitHub:
TIMEOUT_SECONDS = 60

Local:
TIMEOUT_SECONDS = 90
```

---

# Step 3 — Run Autostash

Run:

```bash
git pull --rebase --autostash
```

Conceptually:

```text
Local uncommitted work
        ↓
Automatic stash
        ↓
Pull + rebase
        ↓
Rebase completes
        ↓
Automatic stash pop
        ↓
CONFLICT
```

The important point is that the conflict may happen while the stashed changes are being reapplied.

---

# Step 4 — Inspect the Conflict

Run:

```bash
git status
```

Open:

```text
app/config.py
```

You may see:

```python
<<<<<<< Updated upstream
TIMEOUT_SECONDS = 60
=======
TIMEOUT_SECONDS = 90
>>>>>>> Stashed changes
```

Choose the correct final value.

For this demonstration, choose:

```python
TIMEOUT_SECONDS = 90
```

Remove the conflict markers.

---

# Step 5 — Stage the Resolution

Run:

```bash
git add app/config.py
```

Then:

```bash
git status
```

Verify that there are no unresolved conflicts.

---

# Important Observation

Do not assume that:

```bash
git pull --rebase --autostash
```

means:

```text
No conflicts possible
```

It only automates:

```text
stash
    ↓
rebase
    ↓
stash pop
```

Your stashed changes can still conflict with the updated code.

---

# Part 4 — Compare All Three Workflows

## Standard Pull

```text
git pull
   ↓
fetch
   ↓
merge
   ↓
possible merge conflict
   ↓
git add
git commit
```

---

## Pull with Rebase

```text
git pull --rebase
   ↓
fetch
   ↓
rebase
   ↓
possible rebase conflict
   ↓
git add
git rebase --continue
```

---

## Pull with Autostash

```text
git pull --rebase --autostash
   ↓
automatic stash
   ↓
fetch
   ↓
rebase
   ↓
automatic stash pop
   ↓
possible stash conflict
```

---

# Part 5 — Final Team Workflow

The recommended practical workflow from this demo is:

```text
                 GitHub
                    │
                    │ remote changes
                    ↓
             ┌──────────────┐
             │ Local branch │
             └──────┬───────┘
                    │
             uncommitted work
                    │
                    ↓
       git pull --rebase --autostash
                    │
             ┌──────┴───────┐
             │              │
          clean           conflict
             │              │
        continue       resolve conflict
             │              │
             └──────┬───────┘
                    ↓
                 git add
                    ↓
                git commit
                    ↓
                 git push
                    ↓
                  GitHub
```

---

# Standard Team Scenario

A typical sequence can be:

```bash
git status
git pull --rebase --autostash
git status
git diff
git add .
git commit -m "Complete feature"
git push
```

The exact commands depend on whether you have uncommitted changes and whether conflicts occur.

---

# What If the Rebase Itself Conflicts?

If you have **committed local changes** and run:

```bash
git pull --rebase
```

you may encounter a rebase conflict.

Then:

```bash
git status
```

Resolve:

```bash
git add <file>
```

Continue:

```bash
git rebase --continue
```

Or cancel:

```bash
git rebase --abort
```

---

# What If Stash Reapplication Conflicts?

If your uncommitted changes were stashed and the stash cannot be reapplied cleanly:

```bash
git status
```

Inspect the conflicting file.

Resolve it.

Then:

```bash
git add <file>
```

Do not blindly run:

```bash
git rebase --continue
```

First determine whether the rebase is still active.

---

# Important Team Rule

The reference guide recommends `git pull --rebase` for shared branches when you want to maintain a clean, linear history. It also states the golden rule:

> Never rebase commits that have already been pushed.

The practical distinction is:

```text
Your local, unpushed commits
        ↓
Rebase
        ↓
Generally safe


Already pushed/shared commits
        ↓
Avoid rebasing
        ↓
Can rewrite history other people depend on
```

---

# Final Test Cases

| #  | Situation                      | Command                                                     | Expected Result         |
| -- | ------------------------------ | ----------------------------------------------------------- | ----------------------- |
| 1  | Clean and up to date           | `git pull --rebase`                                         | Nothing to update       |
| 2  | Remote ahead                   | `git pull --rebase`                                         | Fast-forward            |
| 3  | Local commits + remote commits | `git pull --rebase`                                         | Local commits replayed  |
| 4  | Local commit conflicts         | `git pull --rebase`                                         | Rebase conflict         |
| 5  | Rebase conflict                | `git add` + `git rebase --continue`                         | Rebase continues        |
| 6  | Rebase too difficult           | `git rebase --abort`                                        | Rebase cancelled        |
| 7  | Uncommitted changes            | `git stash`                                                 | Clean tree              |
| 8  | Stashed changes                | `git stash pop`                                             | Changes restored        |
| 9  | Uncommitted + remote changes   | `git pull --rebase --autostash`                             | Automatic stash/reapply |
| 10 | Stash overlaps remote          | `git pull --rebase --autostash`                             | Possible stash conflict |
| 11 | Standard pull conflict         | `git pull`                                                  | Merge conflict          |
| 12 | Cancel merge                   | `git merge --abort`                                         | Merge cancelled         |
| 13 | Successful workflow            | `git pull --rebase --autostash` → `git commit` → `git push` | Updated remote          |

---

# Final Mental Model

```text
                       GIT UPDATE
                           │
            ┌──────────────┼──────────────┐
            │              │              │
         git pull      pull --rebase   --autostash
            │              │              │
          merge          rebase       stash first
            │              │              │
     merge conflict   rebase conflict    reapply stash
            │              │              │
      git commit    rebase --continue    possible conflict
            │              │              │
      merge --abort  rebase --abort       resolve
```

And for uncommitted work:

```text
        Uncommitted Changes
                │
        ┌───────┴────────┐
        │                │
     Manual            Automatic
        │                │
   git stash       --autostash
        │                │
   pull --rebase    pull --rebase
        │                │
   stash pop       automatic pop
        │                │
        └───────┬────────┘
                │
         possible conflict
                │
             resolve
                │
             git add
                │
             commit
                │
              push
```