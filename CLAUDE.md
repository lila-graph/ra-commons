# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ra-commons** is a portable, drop-in framework for comprehensive repository analysis across multiple domains. It provides reusable orchestrators, agents, and tools for analyzing codebases with specialized multi-agent workflows.

**Key Design Principles:**
- **Portability** - Drop into any repository without modification (uses `ra_` prefix to avoid collisions)
- **Timestamped Outputs** - Each run creates `ra_output/{domain}_{YYYYMMDD_HHMMSS}/` to preserve analysis history
- **Extensibility** - Base framework supports adding new domains in <1 day
- **Reusability** - Agents and tools shared across domains

## Repository Structure

```
src/
├── ra_orchestrators/        # Domain orchestrators
│   ├── base_orchestrator.py         # Core framework
│   ├── architecture_orchestrator.py # Architecture analysis
│   ├── ux_orchestrator.py           # UX/UI design workflow
│   └── architecture.py              # Legacy orchestrator
├── ra_agents/              # Agent definitions (JSON)
│   ├── architecture/       # Architecture analysis agents
│   └── ux/                 # UX design agents
├── ra_tools/               # Tool integrations
│   ├── mcp_registry.py     # MCP server discovery
│   └── figma_integration.py # Figma MCP + REST API
└── ra_output/              # Analysis outputs (timestamped)

dot-cursor/rules/           # Cursor AI rules for development workflow
dot-github/                 # GitHub templates
agentic-om-docs/           # Documentation about agentic workflows
```

## Common Commands

### Running Orchestrators

```bash
# Architecture analysis (generates ra_output/architecture_{timestamp}/)
# Runs 5 phases: Component Inventory, Architecture Diagrams, Data Flows, API Docs, Synthesis
python -m ra_orchestrators.architecture_orchestrator "Project Name"

# UX design workflow (generates ra_output/ux_{timestamp}/)
# Runs 6 phases: Research, IA, Design, Prototypes, API Contracts, Design System
python -m ra_orchestrators.ux_orchestrator "Project Name"

# With timeout for long-running analyses (30 minutes)
timeout 1800 python -m ra_orchestrators.architecture_orchestrator "Project Name"
```

### Development Setup

```bash
# Install dependencies (using uv)
uv sync

# Activate virtual environment
source .venv/bin/activate

# Install dependencies (using pip)
pip install -e .
```

### Agent Management

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
```

### Testing and Validation

```bash
# Run orchestrator with specific project
python -m ra_orchestrators.architecture_orchestrator "MyProject"

# Verify outputs
ls -lh ra_output/architecture_*/
```

### SpecKit Workflow Commands

This repository includes SpecKit slash commands for feature specification and planning workflow.

**Quick workflow:** `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`

**All commands:** See `.claude/commands/speckit.*.md` for complete command documentation
**Command reference:** See `docs/quick-reference.md` for usage examples
**Templates:** See `.specify/templates/` for spec, plan, task, and checklist templates

## Architecture Patterns

### Three-Layer Architecture

1. **Orchestrators** (`ra_orchestrators/`) - Coordinate multi-phase analysis workflows
   - Inherit from `BaseOrchestrator`
   - Define agents, tools, and phase execution
   - Manage output directory structure

2. **Agents** (`ra_agents/`) - Specialized analysis agents defined in JSON
   - Loaded dynamically via `AgentRegistry`
   - Domain-specific or shared across domains
   - Include name, description, prompt, tools, model

3. **Tools** (`ra_tools/`) - External service integrations
   - MCP server discovery and management
   - API integrations (Figma, etc.)
   - Fallback handling when tools unavailable

### Base Orchestrator Pattern

All orchestrators inherit from `BaseOrchestrator` - see `src/ra_orchestrators/base_orchestrator.py` for complete implementation.

**Key Methods to Implement:**
- `get_agent_definitions()` - Return dict of AgentDefinition objects
- `get_allowed_tools()` - Return list of allowed tool names
- `run()` - Define the phase-based workflow

**Provided Helper Methods:**
- `execute_phase(phase_name, agent_name, prompt, client)` - Execute a workflow phase
- `display_phase_header(phase_number, phase_name, emoji)` - Display phase header
- `verify_outputs(expected_files)` - Verify expected files were created
- `run_with_client()` - Entry point with client lifecycle management

**Complete tutorial:** See `docs/tutorial-new-orchestrator.md` for step-by-step guide with full code examples.

### Agent Definition Pattern

Agents are defined in JSON files at `src/ra_agents/{domain}/{agent_name}.json`.

**Example:** See `src/ra_agents/architecture/analyzer.json` for complete structure.

**Loading agents:**
```python
from ra_agents.registry import AgentRegistry

