# Multi-Agent Travel Itinerary System

## Three-Agent Architecture

```mermaid
graph TB
    subgraph "User Interface"
        UI[Web Chat Interface]
    end
    
    subgraph "Agent System"
        SA[Strategist Agent<br/>LangChain]
        CA[Copywriter Agent<br/>LangChain + RAG]
        RA[Reasoning Agent<br/>DeepSeek API]
    end
    
    subgraph "Data Sources"
        RAG[RAG System]
        DB[(Travel Database)]
        TEMPLATES[Itinerary Templates]
    end
    
    subgraph "Output"
        ITINERARY[Final Itinerary]
    end
    
    UI --> SA
    SA --> RA
    RA --> CA
    CA --> RAG
    RAG --> DB
    CA --> TEMPLATES
    CA --> RA
    RA --> ITINERARY
    
    style UI fill:#e1f5fe
    style SA fill:#fff3e0
    style CA fill:#f3e5f5
    style RA fill:#ffcdd2
    style RAG fill:#c8e6c9
    style DB fill:#c8e6c9
    style TEMPLATES fill:#fff9c4
    style ITINERARY fill:#ffecb3
```

## Agent Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant SA as Strategist Agent
    participant RA as Reasoning Agent
    participant CA as Copywriter Agent
    participant RAG as RAG System
    
    U->>SA: "I want to plan a trip to Paris"
    SA->>U: "What's your budget and travel dates?"
    U->>SA: "Around $3000, June 15-22"
    SA->>RA: Validate requirements
    RA->>SA: Requirements approved
    SA->>CA: Pass requirements
    CA->>RAG: Query travel plans
    RAG->>CA: Return relevant data
    CA->>RA: Send itinerary for verification
    RA->>CA: Verification complete
    CA->>U: Present final itinerary
```

## Three Agents

### 1. **Strategist Agent (LangChain)**
- Collects user requirements (destination, dates, budget, interests)
- Manages conversation flow and validation
- Passes complete requirements to Reasoning Agent

### 2. **Copywriter Agent (LangChain + RAG)**
- Queries company database via RAG system
- Uses itinerary templates and company data
- Creates personalized day-by-day itineraries
- Sends to Reasoning Agent for verification

### 3. **Reasoning Agent (DeepSeek API)**
- Validates user requirements for consistency
- Verifies itinerary matches all requirements
- Checks budget, dates, and logical flow
- Provides final approval or revision requests

## Key Components

### 1. **RAG System**
- Searches company's travel database
- Finds relevant travel plans and offers
- Provides context for itinerary generation

### 2. **Travel Database**
- Stores company's travel packages
- Contains pricing, activities, accommodations
- Includes special offers and deals

### 3. **Output**
- Personalized travel itinerary
- Day-by-day schedule
- Budget breakdown
- Activity recommendations 