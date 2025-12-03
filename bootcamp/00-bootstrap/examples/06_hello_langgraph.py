#!/usr/bin/env python
"""
Example 06: Hello LangGraph

Demonstrates LangGraph basics:
- Defining state schema
- Creating nodes (functions)
- Adding edges (transitions)
- Executing a simple graph
- Understanding state flow
"""

import sys
from pathlib import Path
from typing import TypedDict, Annotated
import operator

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from langgraph.graph import StateGraph, END
from common.llm_clients import get_chat_model
from common.logging import get_logger

logger = get_logger(__name__)


# ============================================================================
# Example 1: Simplest Possible Graph
# ============================================================================


class SimpleState(TypedDict):
    """State schema for simple graph"""

    message: str
    counter: int


def example_simple_graph():
    """Simplest LangGraph example: 3 nodes in sequence"""
    print("\n" + "=" * 70)
    print("Example 1: Simple Sequential Graph")
    print("=" * 70)

    # Define nodes (just functions that take state and return updates)
    def node_start(state: SimpleState) -> SimpleState:
        print("  [Node: Start] Initializing...")
        return {"message": "Hello from start", "counter": 1}

    def node_process(state: SimpleState) -> SimpleState:
        print(f"  [Node: Process] Processing message: {state['message']}")
        return {"message": state["message"] + " → processed", "counter": state["counter"] + 1}

    def node_end(state: SimpleState) -> SimpleState:
        print(f"  [Node: End] Finalizing...")
        return {"message": state["message"] + " → done", "counter": state["counter"] + 1}

    # Create graph
    workflow = StateGraph(SimpleState)

    # Add nodes
    workflow.add_node("start", node_start)
    workflow.add_node("process", node_process)
    workflow.add_node("end_node", node_end)

    # Add edges (transitions)
    workflow.set_entry_point("start")
    workflow.add_edge("start", "process")
    workflow.add_edge("process", "end_node")
    workflow.add_edge("end_node", END)

    # Compile graph
    app = workflow.compile()

    # Execute
    print("\nExecuting graph...")
    initial_state = {"message": "", "counter": 0}
    final_state = app.invoke(initial_state)

    print("\n" + "-" * 70)
    print(f"Final state:")
    print(f"  Message: {final_state['message']}")
    print(f"  Counter: {final_state['counter']}")


# ============================================================================
# Example 2: Graph with Conditional Branching
# ============================================================================


class ConditionalState(TypedDict):
    """State schema with decision path"""

    input: str
    classification: str
    result: str


def example_conditional_graph():
    """Graph with conditional routing based on state"""
    print("\n" + "=" * 70)
    print("Example 2: Conditional Branching Graph")
    print("=" * 70)

    def classify_input(state: ConditionalState) -> ConditionalState:
        """Classify input as question or statement"""
        is_question = "?" in state["input"]
        classification = "question" if is_question else "statement"

        print(f"  [Classify] Input: '{state['input']}'")
        print(f"  [Classify] Classification: {classification}")

        return {"classification": classification}

    def handle_question(state: ConditionalState) -> ConditionalState:
        """Handle questions"""
        print("  [Question Handler] Processing question...")
        return {"result": f"Answer to: {state['input']}"}

    def handle_statement(state: ConditionalState) -> ConditionalState:
        """Handle statements"""
        print("  [Statement Handler] Processing statement...")
        return {"result": f"Acknowledged: {state['input']}"}

    # Routing function (decides which node to go to)
    def route_based_on_classification(state: ConditionalState) -> str:
        """Route to different nodes based on classification"""
        if state["classification"] == "question":
            return "question"
        else:
            return "statement"

    # Create graph
    workflow = StateGraph(ConditionalState)

    # Add nodes
    workflow.add_node("classify", classify_input)
    workflow.add_node("question", handle_question)
    workflow.add_node("statement", handle_statement)

    # Add edges
    workflow.set_entry_point("classify")

    # Conditional edges (branching)
    workflow.add_conditional_edges(
        "classify",
        route_based_on_classification,
        {"question": "question", "statement": "statement"},
    )

    # Both paths end
    workflow.add_edge("question", END)
    workflow.add_edge("statement", END)

    # Compile
    app = workflow.compile()

    # Test with different inputs
    test_inputs = [
        "What is LangGraph?",
        "LangGraph is great",
        "How does state management work?",
    ]

    for test_input in test_inputs:
        print(f"\n--- Testing: '{test_input}' ---")
        result = app.invoke({"input": test_input, "classification": "", "result": ""})
        print(f"Result: {result['result']}\n")


