# ra-commons Quick Reference

Command reference for common operations with the ra-commons framework.

## Running Orchestrators

```bash
# Architecture analysis
python -m ra_orchestrators.architecture_orchestrator "Project Name"

# UX design workflow
python -m ra_orchestrators.ux_orchestrator "Project Name"

# With timeout for long-running analyses (30 minutes)
timeout 1800 python -m ra_orchestrators.architecture_orchestrator "Project Name"
```

## Development Setup

```bash
# Install dependencies (using uv)
uv sync

# Activate virtual environment
source .venv/bin/activate

# Install dependencies (using pip)
pip install -e .
```

## Agent Management

```bash
# List available agents
python -c "
from ra_agents.registry import AgentRegistry
registry = AgentRegistry()
print(registry.discover_agents())
"

# List agents for specific domain
python -c "
from ra_agents.registry import AgentRegistry
registry = AgentRegistry()
print(registry.discover_agents(domain='ux'))
"

# Load specific agent
python -c "
from ra_agents.registry import AgentRegistry
registry = AgentRegistry()
agent = registry.load_agent('analyzer', domain='architecture')
print(agent)
"
```

## Testing and Validation

```bash
# Run orchestrator with specific project
python -m ra_orchestrators.architecture_orchestrator "MyProject"

# Verify outputs
ls -lh ra_output/architecture_*/

# Check specific phase outputs
ls -lh ra_output/architecture_*/docs/
ls -lh ra_output/architecture_*/diagrams/
```

## MCP Server Discovery

```python
from ra_tools.mcp_registry import MCPRegistry

registry = MCPRegistry()
available_servers = registry.discover_servers()
print(f"Found {len(available_servers)} MCP servers")

# Check specific MCP server
if 'figma' in available_servers:
    print("Figma MCP server is available")
```

## Figma Integration

```bash
# Set environment variable
export FIGMA_ACCESS_TOKEN="your_token"
```

```python
from ra_tools.figma_integration import FigmaIntegration

figma = FigmaIntegration()
if figma.is_available():
    design_data = await figma.get_file(file_key)
```

## SpecKit Workflow Commands

```bash
# Create feature specification
/speckit.specify "feature description here"

# Clarify underspecified areas
/speckit.clarify

# Generate technical implementation plan
/speckit.plan

# Generate task breakdown
/speckit.tasks

# Convert tasks to GitHub issues
/speckit.taskstoissues

# Analyze cross-artifact consistency
/speckit.analyze

# Generate custom checklist
/speckit.checklist "domain requirements"

# Update project constitution
/speckit.constitution

# Execute implementation from tasks
/speckit.implement
```

**Typical workflow:**
```bash
/speckit.specify "Add user authentication"
/speckit.clarify  # optional
/speckit.plan
/speckit.tasks
/speckit.implement
```

## Creating a New Orchestrator

```bash
# Create orchestrator directory
mkdir -p src/ra_orchestrators

# Create agent definitions directory
mkdir -p src/ra_agents/custom

# Run new orchestrator
python -m ra_orchestrators.custom_orchestrator
```

## Git Workflow

```bash
# Create feature branch
git switch -c feature/<short-tag>-<description>

# Stage and commit changes
git add .
git commit -m "Description of changes"

# Push to remote
git push -u origin feature/<branch-name>

# Create pull request (using gh CLI)
gh pr create --title "Feature: Description" --body "PR details"
```

## Troubleshooting

```bash
# Fix import errors - run from repository root
cd $(git rev-parse --show-toplevel)
python -m ra_orchestrators.architecture_orchestrator

# Check Python environment
which python
python --version

# Verify dependencies
pip list | grep claude-agent-sdk

# Check output directory
ls -la ra_output/
```

## File Paths Reference

| Path | Description |
|------|-------------|
| `src/ra_orchestrators/` | Domain orchestrators |
| `src/ra_agents/` | Agent definitions (JSON) |
| `src/ra_tools/` | Tool integrations |
| `ra_output/` | Analysis outputs (timestamped) |
| `.specify/templates/` | SpecKit templates |
| `.specify/memory/` | Project constitution |
| `.claude/commands/` | Slash command definitions |

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `FIGMA_ACCESS_TOKEN` | Figma API access | `figd_xxxxx` |
| `ANTHROPIC_API_KEY` | Claude API access | `sk-ant-xxxxx` |

## Output Structure

```
ra_output/
└── {domain}_{YYYYMMDD_HHMMSS}/
    ├── docs/           # Documentation outputs
    ├── diagrams/       # Mermaid diagrams
    └── README.md       # Synthesis report
```

## Additional Resources

- **Framework docs:** `src/ra_orchestrators/README.md`
- **Tutorial:** `docs/tutorial-new-orchestrator.md`
- **Contributing:** `CONTRIBUTING.md`
- **SpecKit templates:** `.specify/templates/`
