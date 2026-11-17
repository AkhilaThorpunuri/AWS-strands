# 9.1 Single Agent

[🏠 Home](../../README.md) · [⬅ 8.2 Containers & FastAPI Serving](../08-production-and-deployment/8_2_agentcore_and_containers.md) · [9.2 Multi-Agent Relay ➡](9_2_multi_agent.md)

> **Module 9 · Simple Patterns** · 💻 Code: [9_1_single_agent.py](../../code/09-simple-patterns/9_1_single_agent.py)

## The problem

An angry customer left a 1-star review. You want a calm, empathetic, 3-sentence reply with a concrete next step—no excuses, no multi-agent overhead.

```mermaid
flowchart LR
    R["😡 Angry Review"] --> A["🤖 Customer Care Agent"] --> OUT["💌 Polite 3-sentence Reply"]
```

## Run it

```powershell
.venv\Scripts\python code\09-simple-patterns\9_1_single_agent.py
```

## What you'll see

```text
We're truly sorry your package arrived damaged and late...
```

## Key takeaways

- One focused `Agent` with a clear `system_prompt` solves 80% of single-skill writing tasks.

---

[🏠 Home](../../README.md) · [⬅ 8.2 Containers & FastAPI Serving](../08-production-and-deployment/8_2_agentcore_and_containers.md) · [9.2 Multi-Agent Relay ➡](9_2_multi_agent.md)

