# Level 2: Agent with Knowledge and Memory

... imports
# You can also use https://docs.agno.com/llms-full.txt for the full documentation
knowledge_base = UrlKnowledge(
  urls=["https://docs.agno.com/introduction.md"],
  vector_db=LanceDb(
    uri="tmp/lancedb",
    table_name="agno_docs",
    search_type=SearchType.hybrid,
    embedder=0penAIEmbedder(id="text-embedding-3-small"),
    reranker=CohereReranker(model="rerank-multilingual-v3.0"),
  ),
)
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

agno_assist = Agent(
  name="Agno AGI",
  model=OpenAIChat(id="gpt-4.1"),
  description=..., 
  instructions=...,
  tools=[PythonTools(), DuckDuckGoTools()],
  add_datetime_to_instructions=True,
  # Agentic RAG is enabled by default when 'knowledge' is provided to the Agent.
  knowledge=knowledge_base,
  # Store Agent sessions in a sqlite database
  storage=storage,
  # Add the chat history to the messages
  add_history_to_messages=True,
  # Number of history runs
  num_history_runs=3, 
  markdown=True,
)

if __name_ == "__main__":
  # Load the knowledge base, comment after first run
  # agno_assist.knovledge.load(recreate=True)
  agno _assist.print_response("What is Agno?", stream=True)
