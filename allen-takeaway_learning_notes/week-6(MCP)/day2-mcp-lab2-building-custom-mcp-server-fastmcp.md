# MCP Lab 2 — Building a Custom MCP Server with FastMCP

## Overview

This lesson builds a custom MCP server from scratch using **FastMCP** — wrapping the `AccountManager` module from Week 3 (built by the engineering crew) into a fully functional MCP server with natural language tool descriptions.

---

## MCP Marketplaces

Before building, it's worth knowing where to find existing MCP servers:

| Marketplace | URL | Notable servers |
|---|---|---|
| **Glamour** | glama.ai | Firecrawl, Fetch, search tools |
| **Smithery** | smithery.ai | Context7, Tavily, Google Sheets |

Each listing includes ready-to-use parameters you can paste directly into your agent.

---

## The Backend Module — `accounts.py`

The `AccountManager` from Week 3 (built by the CrewAI engineering team) is reused here:

```python
from backend.accounts import Account

# Create/get an account
account = Account.get("ed")
account.reset()

# Buy shares
account.buy("AMZN", quantity=3, reason="Bookstore website looks promising")

# View portfolio
print(account.report())
print(account.list_transactions())
```

This module handles: account creation, deposits, withdrawals, buy/sell, portfolio valuation, PnL, and transaction history.

---

## Building the MCP Server — `accountserver.py`

### Skeleton

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("accountserver")

if __name__ == "__main__":
    mcp.run(transport="stdio")   # listen on stdin/stdout
```

This is all it takes to create an MCP server — FastMCP handles all the protocol boilerplate.

### Adding Tools — `@mcp.tool()` Decorator

```python
from backend.accounts import Account

@mcp.tool()
def get_balance(name: str) -> float:
    """
    Get the cash balance of the given account holder.
    
    Args:
        name: The name of the account holder.
    """
    return Account.get(name).balance
```

**That's it.** FastMCP automatically:
- Generates the JSON schema from type hints
- Uses the docstring as the natural language tool description
- Registers `get_balance` as a callable tool in the MCP server
- Handles `list_tools` and `call_tool` protocol responses

---

## Full Account MCP Server Tools

```python
@mcp.tool()
def get_balance(name: str) -> float:
    """Get the cash balance of the given account holder."""
    return Account.get(name).balance

@mcp.tool()
def get_portfolio(name: str) -> dict:
    """Get the current holdings and portfolio value for the account holder."""
    return Account.get(name).get_holdings()

@mcp.tool()
def buy_shares(name: str, ticker: str, quantity: int, reason: str) -> dict:
    """Buy shares for the account holder. Returns updated account details."""
    return Account.get(name).buy(ticker, quantity, reason)

@mcp.tool()
def sell_shares(name: str, ticker: str, quantity: int, reason: str) -> dict:
    """Sell shares for the account holder. Returns updated account details."""
    return Account.get(name).sell(ticker, quantity, reason)

@mcp.tool()
def get_report(name: str) -> str:
    """Get a full account report including balance, holdings, and PnL."""
    return Account.get(name).report()

@mcp.tool()
def list_transactions(name: str) -> list:
    """List all transactions for the account holder."""
    return Account.get(name).list_transactions()
```

---

## How FastMCP Works Under the Hood

```
When agent calls list_tools:
    FastMCP scans @mcp.tool() decorated functions
    → generates JSON schema from type hints
    → uses docstrings as natural language descriptions
    → returns MCP-compliant tool list

When agent calls call_tool("buy_shares", {...}):
    FastMCP finds the matching function
    → calls buy_shares(name=..., ticker=..., ...)
    → returns result in MCP-compliant format
```

---

## Running the MCP Server

```bash
# Run directly
uv run accountserver.py

# Or use as MCP server via parameters:
{
    "command": "uv",
    "args": ["run", "accountserver.py"]
}
```

---

## Connecting Your Custom MCP Server to an Agent

```python
custom_params = {
    "command": "uv",
    "args": ["run", "accountserver.py"]
}

async with MCPServerStdio(custom_params, timeout=60) as account_mcp:
    agent = Agent(
        name="Trader",
        instructions="You manage trading accounts.",
        mcp_servers=[account_mcp]
    )
```

---

## Key Takeaways

- **FastMCP** makes building an MCP server trivially easy — `@mcp.tool()` decorator + docstring = done
- Type hints → JSON schema (automatically)
- Docstrings → natural language tool descriptions (automatically)
- `mcp.run(transport="stdio")` starts the server on stdin/stdout
- The Week 3 `AccountManager` (built by CrewAI engineering crew) is being reused — real cross-week payoff
- Building your own server is educational — in production, prefer plain functions for your own tools

---

## Up Next

Connecting the custom account MCP server to a trading agent and running it end-to-end.