# Multi-Agent Travel Itinerary Generation System

## Overview
This system creates personalized travel itineraries using a three-agent architecture that combines conversational AI, RAG (Retrieval-Augmented Generation), and quality assurance to deliver comprehensive travel planning solutions.

## Architecture

### Three-Agent System:
1. **Strategist Agent** (LangChain): Collects and analyzes user travel requirements
2. **Copywriter Agent** (LangChain + RAG): Creates detailed itineraries using company travel data
3. **Reasoning Agent** (DeepSeek API): Verifies consistency and quality of generated itineraries

### Workflow:
1. User provides complete travel requirements in natural language
2. **Strategist Agent** analyzes requirements and gathers destination context via web search
3. **Copywriter Agent** creates detailed itinerary using RAG system and Amadeus API tools
4. **Reasoning Agent** verifies the itinerary against original requirements
5. User receives a complete, verified travel itinerary

For detailed workflow diagrams and agent interactions, see [workflow_diagram.md](workflow_diagram.md).

## Features
- **Multi-Agent Architecture**: Three specialized agents working in sequence
- **Real-time Processing**: See each agent's output as it completes
- **RAG Integration**: Access to company travel data and templates
- **API Integration**: Amadeus API for hotels, flights, and activities
- **Quality Assurance**: Automated verification of itinerary consistency
- **Web Search**: Real-time destination information gathering
- **Streamlit Interface**: Interactive chat-based user experience

## Tech Stack
- **Python 3.9+**
- **LangChain**: Agent framework and RAG implementation
- **Streamlit**: Web interface and real-time updates
- **Groq API**: DeepSeek model for verification agent
- **Amadeus API**: Travel data (hotels, flights, activities)
- **Tavily API**: Web search for destination context
- **OpenAI API**: GPT-4 for strategist and copywriter agents

## System Components

### Agent System
- **Strategist Agent**: Analyzes user requirements and gathers destination context
- **Copywriter Agent**: Creates detailed itineraries using RAG and travel APIs
- **Reasoning Agent**: Verifies consistency and quality assurance

### RAG System
- Vector database for company travel data
- Itinerary templates for different travel styles
- Travel packages and pricing information
- Activities and tour recommendations

### External APIs
- **Amadeus API**: Real-time hotel, flight, and activity data
- **Tavily API**: Web search for destination information
- **Groq API**: DeepSeek model for verification

For detailed agent prompts and workflow diagrams, refer to [workflow_diagram.md](workflow_diagram.md).

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file with the following API keys:
```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
AMADEUS_CLIENT_ID=your_amadeus_client_id
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret
TAVILY_API_KEY=your_tavily_api_key
```

### 3. Run the Application
```bash
streamlit run streamlit_app.py
```

## Usage Example

1. **Start the application**: `streamlit run streamlit_app.py`
2. **Enter travel requirements**: "I want to travel to Manali from Delhi, September 1-10, 2025. Please create a travel itinerary."
3. **Watch the process**:
   - Strategist Agent analyzes your requirements
   - Copywriter Agent creates detailed itinerary
   - Reasoning Agent verifies the final plan
4. **Review results**: Complete itinerary with verification report

## Project Structure
```
thrillopilla/
├── streamlit_app.py          # Main Streamlit application
├── agent_lc/
│   ├── agent.py              # Agent implementation
│   ├── prompts.py            # Agent prompts and configurations
│   ├── tools.py              # Amadeus API tools and utilities
│   └── chat_history.py       # Chat history management
├── requirements.txt          # Python dependencies
├── packages.txt              # System dependencies for Streamlit Cloud
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── workflow_diagram.md       # Detailed system architecture and workflows
└── README.md                # This file
```

## Agent Details

### Strategist Agent
- **Purpose**: Analyze complete user requirements and gather destination context
- **Tools**: Web search for destination information
- **Output**: Comprehensive travel requirements analysis

### Copywriter Agent
- **Purpose**: Create detailed day-by-day itineraries
- **Tools**: Amadeus API (hotels, flights, activities), RAG system
- **Output**: Complete travel itinerary with pricing and recommendations

### Reasoning Agent
- **Purpose**: Verify itinerary consistency and quality
- **Model**: DeepSeek via Groq API
- **Output**: Verification report with quality score and recommendations

For detailed agent prompts and interaction flows, see [workflow_diagram.md](workflow_diagram.md).

## Deployment

### Streamlit Cloud
The application is configured for deployment on Streamlit Cloud with:
- Exact version pinning in `requirements.txt`
- System dependencies in `packages.txt`
- Streamlit configuration in `.streamlit/config.toml`

### Local Development
For local development, ensure all environment variables are set and run:
```bash
streamlit run streamlit_app.py
```

## Workflow Diagrams

For comprehensive workflow diagrams, agent interaction sequences, and detailed system architecture, please refer to [workflow_diagram.md](workflow_diagram.md). This document contains:

- Three-agent architecture diagram
- Agent workflow sequence diagram
- Detailed agent prompts
- Sample itinerary output format
- System interaction flows

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the Streamlit interface
5. Submit a pull request

## License

This project is for interview preparation and demonstration purposes. 