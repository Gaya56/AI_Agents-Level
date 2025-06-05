# AI Agents in 5 Levels of Difficulty (With Full Code Implementation)

About two weeks before a big product deadline, my prototype agent broke in the worst way.

*It looked fine*. It fetched data, called tools, and even explained its steps. But under the hood, it was bluffing. No real state, no memory, no reasoning. Just looping prompts pretending to be smart.

I only noticed when an edge case completely threw it off. That's when it hit me: I hadn't built an agent. I'd built a fancy prompt chain.

Fixing it meant redesigning the whole thing — not just chaining calls, but managing state, decisions, and long-term flow. Once that clicked, everything got simpler. The code, the logic, the results.

That's what this guide is about: breaking agent design into five practical levels of difficulty — each with working code.

Whether you're just starting out or trying to scale real-world tasks, this will help you avoid the traps I fell into and build agents that actually work.

The levels are:

- **Level 1: Agent with Tools and Instructions**
- **Level 2: Agent with Knowledge and Memory**
- **Level 3: Agent with Long-Term Memory and Reasoning**
- **Level 4: Multi-Agent Teams**
- **Level 5: Agentic Systems**

## 📁 Code Examples Index

This repository is organized for easy navigation and learning. Each level has its own folder with implementation files and documentation:

### 🔗 Quick Navigation Links

| Level | Description | Code Files | Documentation |
|-------|-------------|------------|---------------|
| **Level 1** | Basic Agents with Tools | [`agent_with_tools.py`](./level-1-basic/agent_with_tools.py) | [`README.md`](./level-1-basic/README.md) |
| **Level 2** | Knowledge + Memory | [`agent_with_knowledge_memory.py`](./level-2-knowledge-memory/agent_with_knowledge_memory.py) | [`README.md`](./level-2-knowledge-memory/README.md) |
| **Level 3** | Long-term Memory + Reasoning | [`agent_with_longterm_memory.py`](./level-3-longterm-reasoning/agent_with_longterm_memory.py) | [`README.md`](./level-3-longterm-reasoning/README.md) |
| **Level 4** | Multi-Agent Teams | [`multi_agent_teams.py`](./level-4-multi-agent/multi_agent_teams.py) | [`README.md`](./level-4-multi-agent/README.md) |
| **Level 5** | Agentic Systems | *Implementation varies* | [`README.md`](./level-5-agentic-systems/README.md) |

### 📚 Additional Resources

- [`docs/overview.md`](./docs/overview.md) - Complete project overview and setup guide
- Each level folder contains detailed README with usage instructions and key concepts

### 🚀 Getting Started

1. Start with **Level 1** for basic agent concepts
2. Progress sequentially through each level
3. Each level builds upon the previous one
4. Refer to individual README files for specific implementation details

Alright, let's dive in.

# **Level 1: Agent with Tools and Instructions**

> 📁 **Implementation**: [`level-1-basic/agent_with_tools.py`](./level-1-basic/agent_with_tools.py)  
> 📖 **Documentation**: [`level-1-basic/README.md`](./level-1-basic/README.md)

This is the basic setup — an LLM that follows instructions and calls tools in a loop. When people say, "*agents are just LLMs plus tool use*," they're talking about this level (and revealing how far they've explored).

Instructions tell the agent what to do. Tools let it take action — fetching data, calling APIs, or triggering workflows. It's simple, but already powerful enough to automate some tasks.

```python
from textwrap import dedent
from agno.agent import Agent 
from agno.models.openai import OpenAIChat 
from agno.tools.duckduckgo import DuckDuckGoTools

# Initialize basic agent with tools and instructions
agno_assist = Agent(
    name="Agno AGI",
    model=OpenAIChat(id="gpt-4.1"),  # Fixed typo: 0penAIChat -> OpenAIChat
    description=dedent("""\
        You are "Agno AGI, an autonomous AI Agent that can build agents using the Agno
        framework. Your goal is to help developers understand and use Agno by providing 
        explanations, working code examples, and optional visual and audio explanations
        of key concepts."""),
    instructions="Search the web for information about Agno.",
    tools=[DuckDuckGoTools()],  # Web search capability
    add_datetime_to_instructions=True, 
    markdown=True,
)

if __name__ == "__main__":
    # Ask the agent a question and stream the response
    agno_assist.print_response("What is Agno?", stream=True)
```

# Level 2: Agent with Knowledge and Memory

> 📁 **Implementation**: [`level-2-knowledge-memory/agent_with_knowledge_memory.py`](./level-2-knowledge-memory/agent_with_knowledge_memory.py)  
> 📖 **Documentation**: [`level-2-knowledge-memory/README.md`](./level-2-knowledge-memory/README.md)

Most tasks require information the model doesn't have. You can't stuff everything into context, so the agent needs a way to fetch knowledge at runtime — this is where agentic RAG or dynamic few-shot prompting comes in.

