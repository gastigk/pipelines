{
  "name": "Local RAG AI Agent",
  "nodes": [
    {
      "parameters": {},
      "id": "99b30fd7-b36c-44ba-9daa-408585aaaee9",
      "name": "Postgres Chat Memory",
      "type": "@n8n/n8n-nodes-langchain.memoryPostgresChat",
      "typeVersion": 1.1,
      "position": [
        1040,
        560
      ],
      "credentials": {
        "postgres": {
          "id": "iN7fO2CgatVwq73z",
          "name": "Postgres account"
        }
      }
    },
    {
      "parameters": {
        "model": "llama3.1:latest",
        "options": {}
      },
      "id": "c7632a7c-2661-492e-bd6f-aab994818998",
      "name": "Ollama Chat Model",
      "type": "@n8n/n8n-nodes-langchain.lmChatOllama",
      "typeVersion": 1,
      "position": [
        920,
        560
      ],
      "credentials": {
        "ollamaApi": {
          "id": "eOwAotC7AUgJlvHM",
          "name": "Ollama account"
        }
      }
    },
    {
      "parameters": {
        "model": "llama3.1:latest",
        "options": {}
      },
      "id": "73d773a4-5c72-4af3-a52d-144f0e417823",
      "name": "Ollama Model",
      "type": "@n8n/n8n-nodes-langchain.lmOllama",
      "typeVersion": 1,
      "position": [
        1960,
        500
      ],
      "credentials": {
        "ollamaApi": {
          "id": "eOwAotC7AUgJlvHM",
          "name": "Ollama account"
        }
      }
    },
    {
      "parameters": {
        "name": "documents",
        "topK": 3
      },
      "id": "3f882fa7-c8ed-4531-b236-a34c16c55838",
      "name": "Vector Store Tool",
      "type": "@n8n/n8n-nodes-langchain.toolVectorStore",
      "typeVersion": 1,
      "position": [
        1740,
        340
      ]
    },
    {
      "parameters": {
        "model": "nomic-embed-text:latest"
      },
      "id": "3a8e3fa0-3997-4bce-985c-975fb5ad4013",
      "name": "Embeddings Ollama",
      "type": "@n8n/n8n-nodes-langchain.embeddingsOllama",
      "typeVersion": 1,
      "position": [
        1840,
        600
      ],
      "credentials": {
        "ollamaApi": {
          "id": "eOwAotC7AUgJlvHM",
          "name": "Ollama account"
        }
      }
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "10646eae-ae46-4327-a4dc-9987c2d76173",
              "name": "file_id",
              "value": "={{ $json.id }}",
              "type": "string"
            },
            {
              "id": "dd0aa081-79e7-4714-8a67-1e898285554c",
              "name": "folder_id",
              "value": "={{ $json.parents[0] }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "id": "87f8bbb0-92c5-4b25-be63-7a9d91fc46f8",
      "name": "Set File ID",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        860,
        880
      ]
    },
    {
      "parameters": {
        "operation": "text",
        "options": {}
      },
      "id": "7efee822-68ad-4fe2-a616-ba19fd127684",
      "name": "Extract Document Text",
      "type": "n8n-nodes-base.extractFromFile",
      "typeVersion": 1,
      "position": [
        1540,
        880
      ],
      "alwaysOutputData": true
    },
    {
      "parameters": {
        "options": {
          "metadata": {
            "metadataValues": [
              {
                "name": "file_id",
                "value": "={{ $('Set File ID').item.json.file_id }}"
              },
              {
                "name": "folder_id",
                "value": "={{ $('Set File ID').item.json.folder_id }}"
              }
            ]
          }
        }
      },
      "id": "da4c8b29-4944-43c4-9df3-e380366c594a",
      "name": "Default Data Loader",
      "type": "@n8n/n8n-nodes-langchain.documentDefaultDataLoader",
      "typeVersion": 1,
      "position": [
        1860,
        1100
      ]
    },
    {
      "parameters": {
        "chunkSize": 100,
        "options": {}
      },
      "id": "d11c39b9-3fa7-4d5d-838f-da0d258c67c5",
      "name": "Recursive Character Text Splitter",
      "type": "@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter",
      "typeVersion": 1,
      "position": [
        1860,
        1320
      ]
    },
    {
      "parameters": {
        "model": "nomic-embed-text:latest"
      },
      "id": "8a04559c-dfe8-479f-8998-a2e9bc994a0a",
      "name": "Embeddings Ollama1",
      "type": "@n8n/n8n-nodes-langchain.embeddingsOllama",
      "typeVersion": 1,
      "position": [
        1700,
        1100
      ],
      "credentials": {
        "ollamaApi": {
          "id": "eOwAotC7AUgJlvHM",
          "name": "Ollama account"
        }
      }
    },
    {
      "parameters": {
        "content": "## Local RAG AI Agent with Chat Interface",
        "height": 527.3027193303974,
        "width": 969.0343804425795
      },
      "id": "a18773ae-1eb3-46b8-91cf-4184c66cf14f",
      "name": "Sticky Note2",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        560,
        220
      ]
    },
    {
      "parameters": {
        "content": "## Agent Tools for Local RAG",
        "height": 528.85546469693,
        "width": 583.4552380860637,
        "color": 4
      },
      "id": "fa010a11-3dda-4bd5-b261-463a3a6b88d9",
      "name": "Sticky Note",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        1540,
        220
      ]
    },
    {
      "parameters": {
        "content": "## Workflow to Create Local Knowledgebase from Google Drive Folder",
        "height": 705.2695614889159,
        "width": 1568.9362829025763,
        "color": 5
      },
      "id": "f29e6cc7-015e-47cb-a4fd-fecd6ffb0d24",
      "name": "Sticky Note1",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        560,
        760
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "5da52326-dfbd-4350-919c-843461f58913",
      "name": "When chat message received",
      "type": "@n8n/n8n-nodes-langchain.chatTrigger",
      "typeVersion": 1.1,
      "position": [
        620,
        340
      ],
      "webhookId": "4b3b1838-d6b3-447e-9d79-d0931eddb9f8"
    },
    {
      "parameters": {
        "qdrantCollection": {
          "__rl": true,
          "value": "documents",
          "mode": "list",
          "cachedResultName": "documents"
        },
        "options": {}
      },
      "id": "355370e0-2174-4e5b-830b-dd0f123b2e40",
      "name": "Qdrant Vector Store",
      "type": "@n8n/n8n-nodes-langchain.vectorStoreQdrant",
      "typeVersion": 1,
      "position": [
        1560,
        480
      ],
      "credentials": {
        "qdrantApi": {
          "id": "VOnegFP8eijBkbNO",
          "name": "QdrantApi account"
        }
      }
    },
    {
      "parameters": {
        "code": {
          "execute": {
            "code": "const { QdrantVectorStore } = require(\"@langchain/qdrant\");\nconst { OllamaEmbeddings } = require(\"@langchain/community/embeddings/ollama\");\n\nconst embeddings = new OllamaEmbeddings({\n  model: \"nomic-embed-text\",\n  baseUrl: \"http://ollama:11434\"\n});\n\nconst vectorStore = await QdrantVectorStore.fromExistingCollection(\n  embeddings,\n  {\n    url: \"http://qdrant:6333\",\n    collectionName: \"documents\",\n  }\n);\n\nconst fileIdToDelete = this.getInputData()[0].json.file_id;\n\nconst filter = {\n        must: [\n            {\n                key: \"metadata.file_id\",\n                match: {\n                    value: fileIdToDelete,\n                },\n            },\n        ],\n    }\n\n// const results = await vectorStore.similaritySearch(\"this\", 10, filter);\n// const idsToDelete = results.map((doc) => doc.id);\n\n// NOT IMPLEMENTED!\n// await vectorStore.delete({ ids: idsToDelete });\n\nvectorStore.client.delete(\"documents\", {\n  filter\n});\n\nreturn [ {json: { file_id: fileIdToDelete } } ];\n"
          }
        },
        "inputs": {
          "input": [
            {
              "type": "main",
              "required": true
            }
          ]
        },
        "outputs": {
          "output": [
            {
              "type": "main"
            }
          ]
        }
      },
      "id": "b93bd001-0c4d-42fe-939a-eb441f354917",
      "name": "Clear Old Vectors",
      "type": "@n8n/n8n-nodes-langchain.code",
      "typeVersion": 1,
      "position": [
        1080,
        880
      ],
      "alwaysOutputData": false
    },
    {
      "parameters": {
        "mode": "insert",
        "qdrantCollection": {
          "__rl": true,
          "value": "documents",
          "mode": "list",
          "cachedResultName": "documents"
        },
        "options": {}
      },
      "id": "97ec4618-c0ea-445b-9406-5d41784d7836",
      "name": "Qdrant Vector Store Insert",
      "type": "@n8n/n8n-nodes-langchain.vectorStoreQdrant",
      "typeVersion": 1,
      "position": [
        1760,
        880
      ],
      "credentials": {
        "qdrantApi": {
          "id": "VOnegFP8eijBkbNO",
          "name": "QdrantApi account"
        }
      }
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "e537544a-37d5-4b00-b5ff-bc71f041f4bb",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        1340,
        340
      ]
    },
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "invoke_n8n_agent",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "2b8cd01f-30a8-4aab-b0dd-56d2b658f059",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [
        620,
        520
      ],
      "webhookId": "4a839da9-b8a2-45f8-bcaf-c484f9a5912d"
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "c9dfe906-178b-4375-8bda-f9290f35f222",
      "name": "AI Agent",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.6,
      "position": [
        1000,
        340
      ]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "75ebfdef-c8e2-4c3e-b716-1479d0cc2a73",
              "name": "chatInput",
              "value": "={{ $json?.chatInput || $json.body.chatInput }}",
              "type": "string"
            },
            {
              "id": "59b7a20f-0626-4861-93e2-015d430c266e",
              "name": "sessionId",
              "value": "={{ $json?.sessionId || $json.body.sessionId}}",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "id": "8f974a15-aa2f-4525-8278-ad58ad296076",
      "name": "Edit Fields",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        820,
        340
      ]
    },
    {
      "parameters": {
        "path": "/mnt/data/docs",
        "watchInterval": 60
      },
      "id": "local_file_trigger",
      "name": "Local File Trigger",
      "type": "n8n-nodes-base.localFileTrigger",
      "typeVersion": 1,
      "position": [
        600,
        880
      ]
    },
    {
      "parameters": {
        "filePath": "={{ $json[\"path\"] }}"
      },
      "id": "read_binary_file",
      "name": "Read Binary File",
      "type": "n8n-nodes-base.readBinaryFile",
      "typeVersion": 1,
      "position": [
        800,
        880
      ]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "name": "file_id",
              "value": "={{ $json.path }}",
              "type": "string"
            }
          ]
        }
      },
      "name": "Set File ID",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [
        1000,
        820
      ],
      "id": "set_file_id"
    },
    {
      "parameters": {
        "chunkSize": 500,
        "chunkOverlap": 50,
        "textProperty": "text"
      },
      "name": "Text Splitter",
      "type": "@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacter",
      "typeVersion": 1,
      "position": [
        1200,
        880
      ],
      "id": "text_splitter"
    }
  ],
  "pinData": {},
  "connections": {
    "Postgres Chat Memory": {
      "ai_memory": [
        [
          {
            "node": "AI Agent",
            "type": "ai_memory",
            "index": 0
          }
        ]
      ]
    },
    "Ollama Chat Model": {
      "ai_languageModel": [
        [
          {
            "node": "AI Agent",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "Ollama Model": {
      "ai_languageModel": [
        [
          {
            "node": "Vector Store Tool",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "Embeddings Ollama": {
      "ai_embedding": [
        [
          {
            "node": "Qdrant Vector Store",
            "type": "ai_embedding",
            "index": 0
          }
        ]
      ]
    },
    "Set File ID": {
      "main": [
        [
          {
            "node": "Clear Old Vectors",
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
            "node": "Text Splitter",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Default Data Loader": {
      "ai_document": [
        [
          {
            "node": "Qdrant Vector Store Insert",
            "type": "ai_document",
            "index": 0
          }
        ]
      ]
    },
    "Recursive Character Text Splitter": {
      "ai_textSplitter": [
        [
          {
            "node": "Default Data Loader",
            "type": "ai_textSplitter",
            "index": 0
          }
        ]
      ]
    },
    "Embeddings Ollama1": {
      "ai_embedding": [
        [
          {
            "node": "Qdrant Vector Store Insert",
            "type": "ai_embedding",
            "index": 0
          }
        ]
      ]
    },
    "When chat message received": {
      "main": [
        [
          {
            "node": "Edit Fields",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Qdrant Vector Store": {
      "ai_vectorStore": [
        [
          {
            "node": "Vector Store Tool",
            "type": "ai_vectorStore",
            "index": 0
          }
        ]
      ]
    },
    "Clear Old Vectors": {
      "main": [
        [
          {
            "node": "Download File",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Webhook": {
      "main": [
        [
          {
            "node": "Edit Fields",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "AI Agent": {
      "main": [
        [
          {
            "node": "Respond to Webhook",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Edit Fields": {
      "main": [
        [
          {
            "node": "AI Agent",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Vector Store Tool": {
      "ai_tool": [
        [
          {
            "node": "AI Agent",
            "type": "ai_tool",
            "index": 0
          }
        ]
      ]
    },
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
        ],
        [
          {
            "node": "Set File ID",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Text Splitter": {
      "ai_textSplitter": [
        [
          {
            "node": "Default Data Loader",
            "type": "ai_textSplitter",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "19f9691c-4682-4704-81f2-33fdec9d0be2",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "f722e3e1e81e942a38faa434ad0aee8699371bbff9f883b9d5c59a7c726605af"
  },
  "id": "vTN9y2dLXqTiDfPT",
  "tags": []
}