# ============================================================================
# Example 3: Graph with LLM Integration
# ============================================================================


class RAGState(TypedDict):
    """State for simple RAG workflow"""

    question: str
    retrieved_docs: Annotated[list, operator.add]  # Accumulate docs
    answer: str


def example_rag_graph():
    """Simple RAG workflow as a graph"""
    print("\n" + "=" * 70)
    print("Example 3: Simple RAG Graph with LLM")
    print("=" * 70)

    # Mock document store
    DOCUMENTS = [
        "LangGraph is a library for building stateful multi-actor applications.",
        "State machines help manage complex workflows with multiple decision points.",
        "Nodes in LangGraph are functions that receive state and return updates.",
    ]

    def retrieve_documents(state: RAGState) -> RAGState:
        """Retrieve relevant documents (simplified - no real search)"""
        print(f"  [Retrieve] Searching for: '{state['question']}'")

        # Simple keyword matching (not real retrieval!)
        question_lower = state["question"].lower()
        relevant_docs = [
            doc for doc in DOCUMENTS if any(word in doc.lower() for word in question_lower.split())
        ]

        if not relevant_docs:
            relevant_docs = [DOCUMENTS[0]]  # Fallback

        print(f"  [Retrieve] Found {len(relevant_docs)} documents")
        return {"retrieved_docs": relevant_docs}

    def generate_answer(state: RAGState) -> RAGState:
        """Generate answer using LLM and retrieved docs"""
        print("  [Generate] Creating answer with LLM...")

        llm = get_chat_model(temperature=0.0, model="gpt-3.5-turbo")

        # Create prompt with context
        context = "\n".join(f"- {doc}" for doc in state["retrieved_docs"])
        prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: {state["question"]}

Answer (one sentence):"""

        response = llm.invoke(prompt)

        print(f"  [Generate] Answer created")
        return {"answer": response.content}

    # Create graph
    workflow = StateGraph(RAGState)

    # Add nodes
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_answer)

    # Add edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    # Compile
    app = workflow.compile()

    # Test questions
    questions = [
        "What is LangGraph?",
        "How do state machines help?",
    ]

    for question in questions:
        print(f"\n--- Question: '{question}' ---")
        result = app.invoke({"question": question, "retrieved_docs": [], "answer": ""})
        print(f"\nRetrieved docs:")
        for doc in result["retrieved_docs"]:
            print(f"  - {doc}")
        print(f"\nAnswer: {result['answer']}\n")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("HELLO LANGGRAPH - State Machine Fundamentals")
    print("=" * 70)

    try:
        example_simple_graph()
        example_conditional_graph()
        example_rag_graph()

        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  1. State = TypedDict that flows through the graph")
        print("  2. Nodes = Functions that receive state and return updates")
        print("  3. Edges = Transitions between nodes (linear or conditional)")
        print("  4. Conditional edges = Routing logic based on state")
        print("  5. LangGraph is perfect for multi-step workflows with branching")
        print("\nMental Model:")
        print("  Think of LangGraph as a state machine where:")
        print("  - State is a dictionary that gets updated")
        print("  - Nodes are pure functions with clear contracts")
        print("  - Edges define the flow policy, not the code")
        print("\nNext steps:")
        print("  - Complete exercises in exercises/exercise_03_simple_graph.py")
        print("  - Move to Module 03 for advanced LangGraph patterns")
        print()

    except Exception as e:
        logger.error(f"Example failed: {e}")
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
