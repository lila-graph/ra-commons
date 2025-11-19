# Testing & Debugging with Claude Code

This guide describes testing and debugging workflows using Claude Code, aligned with the BMAD Loop (Build-Measure-Analyze-Decide) from Part VIII of the [GitHub-Native Operating Model](../github-native-operating-model.md#part-viii--cicd-as-a-bmad-loop).

---

## Table of Contents

- [Test-Driven Development with Claude Code](#test-driven-development-with-claude-code)
- [Debugging Workflow](#debugging-workflow)
- [Extended Thinking Modes](#extended-thinking-modes)
- [Subagent Brainstorming](#subagent-brainstorming)
- [BMAD Loop Integration](#bmad-loop-integration)
- [Documentation Testing](#documentation-testing)

---

## Test-Driven Development with Claude Code

### TDD Pattern

**Classic TDD Cycle:**
1. Write failing test
2. Implement minimum code to pass
3. Refactor with passing tests

**With Claude Code:**

```
Implement user authentication using TDD:

1. Write test for successful login
2. Implement minimum code to pass
3. Write test for invalid credentials
4. Implement password validation
5. Write test for account lockout
6. Implement lockout logic
7. Refactor for clarity

Run tests after each step. Stop if any test fails.

Think.
```

### Example: Adding a New Feature with Tests

```
I need to add email validation to the user registration form.

Following TDD:
1. Write test: valid email passes validation
2. Write test: invalid email fails validation
3. Write test: empty email fails validation
4. Implement email validation function
5. Integrate with registration form
6. Run all tests

Use @src/auth.py and @tests/test_auth.py for context.

Think.
```

**Claude will:**
- Write comprehensive tests first
- Implement minimal code to pass
- Run tests incrementally
- Show pass/fail for each test
- Refactor when all tests pass

---

## Debugging Workflow

### Test-Driven Debugging Pattern

**From DeepLearning.AI Course and CLAUDE.md:**

```
When encountering an error:
1. Write tests to evaluate the failing component
2. Write tests for related components
3. Run tests to identify specific failures
4. Propose fixes based on test evidence

Use "think" mode for complex debugging.
```

### Example: Debugging an Authentication Error

```
The application returns "Authentication failed" for valid credentials.

Debug using test-driven approach:
1. Write test to reproduce the error
2. Write tests for token validation
3. Write tests for password hashing
4. Write tests for database queries
5. Run all tests and identify which component fails
6. Propose fix based on failing test

Use @src/auth.py, @src/db.py, and @tests/ for context.

Think hard.
```

**Expected Output:**

```
✓ Test 1: User login with valid credentials - FAIL
  Expected: 200 OK
  Actual: 401 Unauthorized

✓ Test 2: Token validation - PASS

✓ Test 3: Password hashing - FAIL
  Expected: bcrypt hash verified
  Actual: Hash mismatch

✓ Test 4: Database query - PASS

Analysis:
The password hashing function is using SHA-256 instead of bcrypt.
The database stores bcrypt hashes, but the comparison uses SHA-256.

Proposed Fix:
Update src/auth.py line 42:
- hash = hashlib.sha256(password.encode()).hexdigest()
+ hash = bcrypt.hashpw(password.encode(), salt)
```

### Incremental Debugging

For complex bugs, use incremental approach:

```
Step 1: Isolate the problem
```

```
Create minimal reproduction of the auth failure.
Use only @src/auth.py and mock dependencies.

Think.
```

```
Step 2: Write comprehensive tests
```

```
Write tests covering all code paths in @src/auth.py:
- Success case
- Invalid credentials
- Missing credentials
- Expired token
- Database error

Think.
```

```
Step 3: Run tests and analyze
```

```
Run all auth tests. For each failure:
1. Show expected vs actual
2. Show relevant code
3. Explain why it fails

Think.
```

```
Step 4: Propose targeted fixes
```

```
Based on test failures, propose minimal fixes to:
1. Fix failing tests
2. Maintain passing tests
3. Improve code clarity

Think.
```

---

## Extended Thinking Modes

### When to Use Extended Thinking

From CLAUDE.md and DeepLearning.AI course:

| Mode | Use Case | Example |
|------|----------|---------|
| **Standard** | Straightforward tasks | "Add logging to this function" |
| **think** | Architectural decisions | "Refactor auth module. Think." |
| **think hard** | High ambiguity | "Design caching strategy. Think hard." |
| **think harder** | Complex changes | "Migrate to microservices. Think harder." |
| **ultrathink** | Critical decisions | "Redesign database schema. Ultrathink." |

### Alignment with Risk & Ambiguity Matrix

From Part VI of the operating model:

| Task Type | Risk | Ambiguity | Thinking Mode |
|-----------|------|-----------|---------------|
| Well-Defined Refactor | Low | Low | Standard |
| New Greenfield Feature | Low | High | think / think hard |
| Security/Auth Change | High | Low | think |
| Production Bug Fix | High | High | think hard / think harder |

### Example: Complex Refactoring

```
Refactor the authentication system to support OAuth2, SAML, and local auth.

Requirements:
- Maintain backward compatibility
- Support multiple providers
- Abstract provider-specific logic
- Comprehensive tests

This is a complex architectural change.

Think harder.
```

**Expected Behavior:**
- Claude allocates more "thinking budget"
- Explores multiple approaches
- Considers edge cases
- Proposes detailed plan before implementing
- Breaks down into phases

---

## Subagent Brainstorming

### Parallel Brainstorming for Design Decisions

From DeepLearning.AI course pattern:

```
Use two parallel subagents to brainstorm approaches for implementing real-time notifications.

Each subagent should propose:
1. Architecture design
2. Technology stack
3. Scalability considerations
4. Implementation complexity
5. Pros and cons

Do not implement any code yet. Present both approaches for human decision.
```

**Output:**

```
Agent 1 Proposal: WebSocket-Based
- Architecture: Dedicated WebSocket server
- Stack: Socket.io + Redis
- Scalability: Horizontal scaling with sticky sessions
- Complexity: Medium
- Pros: Real-time, bidirectional
- Cons: Requires persistent connections

Agent 2 Proposal: Server-Sent Events (SSE)
- Architecture: Built into existing API server
- Stack: Native SSE + PostgreSQL LISTEN/NOTIFY
- Scalability: Leverages existing infrastructure
- Complexity: Low
- Pros: Simpler, HTTP-based
- Cons: Unidirectional only

Recommendation:
For this use case (notifications only), SSE is sufficient and simpler.
If bidirectional communication is needed later, migrate to WebSocket.
```

### Subagents for Test Strategy

```
Use three parallel subagents to propose test strategies for the refactored auth module.

Each agent should focus on different testing aspect:
1. Unit testing strategy
2. Integration testing strategy
3. End-to-end testing strategy

Provide test examples for each approach. Do not implement yet.
```

---

## BMAD Loop Integration

### BUILD: Write Tests as Part of Development

From Part VIII:

> **BUILD:** Standard CI job. Compile code, run unit tests, build container.

**With Claude Code:**

```
Implement feature X and write comprehensive tests:

1. Unit tests for individual functions
2. Integration tests for module interactions
3. Contract tests for API endpoints (if applicable)

Ensure 90%+ code coverage.

Think.
```

### MEASURE: Run Tests and Collect Metrics

```
Run all tests and show:
1. Pass/fail summary
2. Code coverage percentage
3. Performance benchmarks (if applicable)
4. Any failing tests with details

Output results in JSON format for CI/CD integration.
```

**Expected Output:**

```json
{
  "summary": {
    "total": 156,
    "passed": 154,
    "failed": 2,
    "skipped": 0
  },
  "coverage": {
    "line": 92.3,
    "branch": 87.1,
    "function": 95.2
  },
  "failures": [
    {
      "test": "test_expired_token_rejected",
      "error": "AssertionError: Expected 401, got 200",
      "file": "tests/test_auth.py",
      "line": 145
    },
    {
      "test": "test_rate_limit_enforced",
      "error": "AssertionError: Expected rate limit after 5 attempts",
      "file": "tests/test_security.py",
      "line": 89
    }
  ]
}
```

### ANALYZE: Interpret Results

```
Analyze the test results from the previous run:

1. Summarize findings (coverage drop, new failures)
2. Identify root causes of failures
3. Assess impact on system
4. Recommend priority for fixes

Think.
```

**Expected Output:**

```
Analysis:

Coverage Drop:
- Line coverage decreased from 95% to 92.3% (-2.7%)
- New code in auth.py lines 145-162 not fully tested

Test Failures:
1. test_expired_token_rejected (HIGH PRIORITY)
   - Root cause: Token expiration check commented out during refactor
   - Impact: Security vulnerability - expired tokens accepted
   - Fix: Uncomment expiration check at auth.py:156

2. test_rate_limit_enforced (MEDIUM PRIORITY)
   - Root cause: Rate limiter reset logic incorrect
   - Impact: Rate limiting not working, DoS risk
   - Fix: Update rate_limiter.py:42 to use sliding window

Recommendation:
Fix test_expired_token_rejected immediately (security issue).
Address rate limit in next sprint.
Add integration test for token expiration flow.
```

### DECIDE: Auto-Create Tech Debt Issues

From Part VIII:

> "The workflow also checks the Analyze job's output. If it produced a tech-debt.json artifact (e.g., test coverage was low), the workflow *automatically creates a new issue*..."

**Simulation with Claude Code:**

```
Based on test analysis, create GitHub issues for:
1. Security: Expired token vulnerability
2. Tech debt: Improve test coverage for auth module
3. Enhancement: Add rate limit integration tests

Use issue templates and link to relevant code.
```

---

## Documentation Testing

### Validate Markdown

```
Test all documentation in @docs/:
1. Verify markdown syntax is valid
2. Check all internal links resolve
3. Ensure code examples are runnable
4. Verify mermaid diagrams compile

Report any issues found.
```

### Test Code Examples

```
Extract all code examples from @docs/api/authentication.md and:
1. Create test file for each example
2. Run examples to verify they work
3. Report any examples that fail

Think.
```

---

## Best Practices

### 1. Always Use "Think" for Debugging

```
# Bad
Fix the login error

# Good
The login returns 401 for valid credentials.

Write tests to identify the failing component.
Propose fix based on test evidence.

Think.
```

### 2. Request Comprehensive Tests

```
# Bad
Add tests for the auth module

# Good
Add comprehensive tests for @src/auth.py:
- Happy path (valid credentials)
- Edge cases (empty input, SQL injection attempts)
- Error conditions (network timeout, database offline)
- Security scenarios (expired token, brute force)

Aim for 95%+ coverage.

Think.
```

### 3. Incremental Testing

```
# Bad
Implement entire feature and test at end

# Good
Implement JWT auth incrementally:
1. Add token generation + test
2. Add token validation + test
3. Add refresh logic + test
4. Add expiration + test

Run tests after each step.
```

### 4. Use Subagents for Complex Decisions

```
# When uncertain about approach
Use two subagents to propose test strategies for the new caching layer.
Do not implement yet.
```

---

## Quick Reference

### Test-Driven Debugging

```
Error: X happens when Y.

Write tests to identify failing component.
Run tests.
Propose fix based on evidence.

Think.
```

### Extended Thinking Triggers

```
think       # Architectural decision
think hard  # High ambiguity task
think harder # Complex refactoring
ultrathink  # Critical system change
```

### Subagent Brainstorming

```
Use N parallel subagents to brainstorm approaches for X.
Do not implement code yet.
```

### BMAD Workflow

```
1. Build: Implement + write tests
2. Measure: Run tests + collect metrics
3. Analyze: Interpret results + identify issues
4. Decide: Propose fixes or create issues
```

---

## Additional Resources

- **BMAD Loop (Part VIII):** [Operating Model](../github-native-operating-model.md#part-viii--cicd-as-a-bmad-loop)
- **Risk & Ambiguity Matrix (Part VI):** [Operating Model](../github-native-operating-model.md#2-the-risk--ambiguity-routing-matrix)
- **Claude Code Best Practices:** https://www.anthropic.com/engineering/claude-code-best-practices
- **DeepLearning.AI Course:** https://github.com/https-deeplearning-ai/sc-claude-code-files

---

**Version:** 1.0.0
**Last Updated:** 2025-01-16
**Maintained By:** GitHub-Native Operating Model Contributors
