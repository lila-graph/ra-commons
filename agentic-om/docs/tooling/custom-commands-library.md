# Custom Commands Library

This guide explains how to create and use custom slash commands in Claude Code, aligned with the GitHub-Native Operating Model workflows.

**Purpose:** Custom commands enforce workflow patterns, reduce repetition, and ensure consistency across AI agent interactions.

---

## Table of Contents

- [What Are Custom Commands?](#what-are-custom-commands)
- [Directory Structure](#directory-structure)
- [Command Syntax](#command-syntax)
- [Example Commands](#example-commands)
- [Best Practices](#best-practices)

---

## What Are Custom Commands?

### Overview

Custom commands are predefined prompts stored in `.claude/commands/` that can be invoked with `/command-name`.

**Benefits:**
- Enforce Spec-Driven Development workflow
- Ensure PR template compliance
- Standardize testing patterns
- Reduce prompt variation across agents
- Embed governance rules into development flow

### Alignment with Operating Model

From Part VI (Specification Layer):

> "All work must begin with an approved spec and plan."

Custom commands can enforce this by requiring spec/plan approval before implementation.

---

## Directory Structure

```
.claude/
└── commands/
    ├── implement-feature.md
    ├── create-pr.md
    ├── run-tests.md
    ├── refactor-with-tests.md
    ├── debug-error.md
    └── update-docs.md
```

**Note:** `.claude/commands/` is version-controlled and shared across the team.

---

## Command Syntax

### Basic Structure

```markdown
# Short description for command listing

Detailed instructions for Claude Code.

$ARGUMENTS  <!-- User-provided arguments -->

IMPORTANT:
- Key constraints
- Workflow requirements
- Governance rules
```

### Using $ARGUMENTS

`$ARGUMENTS` is replaced with user input when command is invoked.

**Example:**

**.claude/commands/implement-feature.md:**
```markdown
Implement the following feature:

$ARGUMENTS

Follow Spec-Driven Development workflow.
```

**Usage:**
```
/implement-feature Add JWT token validation to auth service
```

**Claude receives:**
```
Implement the following feature:

Add JWT token validation to auth service

Follow Spec-Driven Development workflow.
```

---

## Example Commands

### 1. /implement-feature

**Purpose:** Enforce Spec Kit workflow (Constitution → Spec → Plan → Tasks → Implementation)

**File:** `.claude/commands/implement-feature.md`

```markdown
# Implement a feature following Spec-Driven Development

You will be implementing a new feature following the Spec-Driven Development workflow.

Feature to implement:

$ARGUMENTS

IMPORTANT:
1. Verify that constitution.md exists in @docs/specs/ or project root
2. Verify that a spec.md file exists for this feature
3. Verify that plan.md has been reviewed and approved by a human
4. If tasks.md doesn't exist, create it by breaking down the plan
5. Implement following the approved plan
6. Write tests for all new functionality
7. Update documentation in @docs/
8. Do NOT deviate from the approved plan without human consultation

Workflow:
1. Read @docs/specs/constitution.md
2. Read feature spec (find appropriate spec.md file)
3. Read approved plan (plan.md)
4. Create or update tasks.md
5. Implement incrementally, checking off tasks
6. Write tests
7. Update docs

Use "think" mode for this architectural work.

Think.
```

**Usage:**
```
/implement-feature JWT token validation for API authentication
```

---

### 2. /create-pr

**Purpose:** Ensure PR follows template and links to specs/issues

**File:** `.claude/commands/create-pr.md`

```markdown
# Create a Pull Request following the repository template

Create a Pull Request for:

$ARGUMENTS

IMPORTANT:
1. Use the PR template structure from CLAUDE.md
2. Link to the original issue or spec
3. Include Plan-SHA if following Spec Kit workflow
4. Ensure all files are staged and committed
5. Push branch to remote before creating PR

PR Template Structure:
## Summary
- <1-3 bullets describing the change>

## Context
- <why this change exists>
- <link to issue/spec>

## Implementation Details
- <design choices made>
- <Plan-SHA: if applicable>

## Testing
- <what tests were added/modified>
- <how to validate the change>

## Risks & Rollback
- <potential impact>
- <how to revert if needed>

Steps:
1. Verify all changes are committed
2. Push branch to remote with: git push -u origin <branch-name>
3. Use `gh pr create` with template
4. Link to related issues/specs

Do NOT create PR without:
- Proper commit messages
- Tests for new functionality
- Updated documentation
```

**Usage:**
```
/create-pr JWT authentication feature
```

---

### 3. /run-tests

**Purpose:** Execute BMAD Measure phase during development

**File:** `.claude/commands/run-tests.md`

```markdown
# Run tests and provide analysis (BMAD Loop - Measure phase)

Run tests for:

$ARGUMENTS

IMPORTANT:
1. Run ALL relevant tests (unit, integration, e2e if applicable)
2. Collect coverage metrics
3. Report failures with specific details
4. Propose fixes for failures
5. Do NOT proceed if critical tests fail

Test Execution:
1. Identify test framework (pytest, jest, etc.)
2. Run tests with coverage: `pytest --cov=src tests/`
3. Collect results
4. Analyze failures

Output Format:
- Total tests: X
- Passed: Y
- Failed: Z
- Coverage: N%

For each failure:
- Test name
- Expected vs Actual
- Root cause analysis
- Proposed fix

Use "think" mode for analyzing complex test failures.

Think.
```

**Usage:**
```
/run-tests authentication module
```

---

### 4. /refactor-with-tests

**Purpose:** Enforce TDD during refactoring

**File:** `.claude/commands/refactor-with-tests.md`

```markdown
# Refactor code using Test-Driven Development

Refactor the following code:

$ARGUMENTS

IMPORTANT:
1. Write characterization tests FIRST (document current behavior)
2. Ensure all tests pass before refactoring
3. Refactor incrementally
4. Run tests after each small change
5. Do NOT change behavior (tests should still pass)
6. Update tests only if behavior intentionally changes

TDD Refactoring Workflow:
1. Identify code to refactor
2. Write tests for current behavior
3. Verify all tests pass (baseline)
4. Make small refactoring change
5. Run tests (should still pass)
6. Repeat steps 4-5 until refactoring complete
7. Review final code for clarity

Test Coverage Goal: 95%+

Use "think" mode for architectural refactoring decisions.

Think.
```

**Usage:**
```
/refactor-with-tests src/auth.py authentication logic
```

---

### 5. /debug-error

**Purpose:** Enforce test-driven debugging pattern

**File:** `.claude/commands/debug-error.md`

```markdown
# Debug an error using test-driven approach

Debug the following error:

$ARGUMENTS

IMPORTANT:
1. Do NOT guess at fixes
2. Write tests to reproduce the error
3. Write tests for related components
4. Identify failing component through tests
5. Propose fix based on test evidence
6. Verify fix with tests

Test-Driven Debugging Workflow:
1. Write test that reproduces the error
2. Verify test fails with the reported error
3. Write tests for suspected components
4. Run all tests
5. Analyze which components fail
6. Identify root cause
7. Propose minimal fix
8. Verify all tests pass after fix

Use "think hard" mode for complex debugging scenarios.

Think hard.
```

**Usage:**
```
/debug-error Authentication returns 401 for valid credentials
```

---

### 6. /update-docs

**Purpose:** Ensure documentation stays in sync with code changes

**File:** `.claude/commands/update-docs.md`

```markdown
# Update documentation after code changes

Update documentation for:

$ARGUMENTS

IMPORTANT:
1. Review ALL code changes in current branch
2. Identify docs that need updates
3. Update API documentation if interfaces changed
4. Update architecture docs if structure changed
5. Update examples if behavior changed
6. Test all code examples in documentation
7. Verify all internal links still work

Documentation Areas to Check:
- @docs/api/ - API reference documentation
- @docs/architecture/ - System architecture docs
- @README.md - Project overview
- @CHANGELOG.md - Change log (if applicable)
- Code comments - Inline documentation

Workflow:
1. Run: git diff main..HEAD
2. Identify changed files
3. For each changed file, find related docs
4. Update docs to reflect changes
5. Test code examples
6. Verify links
7. Commit doc updates to same branch

Do NOT:
- Skip updating related docs
- Leave broken links
- Include outdated examples
```

**Usage:**
```
/update-docs JWT authentication changes
```

---

## Best Practices

### 1. Make Commands Atomic

Each command should do ONE thing well:

✅ Good:
- `/implement-feature`
- `/create-pr`
- `/run-tests`

❌ Bad:
- `/implement-feature-and-create-pr-and-run-tests`

### 2. Embed Governance Rules

Commands should enforce operating model principles:

```markdown
IMPORTANT:
1. Verify spec.md exists (Principle #3: Specification is the contract)
2. Do NOT bypass PR requirements (Principle #1: Every contribution is a PR)
3. Human approval required for high-risk changes (Principle #4: Ambiguity requires human judgment)
```

### 3. Use Extended Thinking Appropriately

Include thinking guidance in commands:

```markdown
Use "think" mode for architectural decisions.
Think.
```

```markdown
Use "think hard" for high-ambiguity refactoring.
Think hard.
```

### 4. Provide Clear Output Format

Specify expected output structure:

```markdown
Output Format:
- Summary: <1-2 sentences>
- Changes Made: <bullet list>
- Tests Added: <bullet list>
- Next Steps: <what remains to be done>
```

### 5. Link to Operating Model

Reference relevant parts of the operating model:

```markdown
This command implements Part VI (Specification Layer) of the operating model.
See @docs/github-native-operating-model.md#part-vi
```

---

## Creating Your Own Commands

### Step 1: Identify Repetitive Workflow

Look for prompts you use frequently:
- "Implement feature X following spec-driven development"
- "Create PR with proper template"
- "Debug error Y using tests"

### Step 2: Create Command File

```bash
# Create .claude/commands/ if it doesn't exist
mkdir -p .claude/commands

# Create command file
touch .claude/commands/my-command.md
```

### Step 3: Write Command Content

```markdown
# One-line description

Detailed instructions for Claude Code.

User input:

$ARGUMENTS

IMPORTANT:
- Key constraints
- Workflow requirements

Workflow steps...

Use appropriate thinking mode if needed.
```

### Step 4: Test Command

```bash
# Launch Claude Code
claude code

# Test your command
/my-command Test argument
```

### Step 5: Commit to Repository

```bash
git add .claude/commands/my-command.md
git commit -m "feat: Add /my-command custom command"
git push
```

Now the command is available to all team members!

---

## Command Library Summary

| Command | Purpose | Enforces |
|---------|---------|----------|
| `/implement-feature` | Spec-driven implementation | Part VI (Spec Kit workflow) |
| `/create-pr` | Compliant PR creation | Part I (PR-first principle) |
| `/run-tests` | BMAD Measure phase | Part VIII (BMAD Loop) |
| `/refactor-with-tests` | TDD refactoring | Testing best practices |
| `/debug-error` | Test-driven debugging | Scientific debugging approach |
| `/update-docs` | Doc synchronization | Part VII (Doc in repo principle) |

---

## Additional Resources

- **Spec Kit Documentation:** https://github.com/github/spec-kit
- **Operating Model (Part VI):** [Specification Layer](../github-native-operating-model.md#part-vi--specification-layer-spec-kit--constitution)
- **Claude Code Custom Commands:** https://docs.anthropic.com/en/docs/claude-code/custom-commands
- **DeepLearning.AI Example:** https://github.com/https-deeplearning-ai/sc-claude-code-files/blob/main/.claude/commands/implement-feature.md

---

**Version:** 1.0.0
**Last Updated:** 2025-01-16
**Maintained By:** GitHub-Native Operating Model Contributors
