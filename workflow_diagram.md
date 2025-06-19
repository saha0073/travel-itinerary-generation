# Travel Itinerary Generation Workflow

## System Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface"
        UI[Streamlit Web App]
    end
    
    subgraph "Conversational Agent"
        CA[Conversation Agent]
        IG[Itinerary Generator]
        SM[Session Manager]
    end
    
    subgraph "RAG System"
        VS[Vector Store<br/>ChromaDB]
        RET[Retriever]
        EMB[Embedding Model]
    end
    
    subgraph "Database"
        DB[(SQL Database)]
        TP[Travel Plans]
        OF[Offers]
        US[User Sessions]
    end
    
    subgraph "External APIs"
        WEATHER[Weather API]
        MAPS[Maps API]
        CURRENCY[Currency API]
    end
    
    UI --> CA
    CA --> SM
    CA --> IG
    
    IG --> RET
    RET --> VS
    VS --> EMB
    EMB --> DB
    
    IG --> WEATHER
    IG --> MAPS
    IG --> CURRENCY
    
    SM --> US
    CA --> US
```

## Detailed Workflow Process

```mermaid
sequenceDiagram
    participant U as User
    participant CA as Conversation Agent
    participant RAG as RAG System
    participant DB as Database
    participant IG as Itinerary Generator
    
    U->>CA: Start conversation
    CA->>U: Greet and ask for destination
    
    U->>CA: Provide destination
    CA->>U: Ask for travel dates
    
    U->>CA: Provide dates
    CA->>U: Ask for budget range
    
    U->>CA: Provide budget
    CA->>U: Ask for travel style (luxury/budget/adventure)
    
    U->>CA: Provide preferences
    CA->>U: Ask for interests (culture, food, nature, etc.)
    
    U->>CA: Provide interests
    CA->>RAG: Query relevant travel plans
    
    RAG->>DB: Retrieve matching offers
    DB->>RAG: Return travel plans
    
    RAG->>CA: Return relevant data
    CA->>IG: Generate itinerary
    
    IG->>IG: Process preferences + RAG data
    IG->>CA: Return itinerary
    
    CA->>U: Present itinerary
    U->>CA: Request modifications
    
    CA->>IG: Refine itinerary
    IG->>CA: Return updated itinerary
    CA->>U: Present final itinerary
```

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph "Input Processing"
        A[User Input] --> B[Intent Recognition]
        B --> C[Entity Extraction]
        C --> D[Preference Collection]
    end
    
    subgraph "RAG Processing"
        D --> E[Query Formation]
        E --> F[Vector Search]
        F --> G[Relevant Data Retrieval]
    end
    
    subgraph "Itinerary Generation"
        G --> H[Data Integration]
        H --> I[Constraint Satisfaction]
        I --> J[Itinerary Creation]
    end
    
    subgraph "Output"
        J --> K[Formatted Itinerary]
        K --> L[User Presentation]
    end
    
    style A fill:#e1f5fe
    style L fill:#c8e6c9
    style G fill:#fff3e0
    style J fill:#f3e5f5
```

## Database Schema

```mermaid
erDiagram
    TRAVEL_PLANS {
        int id PK
        string destination
        string title
        text description
        decimal price
        int duration_days
        string travel_style
        json activities
        json accommodations
        json transportation
        boolean is_active
        datetime created_at
    }
    
    OFFERS {
        int id PK
        int travel_plan_id FK
        string offer_type
        decimal discount_percentage
        date valid_from
        date valid_until
        text terms_conditions
        boolean is_active
    }
    
    USER_SESSIONS {
        int id PK
        string session_id
        json preferences
        json conversation_history
        datetime created_at
        datetime last_updated
    }
    
    ITINERARIES {
        int id PK
        int session_id FK
        text itinerary_content
        json metadata
        datetime created_at
        string status
    }
    
    TRAVEL_PLANS ||--o{ OFFERS : "has"
    USER_SESSIONS ||--o{ ITINERARIES : "generates"
```

## Key Components Description

### 1. Conversation Agent
- **Purpose**: Manages natural language interaction with users
- **Functions**: 
  - Intent recognition and entity extraction
  - Progressive preference collection
  - Context maintenance across conversation
  - Itinerary presentation and refinement

### 2. RAG System
- **Purpose**: Retrieves relevant travel information from company database
- **Components**:
  - Vector store (ChromaDB) for semantic search
  - Embedding model for text vectorization
  - Retriever for relevant document fetching
  - Query processing and ranking

### 3. Itinerary Generator
- **Purpose**: Creates personalized travel itineraries
- **Process**:
  - Integrates user preferences with retrieved data
  - Applies business rules and constraints
  - Generates day-by-day itinerary
  - Handles budget optimization

### 4. Database Layer
- **Purpose**: Stores company's travel plans, offers, and user data
- **Tables**:
  - Travel Plans: Company's travel packages
  - Offers: Special deals and promotions
  - User Sessions: Conversation state management
  - Itineraries: Generated travel plans

## Implementation Notes

1. **Vector Embeddings**: Use sentence-transformers for travel plan embeddings
2. **Conversation State**: Maintain session state for multi-turn conversations
3. **Budget Optimization**: Implement constraint satisfaction for budget-aware recommendations
4. **Real-time Updates**: Integrate with external APIs for current pricing and availability
5. **Personalization**: Use collaborative filtering for similar user recommendations 