Search should be hybrid (full-text + semantic), and reranking is a must. Together, hybrid search + reranking is the best plug-and-play setup for agentic retrieval.

Storage gives the agent memory. LLMs are stateless by default; storing past actions, messages, and observations makes the agent stateful — able to reference what's happened so far and make better decisions.

```python
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.python import PythonTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.embedders.openai import OpenAIEmbedder
from agno.rerankers.cohere import CohereReranker
from agno.storage.sqlite import SqliteStorage

# Setup knowledge base with hybrid search and reranking
knowledge_base = UrlKnowledge(
    urls=["https://docs.agno.com/introduction.md"],
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,  # Combines full-text and semantic search
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        reranker=CohereReranker(model="rerank-multilingual-v3.0"),
    ),
)

# Setup persistent storage for agent sessions
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

# Create agent with knowledge and memory capabilities
agno_assist = Agent(
    name="Agno AGI",
    model=OpenAIChat(id="gpt-4.1"),
    description=dedent("""\
        You are "Agno AGI, an autonomous AI Agent that can build agents using the Agno
        framework. Your goal is to help developers understand and use Agno by providing 
        explanations, working code examples, and optional visual and audio explanations
        of key concepts."""),
    instructions="Search the web for information about Agno.",
    tools=[PythonTools(), DuckDuckGoTools()],
    add_datetime_to_instructions=True,
    knowledge=knowledge_base,  # Enables agentic RAG
    storage=storage,  # Persistent session storage
    add_history_to_messages=True,  # Include conversation history
    num_history_runs=3,  # Number of previous runs to include
    markdown=True,
)

if __name__ == "__main__":
    # Load the knowledge base (comment out after first run)
    # agno_assist.knowledge.load(recreate=True)
    agno_assist.print_response("What is Agno?", stream=True)
```

# Level 3: Agent with Long-Term Memory and Reasoning

> 📁 **Implementation**: [`level-3-longterm-reasoning/agent_with_longterm_memory.py`](./level-3-longterm-reasoning/agent_with_longterm_memory.py)  
> 📖 **Documentation**: [`level-3-longterm-reasoning/README.md`](./level-3-longterm-reasoning/README.md)

Memory lets agents recall details across sessions — like user preferences, past actions, or failed attempts — and adapt over time. This unlocks personalization and continuity. We're just scratching the surface here, but what excites me most is self-learning: agents that refine their behavior based on past experiences.

Reasoning takes things a step further.

It helps the agent break down problems, make better decisions, and follow multi-step instructions more reliably. It's not just about understanding — it's about increasing the success rate of each step. Every serious agent builder needs to know when and how to apply it.

```python
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.claude import Claude
from agno.tools.python import PythonTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.memory import Memory
from agno.memory.db.sqlite import SqliteMemoryDb
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.embedders.openai import OpenAIEmbedder
from agno.rerankers.cohere import CohereReranker
from agno.storage.sqlite import SqliteStorage

# Setup knowledge base (reusing from Level 2)
knowledge_base = UrlKnowledge(
    urls=["https://docs.agno.com/introduction.md"],
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        reranker=CohereReranker(model="rerank-multilingual-v3.0"),
    ),
)

# Setup long-term memory for user preferences and experiences
memory = Memory(
    model=OpenAIChat(id="gpt-4.1"),  # Model for creating memories
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
    delete_memories=True,  # Allow memory deletion
    clear_memories=True,   # Allow memory clearing
)

# Setup persistent storage
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

# Create agent with reasoning and long-term memory
agno_assist = Agent(
    name="Agno AGI",
    model=Claude(id="claude-3-7-sonnet-latest"),  # Claude for enhanced reasoning
    user_id="ava",  # User identifier for personalized memories
    description=dedent("""\
        You are "Agno AGI, an autonomous AI Agent that can build agents using the Agno
        framework. Your goal is to help developers understand and use Agno by providing 
        explanations, working code examples, and optional visual and audio explanations
        of key concepts."""),
    instructions="Search the web for information about Agno.",
    tools=[
        PythonTools(), 
        DuckDuckGoTools(), 
        ReasoningTools(add_instructions=True)  # Enhanced reasoning capabilities
    ],
    knowledge=knowledge_base,
    storage=storage,
    memory=memory,  # Long-term memory storage
    enable_agentic_memory=True,  # Let agent manage its own memories
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

if __name__ == "__main__":
    # Set user preference (agent will remember this)
    agno_assist.print_response("Always start your messages with 'hi ava'", stream=True)
    # Ask a question - agent will apply remembered preferences
    agno_assist.print_response("What is Agno?", stream=True)
```

# Level 4: Multi-Agent Teams

> 📁 **Implementation**: [`level-4-multi-agent/multi_agent_teams.py`](./level-4-multi-agent/multi_agent_teams.py)  
> 📖 **Documentation**: [`level-4-multi-agent/README.md`](./level-4-multi-agent/README.md)

