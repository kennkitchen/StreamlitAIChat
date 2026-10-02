#!/usr/bin/bash
docker run --name lamaqd -d -p 6333:6333 -p 6334:6334 \
-v "$(pwd)/data/qdrant_storage:/data/qdrant/storage:z" \
qdrant/qdrant
uv run streamlit run main.py
