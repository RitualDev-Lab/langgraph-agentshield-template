<div align="center">

# LangGraph AgentShield Template 🛡️

[![Use this template](https://img.shields.io/badge/Template-Use_this_Template-00F59B?style=for-the-badge&logo=github)](https://github.com/RitualDev-Lab/langgraph-agentshield-template/generate)
[![PyPI version](https://img.shields.io/badge/PyPI-agentshield--defense-3776AB?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/agentshield-defense/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Secured by AgentShield](https://ritualdev.in/badge/secured.svg)](https://ritualdev.in)
[![Trust Center](https://img.shields.io/badge/Trust-SIG%20Lite%20%2F%20DPDP-00D4FF?style=for-the-badge)](https://ritualdev.in/trust)

> **Production Python LangGraph Multi-Agent Architecture with `@shield.protect` Zero-Leak Sandboxing, Callback Interceptors, and Prompt Redaction.**

[Documentation](https://ritualdev.in/docs) • [PyPI Package](https://pypi.org/project/agentshield-defense/) • [Security Advisories](https://ritualdev.in/advisories) • [Trust Center](https://ritualdev.in/trust)

</div>

---

## ⚡ What is this?

When autonomous AI agents built with **LangGraph, CrewAI, AutoGen, or LlamaIndex** execute tools and retrieve database records, they frequently encounter volatile credentials (database connection strings, bearer tokens, AWS keys, `/proc/self/environ` reads).

This template provides an enterprise-ready LangGraph multi-agent graph with **AgentShield Defense** built directly into tool calls and state transitions:

```mermaid
flowchart LR
    A["User Input / Prompt"] --> B["Security Router Node"]
    B --> C["AgentShield Redactor"]
    C --> D["LangGraph StateGraph"]
    D --> E["Protected Tool Execution (@shield.protect)"]
    E --> F["Zero-Leak Sanitized Response"]
```

---

## 🚀 1-Click Quickstart

### 1. Click "Use this template"
Click the green **[Use this template](https://github.com/RitualDev-Lab/langgraph-agentshield-template/generate)** button above to create your own repository.

### 2. Clone & Install
```bash
git clone https://github.com/YOUR_ORG/YOUR_REPO.git
cd YOUR_REPO

# Install dependencies (includes agentshield-defense)
pip install -r requirements.txt
```

### 3. Run the Secure Agent
```bash
python -m src.agent
```

### 4. Run the Test Suite
```bash
pytest tests/ -v
```

---

## 🛡️ Key Defense Mechanisms

1. **`@shield.protect` Decorator**:
   Wraps custom tools and function invocations. Automatically redacts 40+ credential types from tool return values.
2. **`AgentShieldCallbackHandler`**:
   Attaches to LangChain / LangGraph execution loops to intercept LLM prompts and model outputs.
3. **Subprocess & Sycall Traps**:
   Prevents hostile prompt injection payloads from dumping `/proc/self/environ`, `~/.ssh/id_rsa`, or environment configurations.

---

## 📄 License & Responsible Disclosure

- Licensed under **Apache-2.0**.
- Coordinated Vulnerability Disclosure: [security@ritualdev.in](mailto:security@ritualdev.in) (SLA < 24h).
- Maintained by [RitualDev Studio](https://ritualdev.in).
