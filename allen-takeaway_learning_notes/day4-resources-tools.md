Here’s a structured Markdown summary of **Day 4 – Resources and Tools**, formatted for your notes and GitHub documentation.

---

# 📘 Day 4 Lesson: Resources and Tools

## Overview
Day 4 explores two critical components of **Agentic AI**:  
- **Resources** → providing LLMs with extra context to improve expertise.  
- **Tools** → granting LLMs the ability to take actions autonomously.  

This lesson emphasizes how these mechanisms enhance agent effectiveness and autonomy.

---

## 🔑 Key Concepts

### **Resources**
- Definition: Additional context or information injected into prompts.  
- Purpose: Improves accuracy and relevance of LLM responses.  
- Example: Airline support agent → include ticket price data in the prompt.  
- Advanced Technique: **RAG** (Retrieval-Augmented Generation) → retrieves only the most relevant context rather than dumping all data.

---

### **Tools**
- Definition: Capabilities given to LLMs to perform actions (e.g., SQL queries, API calls, device control).  
- Purpose: Enables autonomy by allowing LLMs to decide when to use tools.  
- Mechanism:
  - LLM is prompted with available tools.
  - Responds in **JSON** specifying desired action.
  - Code executes the tool → returns result → LLM continues.  
- Example:  
  - User asks: *“How much is a flight to Paris?”*  
  - LLM responds: `Use tool to fetch ticket price for Paris`.  
  - Code executes query → returns price → LLM integrates result into final answer.  

---

## 📖 Important Distinctions
- **Resources**: Context injection → improves knowledge.  
- **Tools**: Action execution → grants autonomy.  
- Together: Resources + Tools = more capable, autonomous agents.

---

## ⚙️ Practical Applications
- **Resource Use**: Customer support bots with company-specific data.  
- **Tool Use**: LLMs querying databases, sending messages, or controlling devices.  
- **Hybrid**: Combine resources (context) with tools (actions) for robust agent workflows.

---

## 📚 Reference
- Anthropic: *Building Effective Agents* (frameworks and autonomy).  
- OpenAI: Tool calling via JSON responses.  
- RAG: Retrieval-Augmented Generation for context relevance.
