# 📘 Agent Patterns (Day 2 – Part 2)

## Overview
Unlike **workflows**, which follow predefined paths, **agent patterns** are **open-ended, dynamic, and autonomous**. They allow LLMs to interact with environments, make decisions, and adapt continuously — but introduce unpredictability in cost, time, and output quality.

---

## 🔑 Key Concepts

### **Agents**
- **Definition**: Systems where LLMs dynamically direct their own processes and actions.
- **Characteristics**:
  - Open-ended loops with feedback.
  - No fixed sequence of steps.
  - Greater flexibility and problem-solving capacity.
  - Less predictable outcomes.

### **Environment Interaction**
- Human provides input → LLM acts on environment → environment returns feedback → LLM continues loop.
- Example: LLM controlling smart devices (e.g., lights).

---

## 📖 Important Distinctions
- **Workflows**: Structured, predictable, step-based.
- **Agents**: Fluid, adaptive, autonomous, potentially indefinite loops.

---

## ⚠️ Challenges of Agent Patterns
- **Unpredictable paths**: Unknown sequence of tasks.
- **Uncertain outputs**: No guarantee of quality or completion.
- **Variable costs**: API usage may escalate unexpectedly.
- **Time unpredictability**: Unknown duration to finish tasks.

---

## 🛡️ Mitigations

### **Monitoring**
- Provides visibility into agent interactions.
- Tools: OpenAI SDK tracing, LangSmith graphs.

### **Guardrails**
- Software constraints ensuring safe, consistent behavior.
- Example: OpenAI Agents SDK guardrails enforce boundaries.


