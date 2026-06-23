# Vibe Coding — Tips for Coding Effectively with LLMs

## Overview

**Vibe coding** (coined by Andrej Karpathy) is the practice of fluidly generating, tweaking, and iterating on code with LLM assistance — letting the model do the heavy lifting while you steer. This lesson provides five practical tips to do it well and avoid common pitfalls.

---

## The Five Tips

### 1. 🎯 Good Vibes — Craft a Reusable Prompt

Invest time in writing a strong base prompt you can reuse across sessions.

**Include:**
- A request for **concise, clean code** (LLMs default to verbose, over-engineered output)
- **Today's date** — explicitly ask for APIs current as of that date to avoid outdated patterns

```
"Please write concise, clean code. Use APIs that are current as of [today's date]."
```

---

### 2. ✅ Vibe but Verify — Ask Multiple LLMs

Don't rely on a single LLM's answer. Cross-check with two or three models (e.g. ChatGPT + Claude).

- One answer may be verbose or miss the point
- Another may be spot-on
- Comparing responses builds better understanding and catches errors early

---

### 3. 🪜 Step Up the Vibe — Work in Small Chunks

**Never generate 200 lines of code and then ask why it's broken.**

Instead:
- Break the problem into **small, independently testable pieces** (~10 lines at a time)
- Ask the LLM to generate code **function by function**
- Request a test alongside each piece to verify it works before moving on

> 💡 If you can't figure out how to break the problem down, ask the LLM to do it for you — but tell it **not** to write any code yet. Ask it to outline 4–5 bite-sized steps first, then tackle each one separately.

---

### 4. 🔍 Vibe and Validate — Use a Second LLM to Review

After getting an answer, paste it into a **different LLM** and ask:

> *"I asked this question and got this answer. Are there any bugs? Is there a cleaner or more concise approach?"*

- Mirrors the **evaluator-optimizer** agentic design pattern — applied manually to your own workflow
- Often catches bugs or simplifies overly complex code

---

### 5. 🎨 Vibe with Variety — Ask for Multiple Solutions

Instead of asking for *one* solution, ask for **three different approaches** to the same problem.

Benefits:
- Forces the model to think beyond its default approach
- Often surfaces a better or more elegant solution
- Asking for rationale/explanation alongside each variant deepens your own understanding

---

## Bonus Tip (Unlisted)

> Always ask the LLM to **explain the code it generates** until you fully understand every line.

Vibe coding is fun and productive — but if something breaks and you don't understand the code, debugging becomes painful. Stay in touch with what's actually happening.

---

## Key Takeaways

| Tip | Core Idea |
|---|---|
| Good Vibes | Strong, reusable prompts with date context |
| Vibe but Verify | Cross-check answers across multiple LLMs |
| Step Up the Vibe | Small chunks, test as you go |
| Vibe and Validate | Use a second LLM as a code reviewer |
| Vibe with Variety | Request multiple solutions to find the best one |

---

## Related Concepts

- Evaluator-optimizer design pattern (parallels "vibe and validate")
- Prompt engineering best practices
- Iterative development / test-driven development