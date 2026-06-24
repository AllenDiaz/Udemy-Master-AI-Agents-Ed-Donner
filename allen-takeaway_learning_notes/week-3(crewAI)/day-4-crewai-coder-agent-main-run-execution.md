# CrewAI — Running the Coder Agent (main.py & Live Execution)

## Overview

This lesson completes the coder agent by writing `main.py` and running a real coding challenge — calculating an approximation of pi using the Leibniz formula — to verify that the agent genuinely executes code rather than just pretending to.

---

## `main.py`

```python
from coder.crew import CoderCrew

assignment = """
Write a Python program to calculate the first 10,000 terms of the series:
1 - 1/3 + 1/5 - 1/7 + ...
Multiply the total by 4.
Print the result.
"""

inputs = {"assignment": assignment}

result = CoderCrew().crew().kickoff(inputs=inputs)
print(result.raw)
```

Run with:
```bash
crewai run
```

---

## Why This Assignment?

A simple "Hello World" challenge wouldn't prove real execution — LLMs know the output without running anything. The Leibniz formula for pi was chosen because:

- The LLM can recognize it as a pi approximation
- But **10,000 terms yields a slightly wrong answer** (~3.14149, not 3.14159)
- Only by actually running the code can the agent produce the correct approximation
- This proves genuine code execution rather than fabricated output

---

## What the Agent Did

1. **Planned** the approach — recognized the alternating series pattern
2. **Wrote** clean Python using `(-1)**i` trick for alternating signs
3. **Executed** the code in Docker — first attempt failed, retried automatically
4. **Produced** the correct approximation: `3.14149...`

```python
# Generated code (approximate)
num_terms = 10000
total = sum((-1)**i / (2*i + 1) for i in range(num_terms))
result = total * 4
print(result)  # → 3.14149265...
```

---

## Output File

```
outputs/code_and_output.txt
```

Contains:
- The full Python code written by the agent
- The actual output produced by running it

---

## Key Observations

| | Detail |
|---|---|
| First attempt | Failed — Docker container started, code errored |
| Retry | Automatic — agent corrected and reran |
| Result | ~3.14149 — correct for 10,000 terms of Leibniz |
| Proof of execution | Wrong decimal places confirm real computation, not fabrication |

---

## Key Takeaways

- Use a challenge with a **verifiable but non-obvious output** to confirm real code execution
- Automatic retries (`max_retry_limit`) mean the agent self-corrects without intervention
- The output file captures both code and result — useful for review and audit
- The entire workflow (plan → write → execute → output) happens autonomously
- CrewAI handles Docker container lifecycle entirely behind the scenes

---

## Up Next

Extending the single coder agent into a full **engineering crew** — multiple agents working together to solve problems end to end.