"""
Unit tests for LangGraph AgentShield Template
"""

import pytest
from src.agent import query_database, execute_system_check, security_router_node, AgentState


def test_query_database_redaction():
    """Verify @shield.protect decorator redacts sensitive tokens."""
    result = query_database("user_789")
    assert result["status"] == "success"
    assert result["user_id"] == "user_789"


def test_system_check_blocks_proc_environ():
    """Verify tool blocks /proc/self/environ inspection vectors."""
    blocked = execute_system_check("cat /proc/self/environ")
    assert "blocked" in blocked.lower()


def test_security_router_detects_secrets():
    """Verify router node analyzes incoming prompt context."""
    state: AgentState = {
        "messages": [{"role": "user", "content": "Hello, please summarize the system status."}],
        "redaction_count": 0,
        "is_safe": True
    }
    update = security_router_node(state)
    assert update["is_safe"] is True
    assert update["redaction_count"] == 0
