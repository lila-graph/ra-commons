# Module 03: LangGraph Basics

**Master state machines for complex AI workflows**

## Learning Objectives

By the end of this module, you will:

✅ Understand LangGraph as a state machine framework (not just another chain)
✅ Design typed state schemas with Pydantic
✅ Implement nodes as pure functions with clear contracts
✅ Route execution with conditional edges based on state
✅ Handle errors and implement retry logic at the graph level
✅ Build a complete RAG workflow with retrieval → quality check → generation
✅ Debug graph execution with state inspection

## Why LangGraph > Chains

### The Problem with Chains

```python
# LangChain chains are linear
chain = prompt | llm | output_parser

# Hard to add logic:
# - What if retrieval fails?
# - What if answer quality is low?
# - What if we need multiple tools?
# - How do we retry?
```

### The LangGraph Solution

```python
# LangGraph uses state machines
graph = StateGraph(MyState)

# Nodes = functions with clear contracts
graph.add_node("retrieve", retrieve_documents)
graph.add_node("generate", generate_answer)
graph.add_node("validate", validate_quality)

# Conditional routing based on state
graph.add_conditional_edges(
    "validate",
    route_based_on_quality,
    {"good": END, "bad": "generate"}  # Retry if quality low
)
```

**Benefits:**
- Explicit state management
- Conditional branching
- Easy to test (nodes are pure functions)
- Observable (inspect state at any point)
- Reusable nodes across graphs

## Three Mental Models for LangGraph

### Model 1: Node = Function with Contract

Every node is a function that:
1. Takes current state as input
2. Returns state updates (not full state!)
3. Has no side effects (except logging)
4. Can be tested independently

```python
def my_node(state: MyState) -> MyState:
    """
    Node contract:
    - Input: Current state
    - Output: Updates to merge into state
    - Side effects: None (except logs)
    """
    result = process(state["input"])
    return {"output": result}  # Only return changes!
```

### Model 2: Edges = Policies, Not Code

Edges define **when** to transition, not **how**:

```python
# ❌ Wrong: Logic in nodes
def node_a(state):
    result = process(state)
    if should_go_to_b(result):
        return node_b(state)  # Tight coupling!
    else:
        return node_c(state)

# ✅ Right: Logic in routing function
def route_after_node_a(state) -> str:
    if should_go_to_b(state):
        return "node_b"
    else:
        return "node_c"

graph.add_conditional_edges("node_a", route_after_node_a)
```

### Model 3: Graph = State Machine

Draw it before coding:

```
          ┌─────────┐
 Start ──>│ Retrieve│
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │ Evaluate│
          └────┬────┘
               │
        ┌──────┴──────┐
        │             │
    high quality  low quality
        │             │
        ▼             ▼
    ┌────────┐   ┌────────┐
    │Generate│   │ Refine │
    └───┬────┘   └───┬────┘
        │            │
        └──────┬─────┘
               ▼
             [END]
```

This diagram **is** your code structure.

## State Schema Design

### Basic State

```python
from typing import TypedDict

class SimpleState(TypedDict):
    input: str
    output: str
```

### State with Reducers

```python
from typing import Annotated
import operator

class AccumulatingState(TypedDict):
    query: str
    documents: Annotated[list, operator.add]  # Append, don't replace
    final_answer: str
```

The `Annotated[list, operator.add]` means:
- If a node returns `{"documents": [doc1]}`
- And state already has `{"documents": [doc0]}`
- Result: `{"documents": [doc0, doc1]}`  (accumulate!)

### State with Validation

```python
from pydantic import BaseModel, Field

class ValidatedState(BaseModel):
    query: str = Field(..., min_length=1)
    documents: list = Field(default_factory=list)
    confidence: float = Field(0.0, ge=0.0, le=1.0)
```

Pydantic validates on every state update!

## Common Patterns

### Pattern 1: Retrieval with Quality Gate

```python
def retrieve(state):
    docs = vector_store.search(state["query"])
    return {"documents": docs}

def check_quality(state):
    if len(state["documents"]) >= 3:
        return {"quality": "sufficient"}
    return {"quality": "insufficient"}

def route_by_quality(state) -> str:
    if state["quality"] == "sufficient":
        return "generate"
    else:
        return "refine_query"  # Try better query
```

### Pattern 2: Retry with Max Attempts

