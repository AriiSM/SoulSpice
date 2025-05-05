PROTOTYPE BACKEND STRUCTURE


SoulSpice_server/
│
├── main.py                      # Main application entry point
├── .env                         # Environment variables (create this)
│
├── app/                         # Application package
│   ├── __init__.py             
│   │
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py            # API routes
│   │
│   ├── core/                    # Core application code
│   │   ├── __init__.py
│   │   └── config.py            # Configuration settings
│   │
│   ├── data/                    # Data and knowledge bases
│   │   ├── __init__.py
│   │   └── knowledge_base.py    # Food-mood knowledge
│   │
│   ├── models/                  # Pydantic models
│   │   ├── __init__.py
│   │   └── message.py           # Message models
│   │
│   └── services/                # Business logic services
│       ├── __init__.py
│       ├── chat_service.py      # Chat processing service
│       ├── emotion_service.py   # Emotion detection service
│       ├── llm_service.py       # LLM integration service
│       └── vector_service.py    # Vector DB/FAISS service
│
└── data/                        # Data storage directory
    ├── knowledge/               # Knowledge base files
    └── vector_db/               # Vector database files