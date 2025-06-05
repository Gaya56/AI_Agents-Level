# Level 3: Agent with Long-Term Memory and Reasoning

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
