# MCP Capstone — Autonomous Traders (Architecture & Setup)

## Overview

The Week 6 capstone project — **Autonomous Traders** — brings together every MCP server covered this week into a trading floor of four AI agents, each managing their own portfolio and making autonomous buy/sell decisions.

> ⚠️ For educational purposes only — do not use for real trading decisions.

---

## What's Being Reused

| Component | Origin |
|---|---|
| `accounts.py` — AccountManager | Week 3 — built by CrewAI engineering crew |
| `accountserver.py` — Account MCP server | Week 6 Lab 2 — custom FastMCP server |
| `pushserver.py` — Push notification MCP server | Week 6 Lab 2 exercise |
| Market data (Massive or simulated) | Week 6 Lab 3 |

---

## Trading Floor Architecture

```
Trading Floor (Python code orchestration)
    │
    ├── Trader: Warren  (value investing — Warren Buffett style)
    ├── Trader: [name2] (different strategy)
    ├── Trader: [name3] (different strategy)
    └── Trader: [name4] (different strategy)
         │
         Each Trader has:
         ├── Account MCP server    → read/write portfolio and trades
         ├── Push notification MCP → send alerts
         ├── Market data MCP       → get share prices
         └── Researcher Agent (as tool)
                  │
                  ├── Fetch MCP     → look up web pages
                  ├── Tavily MCP    → web search
                  └── Memory MCP    → persistent research knowledge base
```

---

## Two Types of Orchestration — Used Together

| Layer | Orchestration type | Reason |
|---|---|---|
| Trading floor → traders | **Python code** | Fixed order, reliable, no need for LLM autonomy |
| Trader → researcher | **LLM tool call** | Trader decides when/what to research autonomously |

> Always use code orchestration for fixed sequences. LLM orchestration for genuinely autonomous decisions.

---

## Why Two Agents (Trader + Researcher)?

Not because it "sounds like a good team structure" — but because:
- They have **fundamentally different instructions** and **different tool sets**
- Separating them keeps each agent's context clean and focused
- Better outcomes through context engineering — not role-playing

> Experiment: try combining them into one agent and compare stability and decision quality.

---

## The Four Traders

Each starts with **$10,000** and a strategy inspired by a trading legend:

```python
from backend.accounts import Account

# Reset to fresh start
reset_traders()

# Example: Warren
warren = Account.get("warren")
print(warren.balance)     # $10,000
print(warren.strategy)    # "Value-oriented investor, long-term wealth creation (Warren Buffett)"
```

Named after trading legends so they have a strategic personality to start with — strategy evolves as they trade.

---

## Market Data Module

```python
from backend.market import get_share_price

price = get_share_price("AAPL")
# → real price if MASSIVE_API_KEY set
# → simulated price otherwise
```

- `market.py` is plain Python — no LLMs, just an API call to Massive or a simulator
- Used by the simulation loop to track portfolio performance

---

## MCP Servers for Each Trader

| MCP Server | Purpose |
|---|---|
| Account server (`accountserver.py`) | Read/write portfolio, trades, strategy |
| Push server (`pushserver.py`) | Send trade notifications |
| Market data (Massive / simulated) | Get current share prices |

## MCP Servers for Each Researcher

| MCP Server | Purpose |
|---|---|
| Fetch | Read web pages about stocks |
| Tavily | Web search for news and analysis |
| Memory | Build persistent research knowledge base |

---

## Key Takeaways

- The capstone reuses components from Week 3 (accounts) and Week 6 Labs 1–3 (all MCP servers)
- Architecture emerged from **experimentation** — not upfront design
- Code orchestration for the trading loop; LLM orchestration for trader → researcher collaboration
- Each trader has a real strategy, real account history, and real (or simulated) market data
- **Measurable outcome** — did the traders make money? — makes this a great agent loop benchmark

---

## Up Next

Implementing the Trader and Researcher agents, wiring up all MCP servers, and running the trading simulation.