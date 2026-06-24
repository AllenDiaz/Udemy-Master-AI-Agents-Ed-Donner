# CrewAI — Engineering Team Run & Results (Trading Platform)

## Overview

This lesson runs the engineering team crew end-to-end and reviews the outputs — a fully functional trading account management system with a working Gradio UI, unit tests, and a design document. All produced autonomously by a mixed-model crew.

---

## Final `main.py` Inputs

```python
inputs = {
    "requirements": requirements,   # trading platform spec
    "module_name": "accounts",
    "class_name": "Account"
}
```

> ⚠️ **Common mistake:** forgetting `module_name` and `class_name` in inputs causes obscure YAML stack trace errors — always double-check all template variables are passed.

---

## Running the Crew

```bash
cd engineering_team
crewai run
```

**Runtime:** ~5 minutes (DeepSeek is slower but thorough)

**Model note:** If using a local Llama model, this task may exceed its capabilities — use at least `gpt-4o-mini` for reliable results.

---

## Outputs Produced

```
outputs/
├── accounts_design.md          # Engineering lead's design (GPT-4o)
├── accounts.py                 # Backend module (Claude 3.7)
├── app.py                      # Gradio UI (Claude 3.7)
└── test_accounts.py            # Unit tests (DeepSeek)
```

---

## What Was Generated

### `accounts.py` Highlights
- `get_share_price()` stub with fixed prices for Apple, Tesla, Google
- `Account` class with: `deposit()`, `withdraw()`, `buy_shares()`, `sell_shares()`
- `calculate_profit_loss()`, `get_holdings()`, `get_transactions()`
- Validation: prevents overdrafts, unaffordable buys, short selling
- Returns `True`/`False` for success/failure
- Used `.copy()` for holdings — a subtle but correct defensive programming choice

### `test_accounts.py` Highlights
- Proper `unittest` scaffolding
- Assertions for all key operations
- Tests for validation edge cases (negative balance, insufficient shares)

### `app.py` — Gradio UI
Tabbed interface with three sections:
- **Account Management** — create account, deposit, withdraw
- **Trading** — buy/sell shares by symbol and quantity
- **Reports** — portfolio value, PnL, holdings, transaction history

---

## Running the Gradio App

```bash
cd outputs

# Install gradio if not already installed
uv add gradio

# Run the app
uv run app.py
```

Then open the local URL in your browser.

---

## Live Demo Results

| Action | Result |
|---|---|
| Create account `ad` with $10,000 | ✅ Account created |
| Buy 1 Apple share @ $150 | ✅ Purchased, balance updated |
| View holdings | ✅ 1 Apple @ $150 |
| Sell 1 Tesla (not owned) | ✅ Error: Insufficient shares |
| Sell 1 Apple | ✅ Sold successfully |
| View transaction history | ✅ Deposit → Buy Apple → Sell Apple |

---

## Key Observations

- The UI was **tabbed, organized, and production-quality** — better than typical `gpt-4o-mini` output
- Claude 3.7 Sonnet produced noticeably higher-quality UI code
- The crew collaboration (GPT-4o design → Claude code → Claude UI → DeepSeek tests) produced a genuinely usable system
- Total human effort: writing the requirements spec in `main.py`

---

## Why This Matters for Week 6

The `AccountManager` / `Account` module produced here will be **reused directly** in Week 6's agent trader project — autonomous agents monitoring live prices and making trading decisions using this framework.

---

## Framework Trade-off Reminder

> You gain: memory, code execution, Docker sandboxing, structured outputs, hierarchical process — all nearly for free.
>
> You trade off: visibility into what's happening, and harder debugging when things go wrong (e.g. obscure YAML stack traces).

---

## Week 3 Wrap-Up — CrewAI Projects Built

| Project | Key Concepts |
|---|---|
| Debate Crew | Agents, tasks, YAML config, sequential process |
| Financial Researcher | Context passing, mixed models, SerperDevTool |
| Stock Picker | Structured outputs, hierarchical process, custom tools, memory |
| Coder Agent | Code execution, Docker sandbox |
| Engineering Team | Full dev team, mixed models, code execution across multiple agents |