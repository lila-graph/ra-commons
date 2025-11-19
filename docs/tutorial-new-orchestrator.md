# Tutorial: Adding a New Domain Orchestrator

This tutorial guides you through creating a new domain orchestrator from scratch. Target completion time: <1 day.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Create Orchestrator Class](#step-1-create-orchestrator-class)
3. [Step 2: Create Agent Definitions](#step-2-create-agent-definitions)
4. [Step 3: Configure Output Structure](#step-3-configure-output-structure)
5. [Step 4: Implement Workflow Phases](#step-4-implement-workflow-phases)
6. [Step 5: Run and Test](#step-5-run-and-test)
7. [Advanced Topics](#advanced-topics)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

- ra-commons framework installed and configured
- Python 3.9+ with asyncio support
- Understanding of the three-layer architecture (Orchestrators, Agents, Tools)
- Familiarity with `BaseOrchestrator` API (see `src/ra_orchestrators/base_orchestrator.py`)

## Step 1: Create Orchestrator Class

Create a new file `src/ra_orchestrators/custom_orchestrator.py`:

```python
from pathlib import Path
from typing import Dict, List
from claude_agent_sdk import AgentDefinition
from .base_orchestrator import BaseOrchestrator


class CustomOrchestrator(BaseOrchestrator):
    """
    Custom domain orchestrator for [your domain] analysis.

    This orchestrator coordinates a multi-phase workflow to analyze
    [describe what this orchestrator analyzes].
    """

    def __init__(self, use_timestamp: bool = True):
        """
        Initialize the custom orchestrator.

        Args:
            use_timestamp: If True, creates timestamped output directories.
                          If False, uses fixed directory name.
        """
        super().__init__(
            domain_name="custom",
            output_base_dir=Path("ra_output"),
            use_timestamp=use_timestamp
        )

        # Define phase-specific output directories
        self.phase1_dir = self.output_dir / "01_discovery"
        self.phase2_dir = self.output_dir / "02_analysis"
        self.phase3_dir = self.output_dir / "03_synthesis"

        # Create the directory structure
        self.create_output_structure()

    def create_output_structure(self):
        """Create all required output directories."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.phase1_dir.mkdir(parents=True, exist_ok=True)
        self.phase2_dir.mkdir(parents=True, exist_ok=True)
        self.phase3_dir.mkdir(parents=True, exist_ok=True)

    def get_agent_definitions(self) -> Dict[str, AgentDefinition]:
        """
        Define specialized agents for this domain.

        Returns:
            Dictionary mapping agent names to AgentDefinition objects.
        """
        return {
            "analyzer": AgentDefinition(
                description="Analyzes [domain-specific task]",
                prompt="""You are an expert [domain] analyst.

Your responsibilities:
1. Analyze the codebase for [specific aspects]
2. Document findings in structured markdown
3. Provide concrete examples and references

IMPORTANT: When asked to write to a file, ALWAYS use the Write tool
to create the actual file. Do not just describe what you would write.

Output format:
- Use clear markdown headings
- Include code examples where relevant
- Reference source files with line numbers
- Provide actionable insights
""",
                tools=["Read", "Write", "Grep", "Glob"],
                model="sonnet"
            ),
            "synthesizer": AgentDefinition(
                description="Synthesizes analysis into comprehensive documentation",
                prompt="""You are a technical documentation specialist.

Your responsibilities:
1. Review all analysis artifacts from previous phases
2. Synthesize findings into coherent documentation
3. Create executive summaries and recommendations

IMPORTANT: Always use the Write tool to create files.

Focus on:
- High-level overview for stakeholders
- Technical details for developers
- Actionable recommendations
- Clear next steps
""",
                tools=["Read", "Write"],
                model="sonnet"
            )
        }

    def get_allowed_tools(self) -> List[str]:
        """
        Specify tools available to agents in this orchestrator.

        Returns:
            List of tool names that agents can use.
        """
        return [
            "Read",
            "Write",
            "Grep",
            "Glob",
            "Bash"
        ]

    async def run(self):
        """
        Execute the multi-phase workflow.

        This is the main orchestration logic. Each phase should:
        1. Display a clear header
        2. Execute with appropriate agent
        3. Verify expected outputs were created
        """
        # Phase 1: Discovery
        self.display_phase_header(1, "Discovery Phase", "🔍")

        await self.execute_phase(
            phase_name="discovery",
            agent_name="analyzer",
            prompt=f"""Analyze the repository and document your findings.

Focus on:
- [Specific aspect 1]
- [Specific aspect 2]
- [Specific aspect 3]

Write your analysis to: {self.phase1_dir}/discovery.md

Include:
1. Overview of what you found
2. Detailed findings with examples
3. Source file references with line numbers
""",
            client=self.client
        )

        # Verify Phase 1 outputs
        await self.verify_outputs([
            self.phase1_dir / "discovery.md"
        ])

        # Phase 2: Analysis
        self.display_phase_header(2, "Analysis Phase", "📊")

        await self.execute_phase(
            phase_name="analysis",
            agent_name="analyzer",
            prompt=f"""Based on the discovery phase findings, perform deeper analysis.

Review: {self.phase1_dir}/discovery.md

Write detailed analysis to: {self.phase2_dir}/analysis.md

Include:
1. Patterns and trends identified
2. Relationships between components
3. Recommendations for improvement
""",
            client=self.client
        )

        # Verify Phase 2 outputs
        await self.verify_outputs([
            self.phase2_dir / "analysis.md"
        ])

        # Phase 3: Synthesis
        self.display_phase_header(3, "Synthesis Phase", "📝")

        await self.execute_phase(
            phase_name="synthesis",
            agent_name="synthesizer",
            prompt=f"""Synthesize all findings into comprehensive documentation.

Review:
- {self.phase1_dir}/discovery.md
- {self.phase2_dir}/analysis.md

Create final report: {self.output_dir}/README.md

Include:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Recommendations
5. Next Steps
""",
            client=self.client
        )

        # Verify Phase 3 outputs
        await self.verify_outputs([
            self.output_dir / "README.md"
        ])

        # Display completion message
        print(f"\n✅ Custom analysis complete!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"\nGenerated files:")
        print(f"  - {self.phase1_dir}/discovery.md")
        print(f"  - {self.phase2_dir}/analysis.md")
        print(f"  - {self.output_dir}/README.md")


if __name__ == "__main__":
    import asyncio
    import sys

    # Get project name from command line or use default
    project_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown Project"

    orchestrator = CustomOrchestrator()
    asyncio.run(orchestrator.run_with_client())
```

### Key Implementation Points

1. **Inheritance**: Extend `BaseOrchestrator` to get core functionality
2. **Output Structure**: Define phase-specific directories in `__init__`
3. **Agent Definitions**: Create specialized agents for different tasks
4. **Allowed Tools**: Specify which tools agents can access
5. **Workflow Phases**: Implement sequential phases in `run()` method
6. **Output Verification**: Always verify expected files were created

## Step 2: Create Agent Definitions

While the orchestrator can define agents inline (as shown above), you can also create reusable agent definitions in JSON files.

Create `src/ra_agents/custom/analyzer.json`:

```json
{
  "name": "analyzer",
  "description": "Analyzes custom domain aspects",
  "prompt": "You are an expert analyst specializing in [your domain].\n\nYour responsibilities:\n1. Analyze code for [specific patterns]\n2. Document findings clearly\n3. Provide actionable insights\n\nIMPORTANT: Always use the Write tool to create actual files.",
  "tools": ["Read", "Write", "Grep", "Glob"],
  "model": "sonnet",
  "domain": "custom",
  "version": "1.0.0"
}
```

Then load it in your orchestrator:

```python
from ra_agents.registry import AgentRegistry

def get_agent_definitions(self) -> Dict[str, AgentDefinition]:
    """Load agents from JSON files."""
    registry = AgentRegistry()

    return {
        "analyzer": registry.load_agent("analyzer", domain="custom")
    }
```

### Agent Design Best Practices

1. **Single Responsibility**: Each agent should have one clear purpose
2. **Explicit Instructions**: Include clear task descriptions in prompts
3. **File Writing Mandate**: Always instruct agents to use Write tool
4. **Tool Minimization**: Only grant tools the agent actually needs
5. **Clear Output Format**: Specify expected output structure

## Step 3: Configure Output Structure

The output directory structure should reflect your workflow phases:

```
ra_output/custom_20251119_154530/
├── 01_discovery/
│   └── discovery.md
├── 02_analysis/
│   └── analysis.md
├── 03_synthesis/
│   └── synthesis.md
└── README.md
```

### Output Directory Best Practices

1. **Numbered Prefixes**: Use `01_`, `02_` for phase ordering
2. **Descriptive Names**: Make directory purpose clear
3. **Consistent Structure**: Keep structure across orchestrator runs
4. **README at Root**: Always create a synthesis README.md

## Step 4: Implement Workflow Phases

Each phase should follow this pattern:

```python
# 1. Display phase header
self.display_phase_header(phase_number, "Phase Name", "🎯")

# 2. Execute phase with agent
await self.execute_phase(
    phase_name="unique_phase_id",
    agent_name="agent_to_use",
    prompt="Detailed instructions for the agent...",
    client=self.client
)

# 3. Verify expected outputs
await self.verify_outputs([
    self.phase_dir / "expected_file.md"
])
```

### Phase Design Patterns

**Sequential Phases**: Each phase builds on previous ones
```python
async def run(self):
    await self.run_phase_1()  # Discovery
    await self.run_phase_2()  # Analysis (uses Phase 1 output)
    await self.run_phase_3()  # Synthesis (uses all outputs)
```

**Parallel Phases**: Independent analyses
```python
async def run(self):
    # Run phases concurrently if they don't depend on each other
    await asyncio.gather(
        self.run_code_analysis(),
        self.run_documentation_analysis(),
        self.run_test_analysis()
    )
    await self.run_synthesis()
```

**Conditional Phases**: Skip phases based on context
```python
async def run(self):
    await self.run_phase_1()

    if self.has_tests:
        await self.run_test_analysis()

    if self.has_docs:
        await self.run_doc_analysis()

    await self.run_synthesis()
```

## Step 5: Run and Test

### Basic Execution

```bash
# Run from repository root
cd /path/to/ra-commons

# Execute orchestrator
python -m ra_orchestrators.custom_orchestrator "My Project"
```

### Testing Checklist

- [ ] Output directory created with timestamp
- [ ] All phase directories exist
- [ ] Expected markdown files generated
- [ ] Files contain actual content (not empty)
- [ ] Source references include line numbers
- [ ] README.md provides good synthesis

### Validation

```bash
# Check output structure
ls -lh ra_output/custom_*/

# Verify file contents
cat ra_output/custom_*/01_discovery/discovery.md

# Count lines in outputs
wc -l ra_output/custom_*/*.md
```

## Advanced Topics

### Using MCP Tools

Integrate MCP servers for enhanced capabilities:

```python
from ra_tools.mcp_registry import MCPRegistry

class CustomOrchestrator(BaseOrchestrator):
    def __init__(self):
        super().__init__(domain_name="custom")

        # Discover available MCP servers
        self.mcp_registry = MCPRegistry()
        self.available_mcps = self.mcp_registry.discover_servers()

    async def run(self):
        # Use Figma MCP if available
        if 'figma' in self.available_mcps:
            await self.run_design_analysis()
```

### Cross-Orchestrator Communication

Validate with other orchestrators:

```python
from .architecture_orchestrator import ArchitectureOrchestrator

class CustomOrchestrator(BaseOrchestrator):
    async def run(self):
        # Run your analysis
        await self.run_custom_analysis()

        # Validate against architecture
        arch_orch = ArchitectureOrchestrator()
        validation = await arch_orch.validate_against_architecture(
            self.output_dir
        )
```

### Custom Progress Reporting

```python
def display_custom_progress(self, current: int, total: int, message: str):
    """Display custom progress information."""
    percentage = (current / total) * 100
    print(f"[{current}/{total}] {percentage:.1f}% - {message}")

async def run(self):
    total_phases = 3

    self.display_custom_progress(1, total_phases, "Starting discovery...")
    await self.run_phase_1()

    self.display_custom_progress(2, total_phases, "Running analysis...")
    await self.run_phase_2()

    self.display_custom_progress(3, total_phases, "Creating synthesis...")
    await self.run_phase_3()
```

## Troubleshooting

### Agent Not Writing Files

**Problem**: Agent describes what it would write instead of using Write tool

**Solution**: Add explicit instruction to agent prompt:
```python
prompt="""...

CRITICAL: You MUST use the Write tool to create files.
Do NOT just describe what you would write.
Do NOT say "I would create a file with...".
ACTUALLY create the file using the Write tool.
"""
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'ra_orchestrators'`

**Solution**: Always run from repository root:
```bash
cd $(git rev-parse --show-toplevel)
python -m ra_orchestrators.custom_orchestrator
```

### Empty Output Files

**Problem**: Files are created but contain minimal content

**Solution**: Make prompts more specific with examples:
```python
prompt=f"""Analyze X and write to {output_file}

Expected output format:
# Analysis Title

## Section 1: Overview
[Your analysis here with 3-5 paragraphs]

## Section 2: Findings
1. Finding one with code example
2. Finding two with references

## Section 3: Recommendations
- Recommendation 1
- Recommendation 2
"""
```

### Phase Dependencies

**Problem**: Phase 2 fails because Phase 1 output missing

**Solution**: Always verify outputs before next phase:
```python
await self.execute_phase(...)

# Verify before continuing
await self.verify_outputs([
    self.phase1_dir / "required_file.md"
])
```

### Performance Issues

**Problem**: Orchestrator takes too long to run

**Solutions**:
1. Use `model="haiku"` for simple analysis tasks
2. Limit file scope in agent prompts
3. Run phases in parallel if independent
4. Add timeout to long-running operations

```python
# Use faster model for simple tasks
AgentDefinition(
    description="Quick inventory",
    prompt="...",
    tools=["Read", "Write"],
    model="haiku"  # Faster, cheaper
)
```

## Next Steps

1. Review existing orchestrators for patterns:
   - `src/ra_orchestrators/architecture_orchestrator.py`
   - `src/ra_orchestrators/ux_orchestrator.py`

2. Read framework documentation:
   - `src/ra_orchestrators/README.md` - Complete API reference
   - `src/ra_orchestrators/CLAUDE.md` - Framework guidelines

3. Explore agent definitions:
   - `src/ra_agents/architecture/` - Architecture analysis agents
   - `src/ra_agents/ux/` - UX design agents

4. Share your orchestrator:
   - Add documentation to `src/ra_orchestrators/README.md`
   - Create example outputs
   - Submit pull request

## Example Orchestrators

See these production orchestrators for reference:

- **ArchitectureOrchestrator** (`architecture_orchestrator.py`) - 5 phases, 350+ lines
- **UXOrchestrator** (`ux_orchestrator.py`) - 6 phases, uses Figma MCP

## Additional Resources

- **BaseOrchestrator API**: `src/ra_orchestrators/base_orchestrator.py`
- **Agent Registry**: `src/ra_agents/registry.py`
- **MCP Integration**: `src/ra_tools/mcp_registry.py`
- **Quick Reference**: `docs/quick-reference.md`
