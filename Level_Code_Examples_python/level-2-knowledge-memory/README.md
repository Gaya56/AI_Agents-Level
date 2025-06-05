# Level 2: Agent with Knowledge and Memory

Most tasks require information the model doesn't have. This level introduces agentic RAG (Retrieval-Augmented Generation) and persistent memory to make agents stateful and knowledgeable.

## Key Features
- Hybrid search (full-text + semantic)
- Vector database integration with LanceDB
- Reranking for better retrieval
- SQLite storage for session persistence
- Chat history management

## Files
- `agent_with_knowledge_memory.py` - Agent with RAG and memory capabilities

## Usage
This level shows how to:
- Set up knowledge bases with URL ingestion
- Configure hybrid search with embeddings and reranking
- Persist agent sessions across interactions
- Maintain conversation history
