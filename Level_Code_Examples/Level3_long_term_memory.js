# Level 3: Agent with Long-Term Memory and Reasoning
... imports

knowledge_base = ...

memory = Memory(
  # Use any model for creating nemories
  model=0penAIChat(id="gpt-4.1"),
  db=SqliteMemoryDb(table_name="user_menories", db_file="tmp/agent.db"),
  delete_memories=True, 
  clear_memories=True,
)

  storage =

agno_assist = Agent(
  name="Agno AGI",
  model=Claude (id="claude-3-7-sonnet-latest"),
  # User for the memories
  user_id="ava", 
  description=..., 
  instructions=...,
  # Give the Agent the ability to reason
  tools=[PythonTools(), DuckDuckGoTools(), 
  ReasoningTools(add_instructions=True)],
  ...
  # Store memories in a sqlite database
  memory=memory,
  # Let the Agent manage its menories
  enable_agentic_memory=True,
)

if __name__ == "__main__":
  # You can comment this out after the first run and the agent will remember
  agno_assist.print_response("Always start your messages with 'hi ava'", stream=True)
  agno_assist.print_response("What is Agno?", stream=True)
