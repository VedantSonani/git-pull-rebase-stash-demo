# Scenario 02 — Standard `git pull`

## Objective

Demonstrate how `git pull` updates a local repository from GitHub.

This scenario covers:

* `git fetch`
* `git pull`
* Fast-forward pull
* Diverged history
* Merge commit created by `git pull`
* Viewing the resulting history with `git log --graph`

---

# Part 1 — Fast-Forward Pull

## Starting State

Make sure the local repository is clean:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

The local and remote repositories are currently aligned:

```text
A --- B --- C
          ↑
       local
       remote
```

---

## Step 1 — Create a Remote Change

Open the repository on GitHub.

Edit:

```text
app/utils.py
```

Change:

```python
def is_valid_quantity(quantity):
    return quantity > 0
```

to:

```python
def is_valid_quantity(quantity):
    return quantity >= 0
```

Commit the change directly on GitHub.

For example:

```text
Commit message:

"Allow zero quantity"
```

The remote repository is now ahead of your local repository:

```text
A --- B --- C --- D
          local  ↑
                 remote
```

More precisely:

```text
A --- B --- C --- D
                ↑
              remote

A --- B --- C
            ↑
          local
```

`C` is the last commit that both repositories share.

---

## Step 2 — Check Local History

Your local repository does not know about `D` yet.

Run:

```bash
git log --oneline --graph --decorate -5
```

You should still see:

```text
C
B
A
```

---

## Step 3 — Run `git pull`

Run:

```bash
git pull
```

Git downloads the remote commit and updates your local branch.

Because your local branch has no unique commits, Git can perform a fast-forward.

The history becomes:

```text
A --- B --- C --- D
                    ↑
              local + remote
```

There is no merge commit.

---

## Step 4 — Verify

Run:

```bash
git status
```

Expected:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Then:

```bash
git log --oneline --graph --decorate -5
```

You should see the new remote commit.

---

# Part 2 — Diverged History

Now we will create the situation where `git pull` performs a merge.

The important state is:

```text
A --- B --- C --- D    ← remote
           \
            E          ← local
```

Here:

* `A → B → C` = common history
* `D` = new remote commit
* `E` = new local commit
* `C` = common ancestor
* The histories diverged after `C`

---

## Step 1 — Create a Remote Commit

Go to GitHub.

Modify:

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

Commit directly on GitHub:

```text
"Enable debug logging"
```

The remote now contains:

```text
A --- B --- C --- D
                    ↑
                  remote
```

Your local repository still has:

```text
A --- B --- C
            ↑
          local
```

---

## Step 2 — Create a Local Commit

Do not pull yet.

In your local repository, modify:

```text
app/utils.py
```

Change:

```python
def format_message(message):
    return message.strip().capitalize()
```

to:

```python
def format_message(message):
    return message.strip().upper()
```

Check:

```bash
git status
```

Stage and commit:

```bash
git add app/utils.py
git commit -m "Improve message formatting"
```

Now your local history is:

```text
A --- B --- C --- E    ← local
           \
            D          ← remote
```

The exact visual layout can vary, but the important relationship is:

```text
       D   ← remote
      /
A---B---C
      \
       E   ← local
```

**`C` is the common ancestor.**

---

## Step 3 — Confirm the Branches Have Diverged

Run:

```bash
git fetch
```

This downloads the remote information without merging it into your current branch.

Now run:

```bash
git log --oneline --graph --decorate --all
```

You should see two different tips:

```text
* E (HEAD -> main)
| 
| * D (origin/main)
|/
* C
```

The exact ordering of the lines may differ depending on the commit history, but you should have:

```text
C
├── D ← origin/main
└── E ← main
```

---

# Part 3 — Run Standard `git pull`

Now run:

```bash
git pull
```

Conceptually, standard `git pull` performs:

```text
git fetch
    ↓
git merge
```

Git fetches `D` and then merges it with your local `E`.

Because the histories have diverged, Git creates a merge commit.

The resulting history is:

```text
        D   ← remote commit
       / \
      /   \
A --- B --- C
           \ \
            E M
              ↑
           merge commit
```

A clearer representation using commit relationships is:

```text
          D
         / \
        /   \
C -----/     M
 \           /
  E --------
```

The exact visual output should be checked with:

```bash
git log --oneline --graph --decorate --all
```

The important relationship is:

```text
C = common ancestor
D = remote commit
E = local commit
M = merge commit
```

---

# Part 4 — Verify the Merge Commit

Run:

```bash
git log --oneline --graph --decorate --all
```

You should see a structure similar to:

```text
*   M Merge branch 'main' of ...
|\
| * D Enable debug logging
* | E Improve message formatting
|/
* C
```

The exact commit hashes and messages will depend on your repository.

The important part is the merge commit:

```text
M
├── D
└── E
```

---

# Part 5 — Verify the Working Tree

Run:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

The local branch now contains both changes:

```text
Remote change
     +
Local change
     ↓
Merge commit
```

---

# What `git pull` Did

Before pulling:

```text
        D   ← remote
       /
A --- B --- C
           \
            E   ← local
```

After:

```text
        D
       / \
      /   \
A --- B --- C
           \ \
            E M
              ↑
             HEAD
```

Conceptually:

```text
git pull
    ↓
git fetch
    ↓
git merge
    ↓
merge commit
```

---

# Important Comparison

### Fast-forward case

When there are no local commits that the remote doesn't have:

```text
Local:

A --- B --- C

Remote:

A --- B --- C --- D
```

`git pull` can simply move the local branch forward:

```text
A --- B --- C --- D
```

No merge commit is required.

---

### Diverged case

When both sides have unique commits:

```text
        D   ← remote
       /
A --- B --- C
           \
            E   ← local
```

`git pull` performs a merge:

```text
        D
       / \
      /   \
     C     M
      \   /
       E
```

The result contains a merge commit.

---

# Useful Commands During the Demo

### Check working tree

```bash
git status
```

### See local changes

```bash
git diff
```

### Download remote information without merging

```bash
git fetch
```

### See all branches and commits

```bash
git log --oneline --graph --decorate --all
```

### Standard pull

```bash
git pull
```

### See the current branch

```bash
git branch --show-current
```

### See remote branches

```bash
git branch -r
```

---

# Key Learning

`git pull` is effectively:

```text
git fetch + git merge
```

When local and remote histories have diverged, the merge step may create an additional merge commit.

This is the main behavior we will compare against:

```bash
git pull --rebase
```

in the next scenario.

---

# Test Cases

| Test | Local State                        | Remote State                 | Command    | Expected Result   |
| ---- | ---------------------------------- | ---------------------------- | ---------- | ----------------- |
| 1    | Up to date                         | Up to date                   | `git pull` | Nothing to update |
| 2    | Behind                             | Ahead                        | `git pull` | Fast-forward      |
| 3    | Local + remote diverged            | Diverged                     | `git pull` | Merge commit      |
| 4    | Remote changed different file      | Local changed different file | `git pull` | Clean merge       |
| 5    | Remote and local modify same lines | Diverged                     | `git pull` | Merge conflict    |

---

# Demo Reset Point

After completing this scenario, the repository should contain a merge commit.

For the next scenario, we will create a **fresh divergence** and demonstrate:

```bash
git pull --rebase
```

The goal is to compare:

```text
git pull
    ↓
merge
    ↓
merge commit
```

against:

```text
git pull --rebase
    ↓
rebase
    ↓
linear history
```
