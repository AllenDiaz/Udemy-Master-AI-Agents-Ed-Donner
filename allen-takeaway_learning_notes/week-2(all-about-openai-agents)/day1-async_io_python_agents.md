# Async IO in Python — Essential for AI Agent Frameworks

## Overview

Before diving into the OpenAI Agents SDK (Week 2), this lesson covers **asynchronous Python (`async`/`await`)** — a concept used universally across all major agent frameworks. Understanding it properly (not just memorizing rules) makes working with any agentic framework significantly easier.

---

## Why Async IO Matters for AI Agents

- All major agent frameworks use `async` Python
- LLM API calls (e.g. OpenAI) are **IO-bound** — most time is spent *waiting* on network responses
- Multi-agent systems may fire off many concurrent LLM requests simultaneously
- Async IO handles this efficiently with minimal resource overhead

---

## Key Concepts

### What Is Async IO?

A **lightweight alternative to multithreading or multiprocessing** built into Python (since v3.5).

| Approach | Level | Overhead |
|---|---|---|
| Multiprocessing | OS process level | High |
| Multithreading | OS thread level | Medium |
| **Async IO** | Python code level | Very Low ✅ |

> Async IO doesn't use OS threads. It uses a **single-threaded event loop** that manually switches between tasks when one is blocked (e.g. waiting on a network response).

---

## The Two Core Keywords

### `async`

Marks a function as a **coroutine** — something Python can pause and resume.

```python
# Regular function
def do_some_processing():
    return "done"

# Coroutine (async function)
async def do_some_processing():
    return "done"
```

> ⚠️ Technically, `async def` no longer defines a *function* — it defines a **coroutine**.

---

### `await`

Schedules a coroutine for execution and **blocks until it completes**, allowing the event loop to run other coroutines in the meantime.

```python
# Calling a regular function — runs immediately
result = do_some_processing()

# Calling a coroutine — returns a coroutine OBJECT, does NOT run
my_coroutine = do_some_processing()  # ❌ Nothing executes

# Correct way — schedules and runs the coroutine
result = await do_some_processing()  # ✅ Runs and returns "done"
```

---

## How the Event Loop Works

1. An **event loop** (from the `asyncio` package) runs as a `while` loop
2. It picks up scheduled coroutines and starts executing them **one at a time**
3. When a coroutine hits an IO wait (e.g. waiting for an OpenAI response), the event loop **pauses it**
4. It then picks up and runs another waiting coroutine
5. Once the paused coroutine's IO resolves, it resumes

> Think of it as **manual multithreading** — not at the OS level, but at the code level, triggered by IO blocking.

---

## Running Coroutines Concurrently: `asyncio.gather()`

Using just `await` alone is still sequential. To run multiple coroutines **concurrently**, use `asyncio.gather()`:

```python
import asyncio

results = await asyncio.gather(
    coroutine_one(),
    coroutine_two(),
    coroutine_three()
)
# results is a list of all three return values
```

- All three coroutines are scheduled together
- While one waits on IO, the others make progress
- Returns a list of results in order

---

## Quick Reference: The Rules

| Situation | Rule |
|---|---|
| Defining an async function | Use `async def` instead of `def` |
| Calling an async function | Always use `await` before it |
| Running multiple coroutines concurrently | Use `await asyncio.gather(...)` |
| Inside a non-async context (e.g. script entry point) | Use `asyncio.run(main())` |

---

## Mental Model Summary

```
Regular function call  →  Runs immediately, returns value
Coroutine call         →  Returns a coroutine object (nothing runs yet)
await coroutine        →  Schedules it, blocks here until done, returns value
asyncio.gather(...)    →  Schedules many at once, runs concurrently via event loop
```

---

## Key Takeaways

- `async`/`await` is **not optional** in agent frameworks — it's everywhere
- It's not true parallelism, but it's highly effective for **IO-bound** workloads (which LLM calls are)
- Understanding the event loop model removes all confusion about why these keywords exist
- Thousands of concurrent coroutines are possible with minimal overhead

---

## Related Concepts to Explore

- `asyncio.run()` — entry point for async programs
- `asyncio.gather()` vs `asyncio.create_task()`
- OpenAI Agents SDK async patterns
- IO-bound vs CPU-bound concurrency