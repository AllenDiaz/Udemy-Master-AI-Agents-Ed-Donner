# Introduction to CrewAI — Week 3 Overview

## Overview

Week 3 shifts focus to **CrewAI**, a popular open-source multi-agent framework. This lesson provides orientation on what CrewAI is, its different product offerings, and the two flavors of the open-source framework: **Crews** and **Flows**.

---

## What Is CrewAI?

CrewAI is actually three distinct things:

| Product | Description | Our Focus? |
|---|---|---|
| **CrewAI Enterprise** | Cloud platform for deploying, monitoring, and managing agents | ❌ |
| **CrewAI UI Studio** | Low-code/no-code tool for composing agent interactions visually | ❌ |
| **CrewAI Framework** | Open-source Python framework for orchestrating AI agents | ✅ |

> We focus exclusively on the **open-source framework** — writing code, building agents ourselves.

---

## CrewAI vs. OpenAI Agents SDK

Transitioning from OpenAI Agents SDK to CrewAI will feel unfamiliar at first — new terminology, new constructs. Key mindset:

- Much of the **core philosophy is similar** (agents, tools, orchestration)
- Differences exist in terminology and design patterns
- Different frameworks suit different projects — learn the strengths of each
- You'll naturally gravitate toward a personal favorite, and that's fine

---

## Two Flavors of the CrewAI Framework

### 1. CrewAI Crews (Our Focus)

Autonomous, team-based agent collaboration.

- A **Crew** = a team of agents with different roles working together
- Agents have autonomy to decide how they approach a problem
- Best for: **creative, exploratory, or autonomous problem-solving tasks**

### 2. CrewAI Flows

Prescribed, deterministic workflows.

- Fixed steps with decision points and defined outcomes
- Higher auditability and control
- Best for: **production systems requiring predictable, auditable behavior**

| | Crews | Flows |
|---|---|---|
| **Approach** | Autonomous | Deterministic |
| **Best for** | Exploration, creativity | Precise control, auditability |
| **Agent autonomy** | High | Low |
| **Predictability** | Lower | Higher |

> Flows likely emerged in response to production concerns around unpredictability in fully autonomous crew-based systems.

---

## Why CrewAI Needs to Monetize

Unlike OpenAI/Anthropic (who monetize via their models), CrewAI's revenue path is:
- **Open-source framework** → drives adoption
- **CrewAI Enterprise** → paid hosting, deployment, and management platform

This explains why their website leads with enterprise features — keep this context in mind when reading their docs.

---

## Key Takeaways

- CrewAI = open-source framework + enterprise platform + UI studio — we only use the framework
- A **Crew** is CrewAI's term for a team of collaborating agents
- **Crews** = autonomous; **Flows** = deterministic — we focus on Crews
- Core agentic concepts carry over from OpenAI Agents SDK — terminology differs, fundamentals don't
- Each framework has strengths — keep comparing as you learn

---

## Coming Up This Week

- CrewAI agents, tasks, and crews
- Defining roles, goals, and backstories for agents
- Tools in CrewAI
- Building autonomous multi-agent workflows with Crews