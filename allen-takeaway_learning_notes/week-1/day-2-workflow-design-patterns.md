
# 📘 Workflow Design Patterns (Agentic Systems)

## Overview
Anthropic identifies **five workflow design patterns** within agentic systems. These patterns show how LLMs and code can be orchestrated to solve tasks in structured ways.

---

## 🔑 Key Patterns

### **Prompt Chaining**
- **Definition**: Sequential LLM calls, each handling a subtask.
- **Structure**: Input → LLM → (optional code) → next LLM → output.
- **Example**:  
  1. LLM chooses a business sector.  
  2. LLM identifies pain points.  
  3. LLM proposes solutions.  
- **Benefit**: Precise framing of each step; guardrails for accuracy.  
- **Note**: Though classified as workflow, autonomy can emerge when the first LLM decides topics.

---

### **Routing**
- **Definition**: An LLM acts as a router, directing tasks to specialized models.  
- **Structure**: Input → Router LLM → Specialist LLM (1, 2, or 3).  
- **Benefit**: Separation of concerns; tasks handled by domain experts.  
- **Autonomy**: Router makes decisions, though within guardrails.

---

### **Parallelization**
- **Definition**: Code splits tasks into subtasks executed concurrently by multiple LLMs.  
- **Structure**: Input → Code → Parallel LLM calls → Aggregator code → Output.  
- **Example**:  
  - Same task repeated 3 times → aggregator averages results.  
  - Different subtasks executed simultaneously.  
- **Benefit**: Efficiency and speed; supports redundancy and consensus.

---

### **Orchestrator–Worker**
- **Definition**: An LLM orchestrates task decomposition and synthesis.  
- **Structure**: Orchestrator LLM → Worker LLMs → Synthesizer LLM → Output.  
- **Benefit**: Dynamic breakdown of complex tasks; flexible recombination.  
- **Note**: Blurs line between workflow and agent due to orchestrator’s discretion.

---

### **Evaluator–Optimizer**
- **Definition**: Feedback loop where one LLM generates and another evaluates.  
- **Structure**: Generator LLM → Evaluator LLM → Accept/Reject → Feedback → Generator retry.  
- **Benefit**: Improves accuracy, robustness, and reliability.  
- **Application**: Common in production systems to validate outputs.  
- **Example**: Evaluator rejects flawed answers, provides reason, generator retries.

---

## 📚 Reference
- Anthropic: *Building Effective Agents* (workflow design patterns).
