# MCP Server Workflow for AI Agents

This document describes the complete workflow for requesting, testing, approving, and deploying Model Context Protocol (MCP) servers within the GitHub-Native Operating Model.

**Context:** This workflow implements the MCP Registry governance described in Part IV of the [GitHub-Native Operating Model](../github-native-operating-model.md#3-github-as-the-factory-floor).

---

## Table of Contents

- [Overview](#overview)
- [MCP Registry Governance](#mcp-registry-governance)
- [Developer Request Process](#developer-request-process)
- [Local Testing](#local-testing)
- [Approval Workflow](#approval-workflow)
- [Deployment](#deployment)
- [Agent Usage](#agent-usage)
- [Security Considerations](#security-considerations)

---

## Overview

### What is MCP?

**Model Context Protocol (MCP)** is a standard for connecting AI models to external tools and data sources. MCP servers provide capabilities like:
- Web browsing (Playwright)
- Time/date utilities
- Database access
- API integrations
- File system operations
- Custom business logic

### Why Governance?

From Part IV of the operating model:

> "The organization will host its *own* internal, private MCP registry. This registry is the *runtime governance plane for AI agent capabilities*. To make a new tool available (e.g., a 'deploy-to-staging' tool), a human must approve a PR to the registry. This 'allow list' is the explicit governance step, preventing agents from using un-vetted tools."

**Key Principle:** No agent can use a tool unless it's been human-approved and added to the registry.

---

## MCP Registry Governance

### Registry Structure

The MCP registry is a git repository containing:

```
mcp-registry/
├── README.md
├── servers/
│   ├── playwright.json
│   ├── time.json
│   ├── database-reader.json
│   └── custom-deploy.json
├── docker/
│   ├── playwright/
│   │   └── Dockerfile
│   └── custom-deploy/
│       └── Dockerfile
└── .github/
    └── workflows/
        └── publish-to-ghcr.yml
```

### Server Metadata Format

Each `servers/*.json` file contains:

```json
{
  "name": "playwright",
  "version": "1.0.0",
  "description": "Browser automation for testing web applications",
  "command": "npx @playwright/mcp@latest",
  "docker_image": "ghcr.io/your-org/mcp-playwright:1.0.0",
  "capabilities": [
    "browser_navigate",
    "browser_snapshot",
    "browser_click",
    "browser_type"
  ],
  "security_review": {
    "reviewed_by": "security-team",
    "reviewed_date": "2025-01-15",
    "risk_level": "medium",
    "notes": "Requires network access. Sandboxed browser environment."
  },
  "approved_by": "team.org.owners",
  "approved_date": "2025-01-16"
}
```

---

## Developer Request Process

### Step 1: Create Issue

**Who:** Human developer or team lead
**Where:** Main repository or dedicated mcp-registry repository

**Use the MCP Server Request issue template:**

```markdown
**MCP Server Name:** playwright

**Purpose:**
Enable AI agents to test web applications through browser automation.

**Capabilities Requested:**
- Navigate to URLs
- Take screenshots
- Click elements
- Fill forms
- Run JavaScript

**Justification:**
Our QA workflow requires automated testing of the frontend. Playwright MCP
server allows AI agents to write and execute browser tests.

**Security Considerations:**
- Requires network access
- Runs in isolated browser context
- Does not access file system directly
- Logs all navigation events

**Proposed Usage:**
AI agents will use this for:
1. Writing end-to-end tests
2. Debugging UI issues
3. Validating accessibility

**Testing Plan:**
1. Test on localhost only
2. Verify sandbox isolation
3. Check resource limits
4. Review audit logs
```

See [.github/ISSUE_TEMPLATE/mcp-server-request.md](../../.github/ISSUE_TEMPLATE/mcp-server-request.md) for full template.

### Step 2: Initial Review

**Who:** team.human.seniors
**Action:** Review request for:
- Business justification
- Security implications
- Alternative solutions
- Resource requirements

**Outcome:**
- ✅ Approve for local testing
- ❌ Reject with explanation
- 🤔 Request more information

---

## Local Testing

### Step 3: Developer Testing

**Who:** Requesting developer
**Where:** Local development environment

#### A. Install MCP Server Locally

```bash
# Using Claude Code CLI
claude mcp add playwright npx @playwright/mcp@latest
```

#### B. Configure Permissions

**Edit `.claude/settings.local.json`:**

```json
{
  "permissions": {
    "allow": [
      "mcp__playwright__browser_navigate",
      "mcp__playwright__browser_snapshot",
      "mcp__playwright__browser_click",
      "mcp__playwright__browser_type"
    ]
  },
  "enableAllProjectMcpServers": true
}
```

**Note:** `.claude/settings.local.json` is gitignored and developer-specific.

#### C. Test Capabilities

**Launch Claude Code:**
```bash
claude code
```

**Test MCP server:**
```
/mcp playwright
```

**Verify tools are available:**
```
Using playwright MCP, navigate to http://localhost:8000 and take a screenshot
```

**Expected output:**
```
✓ Navigated to http://localhost:8000
✓ Screenshot saved to page-screenshot.png
```

#### D. Document Test Results

Create `mcp-testing-notes.md`:

```markdown
# Playwright MCP Server Testing

## Test Date: 2025-01-16

### Tests Performed
1. ✅ Navigate to URL
2. ✅ Take screenshot
3. ✅ Click button
4. ✅ Fill form
5. ✅ Execute JavaScript

### Issues Found
- None

### Resource Usage
- Memory: ~150MB
- CPU: <5%
- Network: Localhost only

### Security Observations
- Runs in isolated browser context
- No file system access
- All actions logged

### Recommendation
✅ Ready for production approval
```

---

## Approval Workflow

### Step 4: Open Pull Request to MCP Registry

**Who:** Developer
**Action:** Create PR to `mcp-registry` repository

```bash
# Clone mcp-registry repo
git clone https://github.com/your-org/mcp-registry.git
cd mcp-registry

# Create branch
git switch -c feature/add-playwright-mcp

# Add server metadata
cat > servers/playwright.json <<EOF
{
  "name": "playwright",
  "version": "1.0.0",
  ...
}
EOF

# If custom Docker image needed, add Dockerfile
mkdir -p docker/playwright
# (Add Dockerfile)

# Commit and push
git add servers/playwright.json
git commit -m "feat: Add Playwright MCP server"
git push -u origin feature/add-playwright-mcp

# Open PR
gh pr create --title "Add Playwright MCP Server" \
  --body "Resolves #123. See testing notes in issue."
```

### Step 5: Senior Review

**Who:** team.human.seniors
**Action:** Review PR for:

**Technical Review:**
- Server metadata complete
- Capabilities well-defined
- Testing notes thorough
- Documentation provided

**Security Review:**
- Risk level assessed
- Security notes documented
- Sandbox/isolation verified
- Audit logging enabled

**Governance Review:**
- Aligns with operating model
- Doesn't bypass controls
- Proper access controls defined

### Step 6: Owners Approval

**Who:** team.org.owners
**Action:** Final approval

From Part IV:

> "To make a new tool available (e.g., a 'deploy-to-staging' tool), a human must approve a PR to the registry. This 'allow list' is the explicit governance step, preventing agents from using un-vetted tools."

**Approval criteria:**
- ✅ Technical review passed
- ✅ Security review passed
- ✅ Governance review passed
- ✅ At least 2 owners approve

### Step 7: Merge to Registry

**Who:** Owner with merge permissions
**Action:** Merge PR to `main` branch of `mcp-registry` repository

```bash
gh pr merge <PR-number> --squash
```

**Result:** MCP server is now in the approved registry.

---

## Deployment

### Step 8: Publish to GitHub Container Registry (ghcr.io)

**Automated via GitHub Actions:**

When PR is merged, `.github/workflows/publish-to-ghcr.yml` triggers:

```yaml
name: Publish MCP Server to ghcr.io

on:
  push:
    branches: [main]
    paths:
      - 'servers/*.json'
      - 'docker/**'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build and push Docker images
        run: |
          for server in docker/*; do
            SERVER_NAME=$(basename $server)
            docker build -t ghcr.io/${{ github.repository_owner }}/mcp-${SERVER_NAME}:latest $server
            docker push ghcr.io/${{ github.repository_owner }}/mcp-${SERVER_NAME}:latest
          done
```

**Result:**
- Docker images published to `ghcr.io/your-org/mcp-playwright:latest`
- Available for deployment

### Step 9: Update Global MCP Configuration

**Who:** Platform team
**Action:** Update organization-wide MCP configuration

**Edit `.mcp.json` in template repository:**

```json
{
  "mcpServers": {
    "playwright": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "ghcr.io/your-org/mcp-playwright:latest"
      ]
    },
    "time": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "ghcr.io/your-org/mcp-time:latest"
      ]
    }
  }
}
```

**Commit and push:**
```bash
git add .mcp.json
git commit -m "feat: Add playwright MCP server to global config"
git push origin main
```

---

## Agent Usage

### Step 10: AI Agents Access New Tool

**Automatic:** Once in registry and deployed, agents can use the tool.

**Example (Claude Code):**

```
/mcp
```

**Output:**
```
Connected MCP Servers:
- time
- sequential-thinking
- Context7
- playwright (newly added)
```

**Usage:**
```
Using playwright MCP, test the login flow at http://localhost:8000/login
```

**Agent executes:**
1. Navigate to login page
2. Fill username field
3. Fill password field
4. Click "Login" button
5. Verify redirect to dashboard
6. Take screenshot of dashboard
7. Report results

---

## Security Considerations

### Principle of Least Privilege

**From Part IV (RBAC Matrix):**

| Team | MCP Server Access |
|------|-------------------|
| team.org.owners | All servers (approval authority) |
| team.human.seniors | All servers (review authority) |
| team.human.engineers | Approved servers only |
| team.ai.developers | Approved servers only (cannot add new) |
| team.ai.evaluators | Read-only servers only |

### Security Checklist

Before approving an MCP server:

- [ ] **Sandboxing:** Server runs in isolated environment
- [ ] **Access Control:** Server respects GitHub RBAC
- [ ] **Audit Logging:** All actions are logged
- [ ] **Resource Limits:** CPU/memory limits enforced
- [ ] **Network Restrictions:** Only necessary network access
- [ ] **Secret Management:** No hardcoded credentials
- [ ] **Input Validation:** Server validates all inputs
- [ ] **Error Handling:** Fails safely without exposing internals

### Security Review Template

```markdown
## Security Review: [MCP Server Name]

**Reviewer:** [Name]
**Date:** [YYYY-MM-DD]

### Risk Assessment
**Overall Risk Level:** [Low/Medium/High]

### Security Controls
- [ ] Runs in Docker container (isolation)
- [ ] No privileged access required
- [ ] Network access limited to [specify]
- [ ] File system access limited to [specify]
- [ ] Credentials managed via secrets management
- [ ] Input validation implemented
- [ ] Output sanitization implemented
- [ ] Rate limiting configured
- [ ] Audit logging enabled

### Identified Risks
1. [Risk description]
   - Mitigation: [How addressed]

### Approval
[ ] Approved for production use
[ ] Requires changes (see comments)
[ ] Rejected (see justification)
```

---

## Troubleshooting

### Agent Can't Access MCP Server

**Problem:** Agent reports "Tool not available"

**Solution:**
```bash
# 1. Check if server is in registry
cat mcp-registry/servers/playwright.json

# 2. Check if server is in .mcp.json
cat .mcp.json | grep playwright

# 3. Check if server is running
docker ps | grep mcp-playwright

# 4. Check agent permissions
# Verify .claude/settings.local.json includes server permissions
```

### MCP Server Request Denied

**Problem:** PR to mcp-registry rejected

**Common reasons:**
- Insufficient justification
- Security concerns not addressed
- Alternative solutions exist
- Capability overlaps with existing server

**Solution:**
- Address reviewer feedback
- Provide more detailed testing notes
- Enhance security documentation
- Clarify unique value proposition

### Docker Image Build Fails

**Problem:** GitHub Action fails to build/publish image

**Solution:**
```bash
# Test build locally
cd mcp-registry/docker/playwright
docker build -t test-playwright .

# Check logs
docker logs <container-id>

# Verify Dockerfile syntax
```

---

## Best Practices

### 1. Start with Read-Only Servers

For initial MCP adoption, prioritize read-only capabilities:
- Documentation fetchers
- Code analyzers
- Log readers

### 2. Require Explicit Justification

Every MCP server request must answer:
- Why is this needed?
- What alternatives were considered?
- What risks does this introduce?
- How will usage be monitored?

### 3. Test Thoroughly Before Approval

Require comprehensive testing:
- Happy path scenarios
- Error conditions
- Resource limits
- Security boundaries

### 4. Version MCP Servers

Use semantic versioning:
```json
{
  "name": "playwright",
  "version": "1.2.0",
  ...
}
```

This allows rollback if issues arise.

### 5. Monitor Usage

Track MCP server usage via audit logs:
- Which agents use which tools
- Frequency of use
- Error rates
- Resource consumption

### 6. Regular Security Reviews

Conduct quarterly reviews of:
- All approved MCP servers
- Usage patterns
- Security incidents
- New vulnerabilities

---

## Integration with Operating Model

### Part IV: MCP Registry

This workflow implements the MCP Registry concept:

> "The organization will host its *own* internal, private MCP registry. This registry is the *runtime governance plane for AI agent capabilities*."

### Part V: Project Board Integration

MCP server requests should appear on the organization-level GitHub Project:

- **Work-Item-Type:** Infrastructure
- **Epic-Link:** Platform-Capabilities
- **Assignee-Type:** Human
- **Risk:** (Based on security review)

### Part VIII: BMAD Loop

MCP servers should include quality metrics:

- **Build:** Docker image builds successfully
- **Measure:** Usage metrics, error rates
- **Analyze:** Security scan results
- **Decide:** Approve, require changes, or sunset server

---

## Additional Resources

- **MCP Official Site:** https://modelcontextprotocol.io
- **GitHub MCP Registry:** https://github.com/modelcontextprotocol/registry
- **Operating Model (Part IV):** [Organizational Operating Model](../github-native-operating-model.md#part-iv--organizational-operating-model)
- **Claude Code MCP Guide:** https://docs.anthropic.com/en/docs/claude-code/mcp
- **GitHub Container Registry:** https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry

---

## Quick Reference

### Request Workflow

1. **Create Issue** (MCP Server Request template)
2. **Local Testing** (`.claude/settings.local.json`)
3. **PR to Registry** (`mcp-registry` repo)
4. **Senior Review** (technical, security, governance)
5. **Owner Approval** (final sign-off)
6. **Merge to main** (registry updated)
7. **Auto-deploy** (GitHub Actions → ghcr.io)
8. **Agent Access** (available in `/mcp` list)

### Key Files

- **Registry:** `mcp-registry/servers/*.json`
- **Local Config:** `.claude/settings.local.json` (gitignored)
- **Global Config:** `.mcp.json` (version controlled)
- **Issue Template:** `.github/ISSUE_TEMPLATE/mcp-server-request.md`

---

**Version:** 1.0.0
**Last Updated:** 2025-01-16
**Maintained By:** GitHub-Native Operating Model Contributors