registry = AgentRegistry()
agent = registry.load_agent("agent_name", domain="custom")
```

**Agent design best practices:** Single responsibility, explicit tools, clear prompts with file-writing mandate.

### Timestamped Output Pattern

The framework creates timestamped directories automatically (see `BaseOrchestrator.__init__`):
- **Format**: `ra_output/{domain}_{YYYYMMDD_HHMMSS}/`
- **Example**: `ra_output/architecture_20251119_122754/`
- **Benefit**: Multiple analyses don't overwrite each other

To disable timestamps: `orchestrator = CustomOrchestrator(use_timestamp=False)`

## Workflow Execution Details

### Architecture Orchestrator Phases

Executes 5 sequential phases:

1. **Component Inventory** - Catalog modules, classes, and functions (excludes `ra_*` framework)
2. **Architecture Diagrams** - Generate Mermaid visualizations of system structure
3. **Data Flow Analysis** - Document information flows and API communication
4. **API Documentation** - Extract and document public interfaces
5. **Final Synthesis** - Create comprehensive README with all findings

**Implementation details:** See `src/ra_orchestrators/architecture_orchestrator.py`
**Output structure:** `ra_output/architecture_{timestamp}/` with `docs/` and `diagrams/` subdirectories

### UX Orchestrator Phases

Executes 6 sequential phases:

1. **User Research** - Personas, user journeys, competitive analysis
2. **Information Architecture** - Sitemaps, navigation, content organization
3. **Visual Design** - Design specs, component library, branding
4. **Interactive Prototypes** - Clickable prototypes, user flows
5. **API Contracts** - Frontend/backend contracts, data schemas
6. **Design System** - Component documentation, usage guidelines

**Implementation details:** See `src/ra_orchestrators/ux_orchestrator.py`

### Cross-Orchestrator Communication

The framework includes a `CrossOrchestratorCommunication` mixin for future cross-domain validation:

```python
# Future capability: UX orchestrator validates with Architecture orchestrator
ux_orchestrator.invoke_orchestrator(
    orchestrator_name="architecture",
    phase_name="validate_api_contracts",
    context={"api_spec": api_data}
)
```

**Note:** This is a future capability for validating consistency across different domain analyses.

## Adding a New Domain Orchestrator

**Target:** Implement new domain in <1 day

**High-level steps:**
1. Create orchestrator class inheriting from `BaseOrchestrator`
2. Implement required methods: `get_agent_definitions()`, `get_allowed_tools()`, `run()`
3. Create agent JSON definitions in `src/ra_agents/{domain}/`
4. Run and test: `python -m ra_orchestrators.custom_orchestrator`

**Complete step-by-step tutorial:** See `docs/tutorial-new-orchestrator.md` for full code examples, best practices, and troubleshooting.

**Reference implementations:**
- `src/ra_orchestrators/architecture_orchestrator.py` - 5-phase architecture analysis
- `src/ra_orchestrators/ux_orchestrator.py` - 6-phase UX design workflow

## Development Workflow

This repository follows trunk-based development with PR-first workflow.

**Key requirements:**
- All work on short-lived feature branches (`feature/`, `bugfix/`, `refactor/`, `docs/`)
- Never commit directly to main (except trivial changes with user approval)
- All changes require pull requests with complete descriptions
- AI agents: Include reasoning, implementation details, validation steps in PRs

**Complete workflow guide:** See `CONTRIBUTING.md` for branch naming, PR templates, code standards, testing requirements, and AI-specific guidelines.

## Tool Integration

### MCP Server Discovery

```python
from ra_tools.mcp_registry import MCPRegistry

