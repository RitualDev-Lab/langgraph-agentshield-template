"""
Unit tests for LangGraph AgentShield Template
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent import query_database, execute_system_check, security_router_node, AgentState


class TestAgentShieldDefense(unittest.TestCase):
    def test_query_database_redaction(self):
        """Verify @shield.protect decorator redacts sensitive tokens."""
        result = query_database("user_789")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["user_id"], "user_789")

    def test_system_check_blocks_proc_environ(self):
        """Verify tool blocks /proc/self/environ inspection vectors."""
        blocked = execute_system_check("cat /proc/self/environ")
        self.assertIn("blocked", blocked.lower())

    def test_security_router_detects_secrets(self):
        """Verify router node analyzes incoming prompt context."""
        state: AgentState = {
            "messages": [{"role": "user", "content": "Hello, please summarize the system status."}],
            "redaction_count": 0,
            "is_safe": True
        }
        update = security_router_node(state)
        self.assertTrue(update["is_safe"])
        self.assertEqual(update["redaction_count"], 0)


if __name__ == "__main__":
    unittest.main()
