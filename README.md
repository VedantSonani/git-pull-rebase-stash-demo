# Git Pull, Rebase & Stash Demo

A practical Git repository designed to demonstrate Git workflows involving:

- `git add`
- `git commit`
- `git push`
- `git pull`
- `git pull --rebase`
- Merge conflicts
- Rebase conflicts
- `git merge --abort`
- `git rebase --abort`
- `git rebase --continue`
- `git stash`
- `git stash pop`
- `git pull --rebase --autostash`
- Team collaboration and diverged branches

The repository is intentionally small so that Git history and conflicts are easy to see during a live demonstration.

---

## Repository Structure

```text
git-pull-rebase-stash-demo/
│
├── app/
│   ├── app.py
│   ├── config.py
│   └── utils.py
│
├── data/
│   └── products.json
│
├── docs/
│   ├── scenarios/
│   │   ├── 01-basic-commit.md
│   │   ├── 02-standard-pull.md
│   │   ├── 03-pull-conflict.md
│   │   ├── 04-pull-abort.md
│   │   ├── 05-pull-rebase.md
│   │   ├── 06-rebase-conflict.md
│   │   ├── 07-rebase-abort.md
│   │   ├── 08-stash.md
│   │   ├── 09-autostash.md
│   │   └── 10-team-workflow.md
│   │
│   └── git-graph.md
│
├── scripts/
│   ├── setup-demo.sh
│   └── reset-demo.sh
│
├── .gitignore
└── README.md