registry = MCPRegistry()
available_servers = registry.discover_servers()
print(f"Found {len(available_servers)} MCP servers")
```

### Figma Integration

Set environment variable:
```bash
export FIGMA_ACCESS_TOKEN="your_token"
```

In orchestrator (src/ra_tools/figma_integration.py):
```python
from ra_tools.figma_integration import FigmaIntegration

figma = FigmaIntegration()
if figma.is_available():
    design_data = await figma.get_file(file_key)
```

### SpecKit Configuration

SpecKit templates and scripts are in `.specify/` directory.

**Key directories:**
- `.specify/templates/` - Spec, plan, task, and checklist templates
- `.specify/memory/constitution.md` - Project principles and constraints
- `.specify/scripts/bash/` - Automation scripts for feature workflow

**Key principles:** Technology-agnostic specs, measurable success criteria, max 3 clarifications per spec

**Full documentation:** See `.specify/memory/constitution.md` and `.claude/commands/speckit.*.md`

## Best Practices

### Agent Design
1. **Single Responsibility** - Each agent has one clear purpose
2. **Explicit Tools** - Only include tools the agent needs
3. **File Writing Mandate** - Agents MUST use Write tool, not describe output
4. **Clear Prompts** - Include examples and edge cases in prompts

### Orchestrator Design
1. **Phase Independence** - Phases should be self-contained
2. **Output Verification** - Always verify expected files were created using `verify_outputs()`
3. **Progress Visibility** - Use `show_tool_details=True` for transparency
4. **Error Recovery** - Handle failures gracefully, preserve partial results

### Output Quality
1. **Structured Markdown** - Consistent heading levels and formatting
2. **Mermaid Diagrams** - Visualize architecture and flows
3. **Source References** - Link to files with line numbers (e.g., `file.py:123`)
4. **Examples** - Include code examples and usage patterns

## Troubleshooting

### Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'ra_orchestrators'
# Solution: Run from repository root
cd $(git rev-parse --show-toplevel)
python -m ra_orchestrators.architecture_orchestrator
```

### Agent Not Writing Files
Ensure agent prompt includes:
```
IMPORTANT: When asked to write to a file, ALWAYS use the Write tool
to create the actual file. Do not just describe what you would write.
```

### MCP Tools Not Available
Check Claude Code MCP server configuration for:
- Figma MCP Server
- Sequential Thinking
- Playwright (browser automation)

See `src/ra_tools/` for integration examples.

## Distribution Model

This framework is designed to be distributed as a standalone repository and dropped into target repositories for analysis. The `ra_` prefix prevents naming collisions with existing code.

### Installation in Target Repository

```bash
# Option 1: Git submodule
cd /path/to/target/repo
git submodule add https://github.com/org/ra-commons

# Option 2: Direct clone
cd /path/to/target/repo
git clone https://github.com/org/ra-commons

# Add to .gitignore
echo "ra_output/" >> .gitignore
```

### Running Analysis

```bash
cd /path/to/target/repo
python -m ra_orchestrators.architecture_orchestrator "TargetProject"
```

## Related Documentation

### Framework Core
- `src/ra_orchestrators/README.md` - Detailed orchestrator usage guide and API reference
- `src/ra_orchestrators/CLAUDE.md` - Framework-specific AI instructions
- `src/ra_orchestrators/base_orchestrator.py` - Core implementation
- `src/ra_orchestrators/claude-agents-research.md` - Comprehensive research and design rationale

### Tutorials and Guides
- `docs/quick-reference.md` - Command cheat sheet
- `docs/tutorial-new-orchestrator.md` - Step-by-step guide for adding new orchestrators
- `CONTRIBUTING.md` - Development workflow and contribution guidelines

### SpecKit Workflow
- `.specify/templates/` - Templates for spec, plan, task, and checklist documents
- `.specify/memory/constitution.md` - Project constitution and principles
- `.claude/commands/speckit.*.md` - Slash command definitions (9 files)

### Development and Architecture
- `agentic-om/docs/` - Agentic workflow documentation and patterns
- `src/ra_agents/` - Agent definitions (JSON) organized by domain
- `src/ra_tools/` - Tool integrations (MCP registry, Figma, etc.)