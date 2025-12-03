# ra-commons

**Portable, drop-in framework for comprehensive repository analysis across multiple domains**

ra-commons provides reusable orchestrators, agents, and tools for analyzing codebases with specialized multi-agent workflows. Originally designed for architecture analysis, it now supports UX design workflows and can be extended to new domains in less than a day.

## Why Migrate to ra-commons?

If you've been using copied RA functionality in your repositories, migrating to ra-commons provides:

- **Single Source of Truth** - Updates and improvements automatically available across all projects
- **No Code Duplication** - Framework updates don't require manual synchronization
- **Collision-Free** - Uses `ra_` prefix to avoid naming conflicts with existing code
- **Timestamped Outputs** - Each analysis run creates `ra_output/{domain}_{timestamp}/` preserving history
- **Extensibility** - Add new analysis domains without modifying core framework
- **Community Improvements** - Benefit from shared agent definitions and orchestrator enhancements

## Quick Start

### Installation

Choose your preferred integration method:

**Option 1: Git Submodule (Recommended)**
```bash
cd /path/to/your/project
git submodule add https://github.com/your-org/ra-commons
echo "ra_output/" >> .gitignore
```

**Option 2: Direct Clone**
```bash
cd /path/to/your/project
git clone https://github.com/your-org/ra-commons
echo "ra_output/" >> .gitignore
```

**Option 3: Development Setup**
```bash
# Clone and install dependencies
git clone https://github.com/your-org/ra-commons
cd ra-commons

# Using uv (recommended)
uv sync
source .venv/bin/activate

# Using pip
pip install -e .
```

### Running Your First Analysis

**Architecture Analysis** (5 phases):
```bash
python -m ra_orchestrators.architecture_orchestrator "MyProject"
```

Output generated in `ra_output/architecture_{timestamp}/`:
- Component inventory (modules, classes, functions)
- Architecture diagrams (Mermaid visualizations)
- Data flow analysis
- API documentation
- Comprehensive synthesis

**UX Design Workflow** (6 phases):
```bash
python -m ra_orchestrators.ux_orchestrator "MyProject"
```

Output generated in `ra_output/ux_{timestamp}/`:
- User research (personas, journeys, competitive analysis)
- Information architecture (sitemaps, navigation)
- Visual design specifications
- Interactive prototypes
- API contracts
- Design system documentation

## Key Features

### Three-Layer Architecture

1. **Orchestrators** - Coordinate multi-phase analysis workflows
   - Inherit from `BaseOrchestrator`
   - Define domain-specific phases and execution flow
   - Manage timestamped output directories

2. **Agents** - Specialized analysis agents (JSON-defined)
   - Loaded dynamically via `AgentRegistry`
   - Single-responsibility design
   - Domain-specific or shared across domains

3. **Tools** - External service integrations
   - MCP server discovery and management
   - API integrations (Figma, etc.)
   - Graceful fallback when tools unavailable

### Design Principles

- **Portability** - Drop into any repository without modification
- **Timestamped Outputs** - Preserve analysis history without overwrites
- **Extensibility** - Add new domains in <1 day
- **Reusability** - Share agents and tools across domains

## Migration Guide

### From Copied RA Code to ra-commons

If your repository currently has RA functionality copied directly:

1. **Backup existing outputs**
   ```bash
   mv ra_output ra_output.backup
   ```

2. **Remove copied RA code**
   ```bash
   # Remove the old copied files
   rm -rf src/ra_orchestrators src/ra_agents src/ra_tools
   ```

3. **Install ra-commons** (choose your method above)

4. **Run analysis from your project**
   ```bash
   cd /path/to/your/project
   python -m ra_orchestrators.architecture_orchestrator "ProjectName"
   ```

5. **Compare outputs**
   ```bash
   # Compare new output with backup
   diff -r ra_output.backup ra_output/architecture_*/
   ```

### Configuration

No configuration required! The framework:
- Auto-discovers agents in `src/ra_agents/{domain}/`
- Creates timestamped output directories automatically
- Uses `ra_` prefix to prevent naming collisions
- Works from any repository root

### Optional: MCP Tool Integration

For enhanced capabilities, configure MCP servers:

**Figma Integration**
```bash
export FIGMA_ACCESS_TOKEN="your_token"
```

**MCP Server Discovery**
```python
from ra_tools.mcp_registry import MCPRegistry

registry = MCPRegistry()
servers = registry.discover_servers()
```

## Repository Structure

