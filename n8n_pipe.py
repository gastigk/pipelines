{
  "name": "Local RAG Agent - Local Folder",
  "nodes": [
    {
      "parameters": {
        "path": "/tu/carpeta/archivos",
        "watchInterval": 60
      },
      "id": "LocalFileTrigger",
      "name": "Local File Trigger",
      "type": "n8n-nodes-base.localFileTrigger",
      "typeVersion": 1,
      "position": [200, 300]
    },
    {
      "parameters": {
        "filePath": "={{ $json[\"path\"] }}"
      },
      "id": "ReadBinaryFile",
      "name": "Read Binary File",
      "type": "n8n-nodes-base.readBinaryFile",
      "typeVersion": 1,
      "position": [400, 300]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "ExtractText",
      "name": "Extract Document Text",
      "type": "n8n-nodes-langchain.extractTextFromFile",
      "typeVersion": 1,
      "position": [600, 300]
    },
    {
      "parameters": {
        "chunkSize": 500,
        "chunkOverlap": 50,
        "textProperty": "text"
      },
      "id": "TextSplitter",
      "name": "Recursive Character Text Splitter",
      "type": "n8n-nodes-langchain.textSplitterRecursiveCharacter",
      "typeVersion": 1,
      "position": [800, 300]
    },
    {
      "parameters": {
        "model": "llama2",
        "textProperty": "text"
      },
      "id": "Embeddings",
      "name": "Embeddings Ollama",
      "type": "n8n-nodes-langchain.embeddingsOllama",
      "typeVersion": 1,
      "position": [1000, 300]
    },
    {
      "parameters": {
        "collection": "local_knowledge",
        "operation": "insert"
      },
      "id": "InsertQdrant",
      "name": "Qdrant Vector Store Insert",
      "type": "n8n-nodes-langchain.vectorStoreQdrant",
      "typeVersion": 1,
      "position": [1200, 300]
    }
  ],
  "connections": {
    "Local File Trigger": {
      "main": [
        [
          {
            "node": "Read Binary File",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Read Binary File": {
      "main": [
        [
          {
            "node": "Extract Document Text",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Document Text": {
      "main": [
        [
          {
            "node": "Recursive Character Text Splitter",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Recursive Character Text Splitter": {
      "main": [
        [
          {
            "node": "Embeddings Ollama",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Embeddings Ollama": {
      "main": [
        [
          {
            "node": "Qdrant Vector Store Insert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}