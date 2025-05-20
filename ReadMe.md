# 🌿 SoulSpice: Your Culinary Psychologist

## 🍽️ Overview

SoulSpice is an innovative chatbot that bridges the gap between culinary arts and emotional wellness. Unlike traditional recipe assistants, SoulSpice understands that food is deeply connected to our emotional state and provides personalized culinary advice that nourishes both body and soul.

### What Makes SoulSpice Special:

- **Emotional Intelligence**: Recommends recipes based on your current mood and emotional state
- **Culinary Expertise**: Provides thoughtful food advice grounded in nutritional science
- **Mindful Eating**: Encourages a healthy relationship with food through mindful eating practices
- **Personalized Approach**: Learns your preferences over time to offer increasingly tailored recommendations

## 🌟 Features

- Mood-based recipe recommendations
- Nutritional guidance customized to emotional states
- Mindful eating techniques
- Real-time conversation with empathetic responses
- Beautiful, intuitive user interface
- Smart semantic search for relevant culinary and psychological knowledge

## 👥 Team Members

- **Brenner Vanessa** 
- **Pasăre Vlăduț** 
- **Sima Alin** 
- **Stan Ariana - Maria**
 


## 🚀 Quick Start

### 🛠️ Prerequisites
- Python 3.10+
- Node.js + npm
- LM Studio (https://lmstudio.ai/)
- Model: mistral-7b-instruct-v0.3 (Download and launch in LM Studio)

### Installation & Setup

Follow these steps to get SoulSpice up and running on your local machine:
#### 1. Clone the Repository
   ```bash
   git clone https://github.com/AriiSM/SoulSpice.git
   cd SoulSpice
   ```


#### 2.  Server Setup
   ``` bash
   # Navigate to server directory
   cd Server

   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install Python dependencies
   pip install -r requirements.txt

   # Start the backend server
   python main.py
   ```

#### 3. Client Setup
   ```bash
   # Navigate to client directory from the project root
   cd client

   # Install frontend dependencies
   npm install

   # Start the React application
   npm start
   ```


## 🔮 Technology Stack

### Backend Architecture
- Python + FastAPI: Powers the server API
- Sentence Transformers: For semantic understanding of user queries
- FAISS: Efficient similarity search for knowledge retrieval
- ToxicityFilter: Ensures safe and appropriate responses
- LM Studio Integration: Leverages Mistral LLM for natural language generation

### Frontend Architecture
- React: Frontend library for building the UI
- CSS Variables: Theme-based styling with custom properties
- React Hooks: State management and side effects
- Axios: API communication with the SoulSpice server


## 🔍 Project Structure
```text
SoulSpice/
├── Client/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js              # API communication functions
│   │   ├── ChatBot/
│   │   │   ├── SoulSpice.js    # Main chat component
│   │   │   └── SoulSpice.css   # Component styles    
│   │   │       
│   │   ├── App.js                  # Root component
│   │   └── index.js                # Application entry point
│   └── package.json
│
└── Server/
    ├── app/                           # Main application package
    │   ├── api/                       # API endpoints
    │   │   └── routes.py              # FastAPI route definitions
    │   ├── core/                      # Core components
    │   │   └── config.py              # Application settings & config
    │   ├── data/                      # Data storage
    │   │   └── faiss/                 # Vector indexes
    │   │       ├── conversations.faiss # Conversation embeddings
    │   │       ├── parsed_conversations.txt # Conversation data
    │   │       ├── parsed_recipes.txt  # Recipe data
    │   │       └── recipes.faiss       # Recipe embeddings
    │   ├── models/                    # Data models
    │   │   └── message.py             # Message schemas
    │   └── services/                  # Business logic
    │       ├── __init__.py
    │       ├── chat_bot_tools.py      # Core chatbot components
    │       ├── chat_service.py        # Chat processing logic
    │       └── llm_service.py         # LLM integration
    ├── tests/                         # Test suite
    │   ├── evaluation_report.json     # LLM evaluation metrics results
    │   └── test_deepeval_runner.py    # DeepEval test runner
    └── main.py                        # Server entry point
```
---

## Demo Video

Watch a full demo of application in action:

[![Watch the demo]([https://www.youtube.com/watch?v=u00s7uuf_v0](https://www.youtube.com/watch?v=u00s7uuf_v0))
