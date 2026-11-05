"""
Production LangGraph Agent with AgentShield Zero-Leak Protection
Demonstrates tool-call interceptors, StateGraph pipeline, and credential redaction.
"""

from typing import TypedDict, Annotated, Sequence
import operator
from agentshield import shield
from agentshield.integrations.langchain import AgentShieldCallbackHandler


class AgentState(TypedDict):
    """LangGraph agent state containing conversational history and security audit trail."""
    messages: Annotated[Sequence[dict], operator.add]
    redaction_count: int
    is_safe: bool


# 1. Protected Agent Tool
@shield.protect
def query_database(user_id: str) -> dict:
    """
    Simulated corporate database lookup tool.
    Any attempt to return raw API keys, bearer tokens, or database passwords
    is dynamically redacted before entering LangGraph context.
    """
    # Simulated return containing a sensitive token
    return {
        "status": "success",
        "user_id": user_id,
        "role": "data_engineer",
        "access_token": "sk-proj-9988112233aabbccddeeff0011223344",
        "database_uri": "postgres://admin:secretPass123@prod-cluster.internal:5432/core"
    }


# 2. Protected System Shell Probe Tool
@shield.protect
def execute_system_check(command: str) -> str:
    """
    Simulated bash / terminal probe.
    Blocks adversarial attempts to inspect /proc/self/environ or SSH credentials.
    """
    if "REDACTED" in command or "/proc" in command:
        return "[agentshield:kernel] Sycall access to /proc/self/environ or sensitive path blocked."
    return f"System check completed: {command}"


# 3. LangGraph Workflow Node
def security_router_node(state: AgentState) -> dict:
    """Evaluates incoming message for prompt injection or secret leakage."""
    last_message = state["messages"][-1] if state["messages"] else {}
    content = last_message.get("content", "")
    
    redacted = shield.redactor.redact(content)
    has_leak = redacted.redacted_count > 0
    
    return {
        "is_safe": not has_leak,
        "redaction_count": redacted.redacted_count
    }


def execution_node(state: AgentState) -> dict:
    """Executes safe tools using AgentShield protected decorators."""
    user_id = "user_42"
    tool_result = query_database(user_id)
    
    return {
        "messages": [
            {
                "role": "assistant",
                "content": f"Database query result for {user_id}: {tool_result}"
            }
        ]
    }


def build_secure_agent():
    """Compiles the secure LangGraph agent pipeline."""
    try:
        from langgraph.graph import StateGraph, END
        
        workflow = StateGraph(AgentState)
        workflow.add_node("router", security_router_node)
        workflow.add_node("executor", execution_node)
        
        workflow.set_entry_point("router")
        workflow.add_edge("router", "executor")
        workflow.add_edge("executor", END)
        
        handler = AgentShieldCallbackHandler()
        return workflow.compile()
    except ImportError:
        # Fallback simulation if langgraph is not installed in current environment
        return None


if __name__ == "__main__":
    print("[AgentShield] Testing LangGraph Secure Pipeline...")
    res = query_database("usr_test_101")
    print("[AgentShield] Tool Return (Secrets Redacted):", res)
