# Level 2: Agent with Knowledge and Memory

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
