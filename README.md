# StreamlitAIChat
This is mostly just a testing/learning project at the moment.

## Requirements
1. Requires a local installation of Ollama on the machine where this code is running.
2. Uses SQLite (it will create the database if it doesn't exist in the `data` directory).
3. If I get around to adding vector search, it will use Qdrant (via Docker).
4. Ergo, if 3 is implemented, it will require Docker.

Note: I'm developing and testing from Linux (CachyOS to be specific).

## FAQ
**Q.** Why Qdrant and not Chroma?

**A.** Chroma is a vector database that is designed for use with large language models (LLMs) and is optimized for fast and efficient vector search. It is a popular choice for building vector databases for LLM applications. However, Qdrant is another vector database that is also designed for use with LLMs and is known for its high performance and scalability. It is also a popular choice for building vector databases for LLM applications. The choice between Chroma and Qdrant ultimately depends on the specific requirements of the application and the preferences of the developer.

Also, I forgot about Chroma and just did a search and discovered Qdrant and thought I'd give it a try.

**Q.** Why is Qdrant in Docker but not Ollama?

**A.** Ollama should have access to your GPU (if you have one) so it can take advantage of it for faster inference. Qdrant, on the other hand, is a vector database and does not require GPU access for its operations.

Also, if you're interested in running local AI, you're probably already using Ollama. Qdrant is more of an edge-case for local AI, as it is primarily used for vector search and retrieval, which is not a common use case for local AI applications. Ergo, there's probably no need for you to have it locally installed.
