# 📘 Day 3 Lesson: Orchestrating LLMs

## Overview
Day 3 shifts back to **practical coding**. The focus is on **orchestrating multiple LLMs** — both paid APIs and open-source models — across cloud and local environments. Learners gain flexibility in choosing models and practice debugging real-world orchestration challenges.

---

## 🔑 Key Concepts

### **Model Orchestration**
- Involves calling multiple LLMs in sequence or parallel.
- Can mix **closed-source APIs** (e.g., GPT-4, Claude) with **open-source models** (e.g., LLaMA, DeepSeek).
- Flexibility: learners can swap models depending on cost, performance, or availability.

### **Closed vs Open Source Models**
- **Closed-source**: GPT-4, Claude, Gemini Pro — higher performance, paid APIs.
- **Open-source**: LLaMA, DeepSeek distilled versions — free, run locally, performance varies.

---

## 📖 Models Covered

- **OpenAI**: GPT-4 mini, GPT-4, reasoning models (o1, o3 mini).
- **Anthropic**: Claude 3.7 Sonnet (main), Claude 3 Haiku (cheaper).
- **Google**: Gemini 2.0 Flash (free tier), Gemini Pro.
- **DeepSeek**: V3 and R1 (innovative training efficiency, open-sourced distilled versions).
- **Grok**:
  - Grok (X/Twitter) → proprietary.
  - Groq (with Q) → infrastructure for fast inference (e.g., LLaMA 3.3).
- **Ollama**: Local platform for running open-source models via optimized C++ (llama.cpp).

---

## ⚙️ Practical Applications

- **Manual Agent Workflow**:  
  Ask ChatGPT and Claude the same question → use one as evaluator (Evaluator–Optimizer pattern).
- **Local Deployment**:  
  Run LLaMA or DeepSeek distilled models locally via Ollama.
- **Leaderboard Reference**:  
  Vellum Leaderboard compares models by:
  - Cost (per token).
  - Context window size.
  - Benchmark performance.

---

## 🛠️ Developer Guidance

- Expect **roadblocks** → debugging is where real learning happens.
- Use **labs and GitHub repo** for updated guides and troubleshooting.
- Monitor **leaderboards** for model performance and cost efficiency.
- Apply **guardrails and monitoring** when orchestrating multiple agents.

---

## 📚 Reference
- Vellum Leaderboard: benchmarking closed vs open-source models.
- Anthropic & OpenAI SDKs: orchestration, tracing, guardrails.