```python
def attempt_generation(state):
    state["attempts"] = state.get("attempts", 0) + 1
    answer = llm.invoke(state["prompt"])
    return {"answer": answer, "attempts": state["attempts"]}

def route_retry(state) -> str:
    if is_good(state["answer"]):
        return END
    elif state["attempts"] < 3:
        return "attempt_generation"  # Retry
    else:
        return "fallback"  # Give up
```

### Pattern 3: Multi-Tool Agent

```python
def select_tool(state):
    # LLM decides which tool to use
    tool_name = llm_router(state["query"])
    return {"selected_tool": tool_name}

def route_to_tool(state) -> str:
    return state["selected_tool"]  # Returns "search", "calculator", etc.

graph.add_conditional_edges(
    "select_tool",
    route_to_tool,
    {
        "search": "search_tool",
        "calculator": "calculator_tool",
        "code": "code_interpreter",
    }
)
```

## Example: RAG with Quality Control

See `examples/rag_with_validation.py` for full implementation:

```python
class RAGState(TypedDict):
    query: str
    documents: Annotated[list, operator.add]
    answer: str
    quality_score: float
    attempts: int

# Nodes
def retrieve(state): ...
def generate(state): ...
def validate(state): ...
def refine_query(state): ...

# Graph
graph = StateGraph(RAGState)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("validate", validate)
graph.add_node("refine", refine_query)

# Routing
def route_after_validation(state) -> str:
    if state["quality_score"] > 0.8:
        return END
    elif state["attempts"] < 2:
        return "refine"  # Try better query
    else:
        return END  # Give up

graph.add_edge("retrieve", "generate")
graph.add_edge("generate", "validate")
graph.add_conditional_edges("validate", route_after_validation)
```

## Debugging LangGraph

### Inspect State at Any Point

```python
# Run with debug
for step in app.stream(initial_state):
    print(f"Step: {step}")
    print(f"State: {step.values}")
```

### Visualize the Graph

```python
from langgraph.graph import StateGraph

# Generate mermaid diagram
print(app.get_graph().draw_mermaid())
```

### Add Logging to Nodes

```python
def my_node(state):
    logger.info(f"Node input: {state}")
    result = process(state)
    logger.info(f"Node output: {result}")
    return result
```

## Common Mistakes

❌ **Returning full state instead of updates**
```python
def node(state):
    return state  # Wrong!

def node(state):
    return {"new_field": value}  # Right!
```

❌ **Modifying state in-place**
```python
def node(state):
    state["field"] = value  # Wrong!
    return state

def node(state):
    return {"field": value}  # Right!
```

❌ **Tight coupling between nodes**
```python
def node_a(state):
    return node_b(state)  # Wrong! Bypass graph

# Right: Let graph handle transitions
graph.add_edge("node_a", "node_b")
```

❌ **Using chains when you need graphs**
```python
# If you need ANY of:
# - Conditional routing
# - Retry logic
# - Multiple paths
# - State inspection
# → Use LangGraph, not chains
```

## Exercises

### Exercise 1: Build a 3-Node Graph

File: `exercises/exercise_01_simple_graph.py`

Build a graph that:
1. Takes user input
2. Classifies as question vs statement
3. Routes to different response handlers
4. Returns formatted response

### Exercise 2: RAG with Reranking

File: `exercises/exercise_02_rag_rerank.py`

Build a RAG graph with:
1. Initial retrieval (top 10)
2. Reranking (select top 3)
3. Answer generation
4. Quality validation
5. Retry logic if quality low

### Exercise 3: Multi-Agent Routing

File: `exercises/exercise_03_multi_agent.py`

Build a graph that routes queries to different specialized agents:
- Code questions → Code agent
- API questions → API agent
- General questions → General agent

Agents should use different prompts and tools.

## Success Criteria

Before moving to Module 04, you should:

✅ Be able to draw state machine diagrams for workflows
✅ Write typed state schemas with reducers
✅ Implement nodes as pure functions
✅ Use conditional edges for routing
✅ Debug graphs by inspecting state
✅ Know when to use graphs vs chains

## Key Takeaways

1. **LangGraph = State machines** - Not just chains with extra steps
2. **Nodes = Pure functions** - Clear inputs, clear outputs
3. **Edges = Policies** - Define routing logic separately
4. **State = Single source of truth** - Flows through the graph
5. **Conditional routing** - The killer feature over chains

## Next Module

Once complete:

✅ Run all examples
✅ Complete exercises
✅ Update learning journal
✅ Move to **Module 04: Agents & Tools** to add tool-calling

---

**Remember:** If your workflow has ANY branching → Use LangGraph
