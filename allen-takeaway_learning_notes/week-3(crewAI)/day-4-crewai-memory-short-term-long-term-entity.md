# CrewAI — Memory (Short-Term, Long-Term & Entity)

## Overview

This lesson adds **memory** to the stock picker crew, covering CrewAI's five memory types and implementing the three most practical ones: short-term, long-term, and entity memory.

---

## CrewAI's Five Memory Types

| Type | Storage | Purpose |
|---|---|---|
| **Short-term** | Vector DB (ChromaDB via RAG) | Recent interactions — retrieved via similarity search |
| **Long-term** | SQLite database | Important info persisted across sessions |
| **Entity** | Vector DB (ChromaDB via RAG) | Info about people, places, concepts |
| **Contextual** | Umbrella term | Combines short-term + long-term + entity, passed as context |
| **User** | Manual | User-specific info — mostly left to developer to manage |

> At the end of the day, memory = **more relevant context shoved into the prompt**. The magic is in the retrieval — finding and inserting the right prior information automatically.

**Trade-off of using CrewAI's memory abstractions:**
- ✅ Get up and running quickly, complex setup handled automatically
- ❌ Less visibility into what's actually in the prompt — harder to debug

---

## Implementation

### Imports

```python
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RagStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
```

### Creating Memory Objects

```python
short_term_memory = ShortTermMemory(
    storage=RagStorage(
        provider="openai",
        model="text-embedding-3-small",
        type="short_term",
        path="memory/"
    )
)

long_term_memory = LongTermMemory(
    storage=LTMSQLiteStorage(path="memory/long_term.db")
)

entity_memory = EntityMemory(
    storage=RagStorage(
        provider="openai",
        model="text-embedding-3-small",
        type="entities",
        path="memory/"
    )
)
```

### Passing Memory to the Crew

```python
@crew
def crew(self) -> Crew:
    manager = Agent(...)

    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.hierarchical,
        manager_agent=manager,
        memory=True,                          # ← enable memory
        short_term_memory=short_term_memory,
        long_term_memory=long_term_memory,
        entity_memory=entity_memory,
        verbose=True
    )
```

### Enabling Memory on Individual Agents

Not all agents need memory — be selective:

```python
@agent
def trending_company_finder(self) -> Agent:
    return Agent(
        config=self.agents_config["trending_company_finder"],
        tools=[SerperDevTool()],
        memory=True    # ← remembers companies it has surfaced before
    )

@agent
def financial_researcher(self) -> Agent:
    return Agent(
        config=self.agents_config["financial_researcher"],
        tools=[SerperDevTool()]
        # No memory — should do fresh research every time
    )

@agent
def stock_picker(self) -> Agent:
    return Agent(
        config=self.agents_config["stock_picker"],
        tools=[PushNotificationTool()],
        memory=True    # ← avoids recommending the same stock twice
    )
```

---

## Files Created at Runtime

```
memory/
├── chroma/          # ChromaDB vector store (short-term + entity)
└── long_term.db     # SQLite database (long-term)
```

---

## YAML Prompts + Memory

Memory only works as well as the prompts that tell agents to use it. Reinforce in YAML:

```yaml
trending_company_finder:
  goal: Find 2-3 trending companies. Surface new companies you have not found before.

stock_picker:
  goal: Pick the best company. Do not pick the same company twice.
```

> Memory inserts relevant past context into the prompt — but the agent still needs instructions to act on it.

---

## Stock Picker Project — Full Feature Summary

| Feature | How Implemented |
|---|---|
| Structured outputs | `output_pydantic=` on tasks |
| Built-in tool | `SerperDevTool()` for web search |
| Custom tool | `PushNotificationTool` via `BaseTool` subclass |
| Hierarchical process | `Process.hierarchical` + `manager_agent` |
| Memory | `ShortTermMemory` + `LongTermMemory` + `EntityMemory` |

---

## Key Takeaways

- `memory=True` on the `Crew` enables the memory system; `memory=True` on individual `Agent`s opts them in
- Short-term and entity memory use **ChromaDB** (vector similarity search); long-term uses **SQLite**
- Memory is a CrewAI abstraction — powerful but less transparent than managing context manually
- Be selective: only give memory to agents that genuinely benefit from it
- Prompts must explicitly instruct agents to use prior knowledge — memory alone isn't enough

---

## Up Next

The **developer agent** project — a new crew designed to assist with software development tasks.