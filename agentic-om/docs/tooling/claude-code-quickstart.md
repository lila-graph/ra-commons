# Claude Code Quick Start Guide

This guide provides essential commands and workflows for using Claude Code with the GitHub-Native Operating Model.

**Audience:** Developers (human and AI) working within repositories that follow the [GitHub-Native Operating Model](../github-native-operating-model.md).

---

## Table of Contents

- [Installation & Setup](#installation--setup)
- [Essential Commands](#essential-commands)
- [Context Management](#context-management)
- [Workflow Integration](#workflow-integration)
- [MCP Server Management](#mcp-server-management)
- [Mode Switching](#mode-switching)
- [Common Workflows](#common-workflows)
- [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Installation & Setup

### Prerequisites

1. **Claude Code CLI**
   ```bash
   # Install via npm
   npm install -g @anthropic-ai/claude-code

   # Or download from https://claude.com/code
   ```

2. **GitHub CLI** (for PR creation and management)
   ```bash
   # Install gh CLI
   # macOS
   brew install gh

   # Ubuntu/Debian
   sudo apt install gh

   # Windows
   winget install GitHub.cli

   # Authenticate
   gh auth login
   ```

3. **Git** (version 2.23+ for modern commands)
   ```bash
   # Verify version
   git --version
   # Should show 2.23 or higher for git switch support
   ```

### First-Time Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/your-repo.git
   cd your-repo
   ```

2. **Launch Claude Code**
   ```bash
   claude code
   ```

3. **Initialize CLAUDE.md** (if not already present)
   ```
   /init
   ```

   This scans the codebase and generates or updates `CLAUDE.md` with project-specific guidance.

4. **Review CLAUDE.md**
   ```
   @CLAUDE.md
   ```

   Familiarize yourself with project-specific rules, conventions, and constraints.

---

## Essential Commands

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/init` | Generate/regenerate CLAUDE.md | `/init` |
| `/clear` | Clear conversation history | `/clear` |
| `/compact` | Summarize conversation to save context | `/compact` |
| `/mcp` | View MCP servers and tools | `/mcp` |
| `/help` | Show available commands | `/help` |
| `exit` | Exit Claude Code | `exit` or `Ctrl+D` |

### Context Commands

| Command | Description | Example |
|---------|-------------|---------|
| `@<file>` | Reference file in prompt | `@src/auth.py` |
| `@<folder>` | Reference all files in folder | `@docs/` |
| `#<instruction>` | Add quick memory/rule | `#use git switch not git checkout` |
| `ESC` | Interrupt Claude | Press `ESC` |
| `ESC ESC` | Rewind conversation | Press `ESC` twice |

### Bash Integration

| Command | Description | Example |
|---------|-------------|---------|
| `!<command>` | Run bash command | `!git status` |
| Regular command | Execute directly | `git status` (without `!`) |

**Note:** Prefer using Claude Code's built-in tools (Read, Edit, Write, Grep, Glob) over bash commands for file operations.

---

## Context Management

### Adding Files to Context

**Single file:**
```
@src/auth.py - Review this authentication module
```

**Multiple files:**
```
Review @src/auth.py and @tests/test_auth.py for consistency
```

**Entire directory:**
```
@docs/ - Analyze all documentation
```

**Pattern matching:**
```
@src/**/*.py - Review all Python files in src
```

### Quick Memory Addition

Use `#` to add rules without editing CLAUDE.md:

```
#always use type hints in Python functions
```

```
#this project uses poetry for dependency management
```

```
#API keys are stored in .env file, never commit them
```

**These memories persist for the current session and can be made permanent by adding them to CLAUDE.md.**

### Clearing Context

When conversation becomes too long or off-track:

```
/clear
```

**Warning:** This removes all conversation history. Use `/compact` to summarize instead.

### Compacting Context

Preserve important context while reducing token usage:

```
/compact
```

Claude will summarize the conversation and retain key decisions.

---

## Workflow Integration

### Standard Development Flow

1. **Start on main branch**
   ```bash
   git switch main
   git pull origin main
   ```

2. **Create feature branch** (via Claude Code)
   ```
   Create a new feature branch for implementing JWT authentication
   ```

   Claude will execute:
   ```bash
   git switch -c feature/123-jwt-auth
   ```

3. **Implement feature** (via Claude Code)
   ```
   Implement JWT token validation following the spec in @docs/specs/auth-spec.md

   Think.
   ```

4. **Run tests**
   ```
   Run all tests and show results
   ```

5. **Create Pull Request**
   ```
   Create a PR for this JWT authentication feature. Title: "feat: Add JWT token validation"
   ```

   Claude will:
   - Stage changes
   - Commit with proper message
   - Push to remote
   - Open PR using `gh` CLI with proper template

### Git Worktrees for Parallel Work

**Create multiple worktrees:**
```
Set up git worktrees for parallel development:
1. Feature 123 - JWT auth
2. Feature 456 - UI dashboard
3. Bugfix 789 - Login timeout

Use .trees/ directory convention.
```

**See [git-worktrees-practical-guide.md](git-worktrees-practical-guide.md) for detailed workflow.**

---

## MCP Server Management

### View Connected MCP Servers

```
/mcp
```

**Example output:**
```
Connected MCP Servers:
- time (mcp-server-time)
- sequential-thinking
- Context7
- ai-docs-server
- playwright

Use /mcp <server-name> to see tools provided by a specific server.
```

### View Server Tools

```
/mcp playwright
```

**Example output:**
```
Playwright MCP Server Tools:
- browser_navigate
- browser_snapshot
- browser_click
- browser_type
...
```

### Adding MCP Servers

**For administrators:**
```bash
# Add server globally
claude mcp add playwright npx @playwright/mcp@latest

# Add server to project
# Edit .claude/settings.local.json
```

**For developers (request new server):**

Create an issue using the MCP Server Request template. See [mcp-server-workflow.md](mcp-server-workflow.md) for process.

---

## Mode Switching

### Planning Mode vs Auto-Accept Mode

**Toggle modes:**
```
Shift + Tab
```

**Planning Mode** (Recommended for this repository)
- Claude proposes changes
- You review before execution
- Safer for governance-focused workflows
- Aligns with PR-first model

**Auto-Accept Mode**
- Changes execute immediately
- Faster iteration
- Use with caution
- Best for rapid prototyping

**Current Mode Indicator:**
Look for `[Planning]` or `[Auto-Accept]` in the status line.

### Extended Thinking Modes

For complex tasks, use graduated thinking levels:

| Command | Use Case | Example |
|---------|----------|---------|
| `think` | Architectural decisions | `Refactor the auth module. Think.` |
| `think hard` | High ambiguity | `Design a new caching strategy. Think hard.` |
| `think harder` | Complex changes | `Migrate from REST to GraphQL. Think harder.` |
| `ultrathink` | Critical decisions | `Redesign database schema. Ultrathink.` |

**Alignment:** Maps to Risk & Ambiguity Routing Matrix (Part VI of operating model).

---

## Common Workflows

### 1. Understanding an Existing Codebase

```
Explain the architecture of this application. Focus on:
1. Entry point and main flow
2. Database schema
3. API endpoints
4. Authentication mechanism

Use @src/ and @docs/ for context.

Think.
```

### 2. Adding a New Feature (Spec-Driven)

```
I need to add user profile management. Here's the spec: @docs/specs/user-profile-spec.md

Following Spec-Driven Development:
1. Review the spec
2. Create a plan
3. Break into tasks
4. Implement incrementally

Think hard.
```

### 3. Debugging an Error

```
The application returns "Authentication failed" for valid credentials.

1. Write tests to evaluate the auth module
2. Write tests for token validation
3. Run tests and identify failures
4. Propose fixes based on evidence

Think.
```

### 4. Refactoring Code

```
Refactor @src/legacy_auth.py to follow modern patterns:
1. Use type hints
2. Extract functions (single responsibility)
3. Add unit tests
4. Update documentation

Ensure all existing tests pass.

Think.
```

### 5. Creating Documentation

```
Create documentation for the authentication module in @src/auth.py

Include:
1. Overview and purpose
2. API reference
3. Usage examples
4. Security considerations

Output to docs/api/authentication.md
```

### 6. Running Tests

```
Run all unit tests and show:
1. Pass/fail summary
2. Coverage percentage
3. Any failing tests with details

If failures exist, propose fixes.
```

### 7. Creating a Pull Request

```
Create a PR for the JWT authentication feature:
- Title: "feat: Add JWT token validation"
- Use PR template structure
- Link to issue #123
- Include testing plan
```

---

## Keyboard Shortcuts

### macOS

| Shortcut | Action |
|----------|--------|
| `Shift + Tab` | Toggle planning/auto-accept mode |
| `ESC` | Interrupt Claude |
| `ESC ESC` | Rewind conversation |
| `Cmd + Shift + Ctrl + 4` | Take screenshot |
| `Ctrl + V` | Paste screenshot |
| `Ctrl + D` | Exit Claude Code |

### Windows

| Shortcut | Action |
|----------|--------|
| `Shift + Tab` | Toggle planning/auto-accept mode |
| `ESC` | Interrupt Claude |
| `ESC ESC` | Rewind conversation |
| `Win + Shift + S` | Take screenshot |
| `Ctrl + V` | Paste screenshot |
| `Ctrl + D` | Exit Claude Code |

### Linux

| Shortcut | Action |
|----------|--------|
| `Shift + Tab` | Toggle planning/auto-accept mode |
| `ESC` | Interrupt Claude |
| `ESC ESC` | Rewind conversation |
| `Ctrl + V` | Paste screenshot (varies by distribution) |
| `Ctrl + D` | Exit Claude Code |

---

## Best Practices

### 1. Start with Planning Mode

Always begin work in planning mode to review changes before execution:
```
Shift + Tab  # Ensure [Planning] mode is active
```

### 2. Use Extended Thinking for Complex Tasks

Don't hesitate to use `think` modes:
```
Redesign the authentication system to support OAuth2. Think harder.
```

### 3. Reference Files Explicitly

Use `@` notation for clarity:
```
@src/auth.py - Add multi-factor authentication support
```

### 4. Leverage CLAUDE.md

Add project-specific rules:
```
#this project requires all functions to have docstrings
#database migrations must include rollback SQL
#never commit .env files
```

### 5. Commit Frequently

Ask Claude to commit incremental progress:
```
Commit the changes we just made with message: "Add JWT validation middleware"
```

### 6. Review Diffs Before Committing

Always review changes:
```
Show me a diff of all changes before we commit
```

### 7. Use Subagents for Brainstorming

For complex decisions:
```
Use two parallel subagents to brainstorm approaches for implementing real-time notifications. Do not implement code yet.
```

---

## Troubleshooting

### Problem: Claude suggests outdated git commands

**Solution:**
```
#always use git switch -c instead of git checkout -b
```

Add to CLAUDE.md's `important-instruction-reminders` section.

### Problem: Context window full

**Solution:**
```
/compact
```

Or start a new session:
```
/clear
```

### Problem: Claude can't access a file

**Solution:**
```
# Explicitly reference the file
@path/to/file.py - Review this file

# Or check if file exists
!ls path/to/file.py
```

### Problem: MCP tool not available

**Solution:**
```
/mcp  # Check if server is connected

# If missing, request via MCP Server Request issue template
```

### Problem: Claude making unwanted changes

**Solution:**
```
ESC  # Interrupt immediately

# Then clarify:
Please only modify src/auth.py, do not touch other files.
```

---

## Additional Resources

- **Claude Code Documentation:** https://docs.anthropic.com/en/docs/claude-code/overview
- **Common Workflows:** https://docs.anthropic.com/en/docs/claude-code/common-workflows
- **Best Practices:** https://www.anthropic.com/engineering/claude-code-best-practices
- **Operating Model:** [github-native-operating-model.md](../github-native-operating-model.md)
- **Git Commands Reference:** [git-commands-reference.md](git-commands-reference.md)
- **Git Worktrees Guide:** [git-worktrees-practical-guide.md](git-worktrees-practical-guide.md)
- **Testing Guide:** [testing-with-claude-code.md](testing-with-claude-code.md)
- **MCP Workflow:** [mcp-server-workflow.md](mcp-server-workflow.md)
- **Custom Commands:** [custom-commands-library.md](custom-commands-library.md)

---

## Quick Reference Card

### Most Common Commands

```bash
# Start Claude Code
claude code

# Initialize project
/init

# Reference files
@src/auth.py

# Add memory
#use modern git commands

# Clear history
/clear

# Compact context
/compact

# View MCP servers
/mcp

# Toggle mode
Shift + Tab

# Interrupt
ESC

# Rewind
ESC ESC

# Exit
exit
```

### Common Prompts

```
# Understand codebase
Explain the architecture. Use @src/ and @docs/. Think.

# Implement feature
Implement X following @docs/specs/X-spec.md. Think.

# Debug error
Error: Y. Write tests, run tests, propose fixes. Think.

# Create PR
Create PR for feature X. Use template. Link issue #123.

# Setup worktrees
Create worktrees for features A, B, C in .trees/ directory.
```

---

**Version:** 1.0.0
**Last Updated:** 2025-01-16
**Maintained By:** GitHub-Native Operating Model Contributors
