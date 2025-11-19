# Git Commands Reference (2025 Edition)

This document provides a quick reference for all git commands used in the GitHub-Native Operating Model, organized by category with modern 2025 syntax and best practices.

## Table of Contents

- [Branching Commands](#branching-commands)
- [Staging Commands](#staging-commands)
- [Committing Commands](#committing-commands)
- [Pushing Commands](#pushing-commands)
- [Inspection Commands](#inspection-commands)
- [Worktree Commands](#worktree-commands)
- [Safety & Governance](#safety--governance)

---

## Branching Commands

### Create and Switch to New Branch (Modern Syntax)

```bash
git switch -c <branch-name>
```

**Examples:**
```bash
git switch -c feature/123-improve-auth
git switch -c bugfix/456-fix-login
git switch -c refactor/database-layer
git switch -c docs/update-readme
```

**Why use `git switch -c` instead of `git checkout -b`?**
- Introduced in Git 2.23 (August 2019)
- Clearer intent: `switch` is explicitly for branches
- Reduces confusion (checkout did too many things)
- Recommended by Git team for modern workflows

**Legacy syntax (avoid in new workflows):**
```bash
git checkout -b <branch-name>  # Still works, but outdated
```

### Switch to Existing Branch

```bash
git switch <branch-name>
```

**Examples:**
```bash
git switch main
git switch feature/123-improve-auth
git switch -  # Switch to previous branch
```

### List Branches

```bash
git branch        # List local branches
git branch -a     # List all branches (local + remote)
git branch -r     # List remote branches only
```

### Delete Branch

```bash
git branch -d <branch-name>   # Safe delete (only if merged)
git branch -D <branch-name>   # Force delete (use with caution)
```

**Best Practice:** Delete branches immediately after PR merge to keep repository clean.

---

## Staging Commands

### Stage All Changes

```bash
git add .
```

**Alternative (functionally equivalent in most contexts):**
```bash
git add -A
```

### Stage Specific Files

```bash
git add <file1> <file2>
```

**Example:**
```bash
git add src/auth.py tests/test_auth.py
```

### Unstage Files (Modern Syntax)

```bash
git restore --staged <file>
```

**Legacy syntax (avoid):**
```bash
git reset HEAD <file>  # Outdated
```

---

## Committing Commands

### Commit with Message (Imperative Mood)

```bash
git commit -m "Add token expiration validation to auth service"
```

**Best Practices:**
- Use imperative mood ("Add", "Fix", "Update", not "Added", "Fixed")
- Keep first line under 50 characters
- Focus on *why* not *what* (code shows what)
- Reference issue numbers when applicable

**Examples of good commit messages:**
```bash
git commit -m "Fix authentication timeout issue (#123)"
git commit -m "Add user profile caching layer"
git commit -m "Update docs to reflect new API endpoints"
git commit -m "Refactor database connection pooling"
```

### Commit with Detailed Message

```bash
git commit
```

This opens your editor for a multi-line commit message:
```
Add token expiration validation to auth service

- Implement JWT token expiration checking
- Add unit tests for token validation
- Update auth middleware to handle expired tokens

Fixes #123
```

---

## Pushing Commands

### Push and Set Upstream Tracking

```bash
git push -u origin <branch-name>
```

**Example:**
```bash
git push -u origin feature/123-improve-auth
```

**Why use `-u` flag?**
- Sets upstream tracking for the branch
- Future `git push` and `git pull` commands work without specifying remote/branch
- Saves typing and prevents errors

### Push to Existing Tracked Branch

```bash
git push
```

**Note:** Only works after upstream tracking is set (via `-u` flag or automatically by GitHub)

### Force Push (Use with Extreme Caution)

```bash
git push --force
```

**⚠️ WARNING:** Never use unless explicitly required and you understand the consequences.
- Can overwrite others' work
- Can break team workflows
- Violates governance in most protected workflows

**Safer alternative (if you must force push):**
```bash
git push --force-with-lease
```
This checks that your local view of the remote is up-to-date before force pushing.

---

## Inspection Commands

### Check Repository Status

```bash
git status
```

**Best Practice:** Run before every commit to verify what you're committing.

**Example output interpretation:**
- Red files: Untracked or modified but not staged
- Green files: Staged for commit
- "nothing to commit, working tree clean": Safe state

### View Unstaged Changes

```bash
git diff
```

**View staged changes:**
```bash
git diff --staged
```

**Best Practice:** Review diffs before committing to catch unintended changes.

### View Commit History

```bash
git log --oneline
```

**Shows concise commit history (recommended for quick inspection):**
```
a1b2c3d Fix auth timeout (#123)
d4e5f6g Add user caching
h7i8j9k Update API docs
```

**More detailed history:**
```bash
git log                    # Full commit details
git log --graph            # ASCII graph of branches
git log --oneline --graph  # Concise graph view
```

### View Specific Commit Details

```bash
git show <commit-sha>
```

**Example:**
```bash
git show a1b2c3d
```

---

## Worktree Commands

Git worktrees enable parallel development by creating multiple working directories from a single repository. Critical for multi-agent development scenarios.

### Create New Worktree

```bash
git worktree add <path> <branch-name>
```

**Example:**
```bash
git worktree add ../feature-123-auth feature/123-improve-auth
```

**Creates:**
- A new directory at `../feature-123-auth`
- Checked out to branch `feature/123-improve-auth`
- Shares the same Git database (no duplication)

### List All Worktrees

```bash
git worktree list
```

**Example output:**
```
/home/user/project                main
/home/user/feature-123-auth       feature/123-improve-auth
/home/user/bugfix-456-login       bugfix/456-fix-login
```

### Remove Worktree

```bash
git worktree remove <path>
```

**Example:**
```bash
git worktree remove ../feature-123-auth
```

**Or manually delete the directory and run:**
```bash
git worktree prune
```

### Why Use Worktrees?

**Use Cases:**
- Multiple agents working in parallel without conflicts
- Testing changes across different branches simultaneously
- Avoiding stash/switch cycles when context-switching
- Keeping long-running builds isolated from development work

**Benefits:**
- No need to stash changes when switching context
- Parallel work without repository duplication
- Shared Git database (efficient disk usage)
- Each worktree has independent working directory state

**See:** Part VII of [github-native-operating-model.md](github-native-operating-model.md) for detailed implementation in multi-agent scenarios.

---

## Safety & Governance

### Commands to AVOID (Unless Explicitly Required)

**Force Push:**
```bash
git push --force  # ❌ Dangerous
```

**Direct Commits to Protected Branches:**
```bash
# ❌ If on main branch, create feature branch instead
git switch -c feature/<topic>  # ✓ Correct approach
```

**Destructive History Rewrites:**
```bash
git reset --hard   # ❌ Use with caution
git rebase         # ❌ Only on unpushed commits
```

### Pre-Commit Inspection Workflow

**Always run before committing:**
```bash
git status        # What's staged?
git diff          # What changed (unstaged)?
git diff --staged # What will be committed?
git log --oneline # Where am I in history?
```

### Verify Current Branch

```bash
git branch --show-current
```

**Or:**
```bash
git status  # Shows current branch in first line
```

**Best Practice:** Always verify you're on the correct branch before making commits.

---

## Command Comparison: Old vs Modern Syntax

| Task | Legacy Syntax (Avoid) | Modern Syntax (2025) |
|------|----------------------|---------------------|
| Create & switch to branch | `git checkout -b <branch>` | `git switch -c <branch>` |
| Switch to existing branch | `git checkout <branch>` | `git switch <branch>` |
| Restore file from commit | `git checkout -- <file>` | `git restore <file>` |
| Unstage file | `git reset HEAD <file>` | `git restore --staged <file>` |

**Rationale:** Git 2.23 (2019) split `checkout` into specialized commands for clarity:
- `git switch` → Branch operations
- `git restore` → File operations

---

## Quick Reference Card

### Most Common Workflow

```bash
# 1. Start new work
git switch -c feature/123-new-feature

# 2. Make changes, then stage
git add .

# 3. Verify before commit
git status
git diff --staged

# 4. Commit with good message
git commit -m "Add feature X to improve Y"

# 5. Push to remote
git push -u origin feature/123-new-feature

# 6. Open Pull Request on GitHub
# (via web interface or gh CLI)

# 7. After PR merge, switch back and clean up
git switch main
git pull
git branch -d feature/123-new-feature
```

---

## Additional Resources

- **Official Git Documentation:** https://git-scm.com/docs
- **Git Switch Command:** https://git-scm.com/docs/git-switch
- **GitHub Flow:** https://docs.github.com/en/get-started/using-github/github-flow
- **Branching Workflow Standard:** [branching-workflow-standard.md](branching-workflow-standard.md)
- **Operating Model:** [github-native-operating-model.md](github-native-operating-model.md)

---

## Version History

- **v1.0.0** (2025-01-16): Initial reference guide with modern Git 2.23+ syntax and GitHub best practices
