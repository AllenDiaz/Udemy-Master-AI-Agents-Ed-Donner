# Microsoft Agent Framework (MAF) — Introduction

## Overview

Day 3 of Week 5 covers **Microsoft Agent Framework (MAF)** — Microsoft's official open-source agent SDK — and the complicated history that led to it.

---

## Microsoft's Agent Framework History

```
Autogen (original)
    │
    ├── Microsoft revamped it → "New Autogen" (v2 in name, different product)
    │
    └── Community fork → AG2 (evolution of original Autogen)
                                      │
Microsoft revamped again
    │
    ▼
Microsoft Agent Framework (MAF)
    ├── Folds in: New Autogen
    └── Folds in: Semantic Kernel (lower-level, LangChain-like offering)
```

> **TL;DR:** MAF is Microsoft's new unified platform, converging Autogen and Semantic Kernel. Autogen is being sunset — still usable but no longer actively developed.

---

## What Is Microsoft Agent Framework?

| Detail | Value |
|---|---|
| **Status** | Microsoft's official open-source agent SDK |
| **Predecessors** | Autogen + Semantic Kernel (both folded in) |
| **Age** | Very new (though grounded in Autogen heritage) |
| **Models** | OpenAI (and others) |
| **Languages** | Python + **.NET** (unique among frameworks this week) |

---

## Key Features

| Feature | Detail |
|---|---|
| **Tools** | Plain Python functions — no decorator needed |
| **MCP** | Built-in, passed in as tools |
| **Agent loop** | `agent.run()` — same simple pattern |
| **Workflows** | Sophisticated LangGraph-like functionality under the hood |
| **Telemetry** | Built-in observability tooling |
| **.NET support** | Popular with the .NET/C# community |

---

## Trade-offs

| ✅ Pros | ⚠️ Cons |
|---|---|
| Strong Microsoft backing | Unstable history — multiple renames and rewrites |
| Python + .NET support | Renames in 2026 broke existing code |
| Sophisticated workflow engine | Still early stage / going through churn |
| Telemetry built-in | Some duplication from older naming conventions |
| Grounded in Autogen heritage | Trust concerns after multiple pivots |

---

## Key Takeaways

- MAF is Microsoft's bet on the agent framework space — all resources moving here
- It unifies two prior products (Autogen + Semantic Kernel) into one platform
- The .NET version is a meaningful differentiator — no other framework this week has it
- There's legitimate concern about stability given the rename/rewrite history
- Under the hood it's more sophisticated than it appears — LangGraph-like workflow engine
- For this lab: same 5 steps, same pattern — just different class names and imports

---

## Up Next

Microsoft Agent Framework in the lab — the same 5 steps applied to MAF.