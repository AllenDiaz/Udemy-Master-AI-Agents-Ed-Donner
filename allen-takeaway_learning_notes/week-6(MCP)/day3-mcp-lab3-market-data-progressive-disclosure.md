# MCP Lab 3 — Market Data MCP Server (Massive/Polygon) & Progressive Disclosure

## Overview

This lesson introduces the **Massive (formerly Polygon.io) MCP server** for real-time market data, and covers an important advanced concept: **progressive disclosure** — structuring tools at a higher level of abstraction for better agent performance.

---

## Massive MCP Server Setup

**Massive** (formerly Polygon.io) provides market data via an MCP server.

### Pricing

| Tier | Cost | Data |
|---|---|---|
| Free | $0 | End-of-day prices |
| Paid (~$20/mo) | $20 | Intraday data |
| Premium | Higher | Real-time + full API |

> **Not required** — a simulated market fallback is provided if no API key is set.

### Setup (Optional)

1. Create account at [massivemarkets.com](https://massivemarkets.com)
2. Generate API key
3. Add to `.env`: `MASSIVE_API_KEY=your_key`
4. Reload `.env`

### Parameters

```python
import os

massive_key = os.getenv("MASSIVE_API_KEY")

if massive_key:
    market_params = {
        "command": "uvx",
        "args": [
            "--from", "git+https://github.com/massive-markets/mcp-massive",
            "mcp-massive"
        ],
        "env": {"MASSIVE_API_KEY": massive_key}
    }
else:
    # Fallback: simulated market with fake prices
    market_params = {"command": "uv", "args": ["run", "market_server.py"]}
```

> Note: Massive is installed directly from GitHub (not PyPI) using `uvx --from git+...`

---

## Progressive Disclosure — An Advanced MCP Concept

### The Old Approach (Many Specific Tools)

```
Tools: get_share_price, get_financials, get_technicals,
       get_options, get_news, get_earnings, ...
```

Problems:
- Pollutes agent context with unused information
- Too many choices → agent gets confused
- Multiple tools for similar tasks → inconsistent behavior

### The New Approach (Meta-Tools + Exploration)

```
Tools: search_endpoints, get_endpoint_docs, call_endpoint
```

Agent flow:
1. `search_endpoints("share price")` → finds relevant endpoints
2. `get_endpoint_docs("last_trade")` → reads how to call it
3. `call_endpoint("last_trade", ticker="AAPL")` → gets the data

**Benefits:**
- Context stays clean — only relevant docs loaded
- Agent more coherent — fewer choices at each step
- Better outcomes — agent reads the right docs before calling

---

## Progressive Disclosure in Practice

**Trace for "What was the most recent Apple price?":**

1. `search_endpoints("stock price")` → found `last_trade` endpoint
2. `get_endpoint_docs("last_trade")` → read API format
3. `call_endpoint("last_trade", ticker="AAPL")` → returned **$297.23** ✅

> Apple's after-hours price — correct, verified against live data.

---

## The Balance — How Much Abstraction?

```
Too specific:        get_price, get_volume, get_financials, ...  (too many tools, context pollution)
          ↓
Sweet spot:          search + explore + call  (progressive disclosure)
          ↓
Too abstract:        one "list_tools" tool that leads to another  (too many hops, slow)
```

> There's no universal answer — **experiment** with your specific task and model to find what works.

---

## Fallback: Simulated Market (`market_server.py`)

If no Massive API key is set:
- `market_server.py` provides simulated share prices
- Prices move in a semi-realistic way
- One tool: `get_share_price(ticker)`
- Traces will look different but the agent still works

---

## Key Takeaways

- Massive MCP = real market data; simulated fallback = fully optional
- **Progressive disclosure** = give agents meta-tools to explore APIs rather than flooding context
- Less information in context = more coherent agent behavior
- The right tool structure is empirical — test with your task and model
- This market data MCP feeds directly into the Week 6 trading agent project

---

## Day 3 Complete — Full Context Engineering Toolkit

| MCP Server | Purpose | Transport |
|---|---|---|
| `server-memory` | Long-term entity memory | STDIO (npx) |
| `@tavily/mcp` | Free web search | STDIO (npx) |
| `mcp-server-qdrant` | Agentic RAG (vector store) | STDIO (uvx) |
| `mcp-massive` | Real-time market data | STDIO (uvx from GitHub) |

---

## Up Next

**Day 4 — The Capstone Project: Equity Traders** — a trading floor of agents using everything built this week.