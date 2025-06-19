# Travel Itinerary Generation System - Simplified Workflow

## High-Level System Architecture

```mermaid
graph TB
    subgraph "User Interface"
        UI[Web Chat Interface]
    end
    
    subgraph "Core System"
        AGENT[Conversational Agent]
        RAG[RAG System]
        DB[(Travel Database)]
    end
    
    subgraph "Output"
        ITINERARY[Generated Itinerary]
    end
    
    UI --> AGENT
    AGENT --> RAG
    RAG --> DB
    AGENT --> ITINERARY
    
    style UI fill:#e1f5fe
    style AGENT fill:#fff3e0
    style RAG fill:#f3e5f5
    style DB fill:#c8e6c9
    style ITINERARY fill:#ffecb3
```

## Simple Workflow Process

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant R as RAG
    participant D as Database
    
    U->>A: "I want to plan a trip to Paris"
    A->>U: "What's your budget range?"
    
    U->>A: "Around $3000"
    A->>U: "What type of travel do you prefer?"
    
    U->>A: "Cultural and food experiences"
    A->>R: Query relevant travel plans
    
    R->>D: Search database
    D->>R: Return matching plans
    R->>A: Send recommendations
    
    A->>U: Present personalized itinerary
```

## Key Components

### 1. **Conversational Agent**
- Collects user preferences (destination, budget, interests)
- Manages conversation flow
- Generates final itinerary

### 2. **RAG System**
- Searches company's travel database
- Finds relevant travel plans and offers
- Provides context for itinerary generation

### 3. **Travel Database**
- Stores company's travel packages
- Contains pricing, activities, accommodations
- Includes special offers and deals

### 4. **Output**
- Personalized travel itinerary
- Day-by-day schedule
- Budget breakdown
- Activity recommendations 