Agents are most effective when they're focused — specialized in one domain with a tight toolset (ideally under 10). To tackle more complex or broad tasks, we combine them into teams. Each agent handles a piece of the problem, and together they cover more ground.

But there's a catch: without strong reasoning, the team leader falls apart on anything nuanced. Based on everything I've seen so far, autonomous multi-agent systems still don't work reliably. They succeed less than half the time — which isn't good enough.

That said, some architectures make coordination easier. [Agno](https://github.com/agno-agi/agno), for example, supports three execution modes — coordinate, route, and collaborate — along with built-in memory and context management. You still need to design carefully, but these building blocks make serious multi-agent work more feasible.

```python
from textwrap import dedent
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.models.claude import Claude
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools

# Specialized web search agent
web_agent = Agent(
    name="Web Search Agent",
    role="Handle web search requests",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources in your responses.",
)

# Specialized financial data agent
finance_agent = Agent(
    name="Finance Agent",
    role="Handle financial data requests",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[YFinanceTools()],
    instructions=[
        "You are a financial data specialist. Provide concise and accurate data.",
        "Use tables to display stock prices, fundamentals (P/E, Market Cap)",
    ],
)

# Team leader with reasoning capabilities
team_leader = Team(
    name="Reasoning Finance Team Leader",
    mode="coordinate",  # Coordinate between specialized agents
    model=Claude(id="claude-3-7-sonnet-latest"),
    members=[web_agent, finance_agent],  # Team members
    tools=[ReasoningTools(add_instructions=True)],  # Enhanced reasoning
    instructions=[
        "Use tables to display data",
        "Only output the final answer, no other text.",
    ],
    show_members_responses=True,  # Show individual agent responses
    enable_agentic_context=True,  # Context management across agents
    add_datetime_to_instructions=True,
    success_criteria="The team has successfully completed the task.",
)

if __name__ == "__main__":
    # Complex multi-step analysis task
    analysis_query = dedent("""\
        Analyze the impact of recent US tariffs on market performance across
        these key sectors:
        - Steel & Aluminum: (X, NUE, AA)
        - Technology Hardware: (AAPL, DELL, HPQ)

        For each sector:
        1. Compare stock performance before and after tariff implementation
        2. Identify supply chain disruptions and cost impact percentages
        3. Analyze companies' strategic responses (reshoring, price adjustments, supplier
        diversification)""")
    
    team_leader.print_response(
        analysis_query,
        stream=True,
        stream_intermediate_steps=True,  # Show progress from each agent
        show_full_reasoning=True,  # Display reasoning process
    )
```

# Level 5: Agentic Systems

> 📁 **Implementation**: *System-level architecture (varies by implementation)*  
> 📖 **Documentation**: [`level-5-agentic-systems/README.md`](./level-5-agentic-systems/README.md)

This is where agents go from being tools to infrastructure. Agentic Systems are full APIs — systems that take in a user request, kick off an async workflow, and stream results back as they become available.

Sounds clean in theory. In practice, it's hard. Really hard.

You need to persist state when the request comes in, spin up a background job, track progress, and stream output as it's generated. Websockets can help, but they're tricky to scale and maintain. Most teams underestimate the backend complexity here.

This is what it takes to turn agents into real products. At this level, you're not building a feature — you're building a system.

# From Demo Fails to Real Wins: Key Lessons in Agent Design

Building AI agents isn't about chasing hype or stacking features — it's about getting the fundamentals right. Each level, from basic tool use to fully asynchronous agentic systems, adds power *only* when the underlying architecture is sound.

Most failures don't come from missing the latest framework. They come from ignoring the basics: clear boundaries, solid reasoning, effective memory, and knowing when to let humans take the wheel.

If you start simple, build up with purpose, don't overcomplicate upfront and add complexity only when it solves a real problem, you won't just build something cool — you'll build something that works.

---

## 🔄 Navigation & Next Steps

### 📁 Explore the Code Examples

All implementations are organized in dedicated folders:

- [`level-1-basic/`](./level-1-basic/) - Start here for basic agent concepts
- [`level-2-knowledge-memory/`](./level-2-knowledge-memory/) - Add knowledge and memory
- [`level-3-longterm-reasoning/`](./level-3-longterm-reasoning/) - Implement reasoning
- [`level-4-multi-agent/`](./level-4-multi-agent/) - Build agent teams
- [`level-5-agentic-systems/`](./level-5-agentic-systems/) - Create full systems

### 📚 Additional Resources

- [`docs/overview.md`](./docs/overview.md) - Complete setup guide and requirements
- Each folder contains detailed README with usage instructions

### 🚀 Quick Start Sequence

1. **Read this article** for conceptual understanding
2. **Start with Level 1** - Basic implementation
3. **Progress sequentially** through each level
4. **Experiment and modify** the code for your use case
5. **Build incrementally** - don't skip to complex levels too quickly

Remember: Each level builds upon the previous one. Master the fundamentals before adding complexity.