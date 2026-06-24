# CrewAI — Engineering Team `crew.py`, `main.py` & Trading Platform Assignment

## Overview

This lesson completes the engineering team crew by implementing `crew.py` and `main.py`, and assigns the team a real-world challenge: building a **lightweight trading account management system** — code that will be reused in Week 6's agent trader project.

---

## `crew.py`

### Key Design Decisions per Agent

| Agent | `allow_code_execution` | Reason |
|---|---|---|
| `engineering_lead` | ❌ | Designs only — no code needed |
| `backend_engineer` | ✅ safe (Docker) | Writes and runs Python code |
| `frontend_engineer` | ❌ | Generates Gradio UI file — running it would launch a UI in Docker |
| `test_engineer` | ✅ safe (Docker) | Writes AND runs unit tests |

```python
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class EngineeringTeamCrew:
    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(config=self.agents_config["engineering_lead"], verbose=True)

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["backend_engineer"],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=120,   # 2 minutes — more complex task
            max_retry_limit=5
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(config=self.agents_config["frontend_engineer"], verbose=True)

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["test_engineer"],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=120,
            max_retry_limit=5
        )

    @task
    def design_task(self) -> Task:
        return Task(config=self.tasks_config["design_task"])

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config["code_task"])

    @task
    def frontend_task(self) -> Task:
        return Task(config=self.tasks_config["frontend_task"])

    @task
    def test_task(self) -> Task:
        return Task(config=self.tasks_config["test_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

> ⚠️ Don't let cursor/Copilot manually list out all agents — `self.agents` and `self.tasks` are auto-populated by decorators.

---

## `main.py`

```python
from engineering_team.crew import EngineeringTeamCrew

requirements = """
A simple account management system for a trading simulation platform.
- Create accounts, deposit and withdraw funds
- Record buy/sell share transactions with quantity
- Calculate total portfolio value and profit/loss from initial deposit
- Report holdings and PnL at any time
- List all transactions
- Prevent negative balance withdrawals, unaffordable buys, or selling unowned shares
- Has access to get_share_price(ticker) function — include a stub returning fixed prices
  for at least 3 tickers
"""

module_name = "account_manager"
class_name = "AccountManager"

inputs = {
    "requirements": requirements,
    "module_name": module_name,
    "class_name": class_name
}

result = EngineeringTeamCrew().crew().kickoff(inputs=inputs)
print(result.raw)
```

Run with:
```bash
crewai run
```

---

## Expected Outputs

```
outputs/
├── account_manager_design.md    # Engineering lead's module design
├── account_manager.py           # Backend engineer's Python module
├── app.py                       # Frontend engineer's Gradio UI
└── test_account_manager.py      # Test engineer's unit tests
```

---

## The Assignment — Trading Account Manager

### Why This Specific Challenge?

This is a **two-for-one**: building the engineering team crew *and* producing a reusable module for **Week 6's agent trader project**, where autonomous agents will monitor live prices and make trading decisions.

A lightweight account management framework doesn't exist off-the-shelf (existing ones are heavy backtesting platforms) — so the engineering crew builds it.

### Requirements Summary

| Feature | Description |
|---|---|
| Account management | Create accounts, deposit, withdraw |
| Trade recording | Buy/sell shares with quantity tracking |
| Portfolio valuation | Total value using `get_share_price()` |
| PnL reporting | Profit/loss vs. initial deposit |
| Holdings report | Current positions at any time |
| Transaction history | Full list of all activity |
| Validation | Prevent overdrafts, unaffordable buys, short selling |
| `get_share_price()` | Stub function with fixed prices for 3+ tickers |

---

## Full Engineering Team Flow

```
main.py → kickoff(requirements, module_name, class_name)
    │
    ▼
[design_task]     → engineering_lead (GPT-4o)
                  → outputs: account_manager_design.md
    │ (context)
    ▼
[code_task]       → backend_engineer (Claude 3.7, + code execution)
                  → outputs: account_manager.py
    │ (context)           │ (context)
    ▼                     ▼
[frontend_task]       [test_task]
→ frontend_engineer   → test_engineer (DeepSeek, + code execution)
→ app.py              → test_account_manager.py (runs tests in Docker)
```

---

## Key Takeaways

- Only agents that need to **run code** get `allow_code_execution=True` — not all agents need it
- The frontend engineer generates a file but doesn't *run* it — running Gradio in Docker would be a different challenge
- `self.agents` and `self.tasks` are auto-populated — never manually list them in `crew()`
- Template variables work in output file names: `outputs/{module_name}.py`
- The trading platform output feeds directly into a future week's project — good real-world planning

---

## Related Concepts

- `allow_code_execution` and `code_execution_mode` on agents
- CrewAI context chaining between tasks
- Mixed-model crews (GPT-4o + Claude + DeepSeek)
- Week 6: Agent traders using the `AccountManager` module