```
ra-commons/
├── src/
│   ├── ra_orchestrators/        # Domain orchestrators
│   │   ├── base_orchestrator.py         # Core framework
│   │   ├── architecture_orchestrator.py # Architecture analysis
│   │   └── ux_orchestrator.py           # UX/UI design workflow
│   ├── ra_agents/               # Agent definitions (JSON)
│   │   ├── architecture/        # Architecture analysis agents
│   │   └── ux/                  # UX design agents
│   └── ra_tools/                # Tool integrations
│       ├── mcp_registry.py      # MCP server discovery
│       └── figma_integration.py # Figma MCP + REST API
├── docs/
│   ├── quick-reference.md       # Command cheat sheet
│   └── tutorial-new-orchestrator.md  # Adding new domains
├── .specify/                    # SpecKit workflow templates
└── CLAUDE.md                    # AI-specific instructions
```

## Common Use Cases

### Analyze Existing Project Architecture

```bash
cd /path/to/existing/project
python -m ra_orchestrators.architecture_orchestrator "ExistingProject"

# View outputs
ls -lh ra_output/architecture_*/
cat ra_output/architecture_*/README.md
```

### Run UX Design Workflow for New Feature

```bash
python -m ra_orchestrators.ux_orchestrator "NewFeature"

# Review design outputs
cat ra_output/ux_*/01_user_research.md
cat ra_output/ux_*/04_interactive_prototypes.md
```

### Long-Running Analysis (with timeout)

```bash
# 30-minute timeout for large codebases
timeout 1800 python -m ra_orchestrators.architecture_orchestrator "LargeProject"
```

### List Available Agents

```bash
python -c "
from ra_agents.registry import AgentRegistry
registry = AgentRegistry()
print(registry.discover_agents())
"
```

## Extending ra-commons

### Adding a New Domain Orchestrator

Target: Implement new domain in **<1 day**

**Quick Steps:**

1. Create orchestrator inheriting from `BaseOrchestrator`
2. Implement required methods: `get_agent_definitions()`, `get_allowed_tools()`, `run()`
3. Create agent JSON files in `src/ra_agents/{domain}/`
4. Test: `python -m ra_orchestrators.custom_orchestrator`

**Example:**

```python
from ra_orchestrators.base_orchestrator import BaseOrchestrator

class SecurityOrchestrator(BaseOrchestrator):
    def __init__(self, project_name: str):
        super().__init__(project_name, domain="security")

    def get_agent_definitions(self):
        # Define security analysis agents
        pass

    def get_allowed_tools(self):
        return ["Read", "Write", "Glob", "Grep"]

    def run(self):
        # Define security analysis phases
        pass
```

See `docs/tutorial-new-orchestrator.md` for complete step-by-step guide.

### Agent Design Best Practices

1. **Single Responsibility** - Each agent has one clear purpose
2. **Explicit Tools** - Only include tools the agent needs
3. **File Writing Mandate** - Agents must use Write tool, not just describe output
4. **Clear Prompts** - Include examples and edge cases

## Documentation

### Framework Core
- [`CLAUDE.md`](./CLAUDE.md) - Complete project overview and AI instructions
- [`src/ra_orchestrators/README.md`](./src/ra_orchestrators/README.md) - Orchestrator API reference
- [`src/ra_orchestrators/base_orchestrator.py`](./src/ra_orchestrators/base_orchestrator.py) - Core implementation

### Tutorials and Guides
- [`docs/quick-reference.md`](./docs/quick-reference.md) - Command cheat sheet
- [`docs/tutorial-new-orchestrator.md`](./docs/tutorial-new-orchestrator.md) - Adding new orchestrators
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) - Development workflow

### SpecKit Workflow
- [`.specify/templates/`](./.specify/templates/) - Spec, plan, task, and checklist templates
- [`.claude/commands/`](./.claude/commands/) - Slash command definitions

## Troubleshooting

### Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'ra_orchestrators'
# Solution: Run from repository root
cd $(git rev-parse --show-toplevel)
python -m ra_orchestrators.architecture_orchestrator "Project"
```

### Agent Not Writing Files

Ensure agent prompt includes:
```
IMPORTANT: When asked to write to a file, ALWAYS use the Write tool
to create the actual file. Do not just describe what you would write.
```

### MCP Tools Not Available

Check Claude Code MCP server configuration:
- Figma MCP Server
- Sequential Thinking
- Playwright (browser automation)

See `src/ra_tools/` for integration examples.

## Contributing

We welcome contributions! This repository follows trunk-based development:

- All work on short-lived feature branches (`feature/`, `bugfix/`, `refactor/`, `docs/`)
- All changes require pull requests
- See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for complete guidelines

## License

[Your License Here]

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: See [`CLAUDE.md`](./CLAUDE.md) for comprehensive documentation
- **Examples**: Reference implementations in `src/ra_orchestrators/`

---

**Built for portability. Designed for extensibility. Ready to drop into your repository.**
