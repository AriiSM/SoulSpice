# 🖥️ SoulSpice Server Documentation

## Overview

SoulSpice is a specialized chatbot that combines expertise in psychology and cooking, providing personalized culinary advice based on emotional and psychological preferences. The project architecture uses FastAPI for the backend, with LLM integration through LM Studio and semantic search capabilities with FAISS.


## Core Components

### 1. Semantic Search Assistant

The main engine of SoulSpice is the `SemanticSearchAssistant` which:
- Retrieves relevant content from two knowledge bases (recipes and conversations)
- Generates appropriate responses using a language model
- Ensures responses are non-toxic and empathetic

### 2. TextChunkLoader

Loads pre-processed text chunks from files containing:
- Recipe data
- Conversation examples and patterns

### 3. SemanticRetriever

Uses sentence transformers and FAISS indexing to:
- Convert user questions into vector embeddings
- Find semantically similar content in knowledge bases
- Retrieve the most relevant information for generating responses

### 4. ToxicityFilter

Implements safety measures to:
- Detect potentially problematic content
- Filter out toxic responses
- Log potential issues for review

### 5. ResponseGenerator

Leverages an LLM to:
- Generate human-like, contextually appropriate responses
- Maintain a consistent tone and personality
- Adapt language based on user input

### 6. ChatService & LLMService

These services handle:
- API integration with the frontend
- Message processing and response generation
- Error handling and service availability checks

## Project Structure

```
Server/
├── _pycache__/                    # Python cache files
├── .deepeval/                     # DeepEval configuration files
├── .pytest_cache/                 # PyTest cache files
├── app/                           # Main application package
│   ├── _pycache__/
│   ├── api/                       # API endpoints
│   │   ├── _pycache__/
│   │   └── routes.py              # FastAPI route definitions
│   ├── core/                      # Core components
│   │   ├── _pycache__/
│   │   └── config.py              # Application settings & config
│   ├── data/                      # Data storage
│   │   └── faiss/                 # Vector indexes
│   │       ├── conversations.faiss # Conversation embeddings
│   │       ├── parsed_conversations.txt # Conversation data
│   │       ├── parsed_recipes.txt  # Recipe data
│   │       └── recipes.faiss       # Recipe embeddings
│   ├── models/                    # Data models
│   │   ├── _pycache__/
│   │   └── message.py             # Message schemas
│   └── services/                  # Business logic
│       ├── _pycache__/ 
│       ├── __init__.py
│       ├── chat_bot_tools.py      # Core chatbot components
│       ├── chat_service.py        # Chat processing logic
│       └── llm_service.py         # LLM integration
├── tests/                         # Test suite
│   ├── _pycache__/
│   ├── .deepeval/
│   ├── .pytest_cache/
│   ├── evaluation_report.json     # LLM evaluation metrics results
│   └── test_deepeval_runner.py    # DeepEval test runner
├── venv/                          # Virtual environment
├── main.py                        # Server entry point
└── README.md                      # Project documentation
```