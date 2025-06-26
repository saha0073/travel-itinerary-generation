# Travel Itinerary Generation System

## Overview
This system creates personalized travel itineraries using a conversational AI agent that leverages RAG (Retrieval-Augmented Generation) to access the company's travel plans and offers database.

## Architecture

### Core Components:
1. **Conversational Agent**: Handles user interaction and collects travel preferences
2. **RAG System**: Retrieves relevant travel plans and offers from company database
3. **Itinerary Generator**: Creates personalized itineraries based on user input and retrieved data
4. **Database**: Stores company's travel plans, offers, and user sessions

### Workflow:
1. User initiates conversation
2. Agent collects travel preferences (destination, budget, dates, interests, etc.)
3. RAG system queries company database for relevant offers
4. Agent generates personalized itinerary
5. User can refine and finalize the itinerary

## Features
- Natural language conversation interface
- Budget-aware recommendations
- Personalized travel suggestions
- Integration with company's travel database
- Session management for ongoing conversations

## Tech Stack
- Python 3.9+
- FastAPI for API endpoints
- SQLAlchemy for database operations
- LangChain for RAG implementation
- ChromaDB for vector storage
- Streamlit for web interface

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Set up database: `python setup_database.py`
3. Run the application: `streamlit run app.py`

## Project Structure
```
travel-iteneary-generation/
├── app.py                 # Main Streamlit application
├── agent/
│   ├── __init__.py
│   ├── conversation_agent.py  # Main conversational agent
│   └── itinerary_generator.py # Itinerary generation logic
├── rag/
│   ├── __init__.py
│   ├── vector_store.py    # Vector database operations
│   └── retriever.py       # RAG retrieval logic
├── database/
│   ├── __init__.py
│   ├── models.py          # Database models
│   └── operations.py      # Database operations
├── data/
│   └── sample_travel_data.py  # Sample travel plans data
├── requirements.txt       # Python dependencies
└── workflow_diagram.md    # System workflow diagram
``` 