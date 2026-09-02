# Scenario 05 — `git pull --rebase`

## Objective

Demonstrate how `git pull --rebase` handles diverged local and remote histories.

This scenario covers:

* Diverged history
* `git fetch`
* `git pull --rebase`
* Replay of local commits
* Linear history
* Difference between `git pull` and `git pull --rebase`
* Inspecting history with `git log --graph`

The reference guide explains `git pull --rebase` as fetching the remote changes, temporarily setting aside local unpushed commits, updating the local branch, and replaying those commits on top of the updated remote branch.

---

# Starting State

Make sure the working tree is clean:

```bash id="kz4w0s"
git status
```

Expected:

```text id="s7qg6a"
On branch main
nothing to commit, working tree clean
```

For this scenario, start from a clean common point:

```text id="1n3q8f"
A --- B --- C
          ↑
     local + remote
```

`C` is the last commit shared by both local and remote.

---

# Step 1 — Create a Remote Commit

Go to GitHub.

Open:

```text id="d0u1t2"
app/config.py
```

Change:

```python id="y4w5r6"
TIMEOUT_SECONDS = 30
```

to:

```python id="h7i8j9"
TIMEOUT_SECONDS = 60
```

Commit directly on GitHub.

Use a message such as:

```text id="k1l2m3"
Increase request timeout
```

The remote branch is now:

```text id="n4o5p6"
A --- B --- C --- D
                    ↑
                  remote
```

Your local branch is still:

```text id="q7r8s9"
A --- B --- C
            ↑
          local
```

---

# Step 2 — Create a Local Commit

Do not pull the remote change yet.

In your local repository, open:

```text id="t0u1v2"
app/utils.py
```

Change:

```python id="w3x4y5"
def is_valid_quantity(quantity):
    return quantity > 0
```

to:

```python id="z6a7b8"
def is_valid_quantity(quantity):
    return quantity >= 0
```

Stage and commit:

```bash id="c9d0e1"
git add app/utils.py
git commit -m "Allow zero quantity"
```

Your local branch now contains a commit that the remote does not have.

The histories have diverged:

```text id="f2g3h4"
A --- B --- C --- D    ← remote
           \
            E          ← local
```

Where:

```text id="i5j6k7"
C = common ancestor
D = remote commit
E = local commit
```

---

# Step 3 — Verify the Divergence

Run:

```bash id="l8m9n0"
git fetch
```

Then:

```bash id="p1q2r3"
git log --oneline --graph --decorate --all
```

Conceptually:

```text id="s4t5u6"
        D   ← origin/main
       /
A --- B --- C
           \
            E   ← HEAD -> main
```

The important relationship is:

```text id="v7w8x9"
C
├── D ← remote
└── E ← local
```

---

# Step 4 — Run `git pull --rebase`

Now run:

```bash id="y0z1a2"
git pull --rebase
```

Git performs the equivalent of:

```text id="b3c4d5"
git fetch
     ↓
temporarily set aside local commits
     ↓
update local branch to remote
     ↓
replay local commits
```

Git does **not** create a merge commit.

---

# Step 5 — Understand What Git Does

Before the rebase:

```text id="e6f7g8"
A --- B --- C --- D    ← remote
           \
            E          ← local
```

Git temporarily sets aside `E`.

The local branch is updated to:

```text id="h9i0j1"
A --- B --- C --- D
                    ↑
                  local
```

Git then replays the changes introduced by `E`.

A new commit is created:

```text id="k2l3m4"
A --- B --- C --- D --- E'
```

The important point is:

```text id="n5o6p7"
E  = original local commit

E' = replayed version of E
```

`E'` has a different commit identity because it now has a different parent (`D`).

---

# Step 6 — Verify the Result

Run:

```bash id="q8r9s0"
git status
```

Expected:

```text id="t1u2v3"
On branch main
nothing to commit, working tree clean
```

Then:

```bash id="w4x5y6"
git log --oneline --graph --decorate --all
```

You should now see a linear history similar to:

```text id="z7a8b9"
* E'  (HEAD -> main) Allow zero quantity
* D   (origin/main) Increase request timeout
* C
* B
* A
```

There is no merge commit.

---

# Step 7 — Compare With Standard `git pull`

A standard pull with diverged history can produce:

```text id="c0d1e2"
        D
       / \
C -----   M
       \ /
        E
```

where `M` is a merge commit.

With rebase:

```text id="f3g4h5"
A --- B --- C --- D --- E'
```

The history is linear.

---

# Step 8 — View the Difference

Run:

```bash id="i6j7k8"
git log --oneline --graph --decorate --all
```

Compare the two approaches.

### Standard pull

```text id="l9m0n1"
        D
       / \
C ----   M
       \ /
        E
```

### Pull with rebase

```text id="o2p3q4"
A --- B --- C --- D --- E'
```

The main difference is whether Git **merges** the histories or **replays** the local commits on top of the remote history.

---

# Step 9 — Inspect the Commit IDs

Run:

```bash id="r5s6t7"
git log --oneline --all
```

Notice that the original local commit `E` is no longer the tip of your branch.

Instead, the rebased commit `E'` is present.

This happens because Git creates a new commit when replaying the local changes.

---

# Step 10 — Understand the Four Rebase Stages

The guide describes the rebase process in four conceptual stages:

```text id="u8v9w0"
1. Fetch
      ↓
2. Rewind
      ↓
3. Update
      ↓
4. Replay
```

### 1. Fetch

Git downloads commits from the remote.

### 2. Rewind

Git temporarily sets aside local commits that have not been pushed.

### 3. Update

The local branch is moved to the latest remote commit.

### 4. Replay

The local commits are reapplied one by one on top of the updated branch.

---

# Why Does `E` Become `E'`?

Suppose the original history was:

```text id="x1y2z3"
C --- E
```

The parent of `E` is `C`.

After the remote update:

```text id="a4b5c6"
C --- D
```

The rebase wants the local change on top of `D`:

```text id="d7e8f9"
C --- D --- E'
```

Because `E'` now has `D` as its parent rather than `C`, it is a new commit.

The changes may be identical, but the commit identity is different.

---

# Important Demonstration Point

This scenario should be performed with **committed local work**.

You should have:

```text id="g0h1i2"
local commit
      +
remote commit
      ↓
git pull --rebase
```

For uncommitted changes, Git may require you to stash them first.

That will be demonstrated separately in the stash scenarios.

---

# Test Case

| Test | Action                        | Expected Result                  |
| ---- | ----------------------------- | -------------------------------- |
| 1    | Create remote commit          | Remote moves ahead               |
| 2    | Create local commit           | Local moves ahead independently  |
| 3    | `git fetch`                   | Remote information downloaded    |
| 4    | `git log --graph`             | Diverged history visible         |
| 5    | `git pull --rebase`           | Rebase begins                    |
| 6    | Remote commit applied as base | Local branch moves to remote tip |
| 7    | Local commit replayed         | New local commit created         |
| 8    | `git log --graph`             | Linear history                   |
| 9    | `git status`                  | Working tree clean               |

---

# Key Learning

When local and remote branches have diverged:

```bash id="j3k4l5"
git pull
```

uses merge and may create:

```text id="m6n7o8"
merge commit
```

while:

```bash id="p9q0r1"
git pull --rebase
```

replays the local commits on top of the remote commits:

```text id="s2t3u4"
A --- B --- C --- D --- E'
```

The reference guide summarizes the comparison as:

```text id="v5w6x7"
git pull
    → fetch + merge
    → branched history
    → possible merge commit

git pull --rebase
    → fetch + rebase
    → linear history
    → no extra merge commit
```