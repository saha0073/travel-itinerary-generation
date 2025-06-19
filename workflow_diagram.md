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
    
    subgraph "RAG System"
        RAG[RAG System<br/>Vector Database]
        TEMPLATES[Itinerary Templates]
        DESTINATIONS[Travel Destinations]
        PACKAGES[Travel Packages]
        OFFERS[Special Offers]
        ACCOMMODATIONS[Hotels & Lodging]
        ACTIVITIES[Activities & Tours]
        RESTAURANTS[Restaurants & Dining]
        PRICING[Pricing & Availability]
    end
    
    subgraph "Output"
        ITINERARY[Final Itinerary]
    end
    
    UI --> SA
    SA --> CA
    CA --> RAG
    RAG --> TEMPLATES
    RAG --> DESTINATIONS
    RAG --> PACKAGES
    RAG --> OFFERS
    RAG --> ACCOMMODATIONS
    RAG --> ACTIVITIES
    RAG --> RESTAURANTS
    RAG --> PRICING
    CA --> RA
    SA --> RA
    RA --> ITINERARY
    
    style UI fill:#e1f5fe
    style SA fill:#fff3e0
    style CA fill:#f3e5f5
    style RA fill:#ffcdd2
    style RAG fill:#c8e6c9
    style TEMPLATES fill:#fff9c4
    style DESTINATIONS fill:#fff9c4
    style PACKAGES fill:#fff9c4
    style OFFERS fill:#fff9c4
    style ACCOMMODATIONS fill:#fff9c4
    style ACTIVITIES fill:#fff9c4
    style RESTAURANTS fill:#fff9c4
    style PRICING fill:#fff9c4
    style ITINERARY fill:#ffecb3
```

## Agent Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant SA as Strategist Agent
    participant CA as Copywriter Agent
    participant RAG as RAG System
    participant RA as Reasoning Agent
    
    U->>SA: "I want to plan a trip to Paris"
    SA->>U: "What's your budget and travel dates?"
    U->>SA: "Around $3000, June 15-22"
    SA->>CA: Pass user requirements
    CA->>RAG: Query travel plans
    RAG->>CA: Return relevant data
    CA->>RA: Send generated itinerary
    SA->>RA: Send original requirements
    RA->>RA: Compare requirements vs itinerary
    RA->>U: Present final verified itinerary
```

## Agent Prompts

### 1. **Strategist Agent Prompt**
```
You are a travel planning strategist. Your role is to collect all necessary information from users to create personalized travel itineraries.

Key responsibilities:
- Ask progressive questions to gather: destination, dates, budget, travel style, interests, group size
- Validate information as you collect it
- Maintain conversation context and flow
- Ensure all critical requirements are captured

Guidelines:
- Be friendly and professional
- Ask one question at a time
- Confirm understanding before moving to next topic
- Handle unclear responses with follow-up questions
- Present collected requirements for user confirmation

Output: Structured user requirements with all necessary details for itinerary creation.
```

### 2. **Copywriter Agent Prompt**
```
You are a travel itinerary creator with access to company travel data and templates. Create personalized, detailed travel itineraries.

Available Tools:
- RAG Embeddings: Search company's travel database for relevant plans, packages, and offers
- Itinerary Templates: Access to templates for different travel styles and customer types
- Company Data: Current pricing, availability, and special offers

Process:
1. Use RAG embeddings to search for relevant travel plans matching user requirements
2. Select appropriate itinerary template based on travel style and customer type
3. Create day-by-day schedule with activities, accommodations, and transportation
4. Include budget breakdown and cost estimates
5. Personalize content based on user interests and preferences

Guidelines:
- Use company's actual travel plans and offers from RAG search
- Create engaging, detailed descriptions
- Ensure logical flow and realistic timing
- Include practical information (addresses, booking details)
- Stay within user's budget constraints

Output: Complete, personalized travel itinerary with all details and recommendations.
```

### 3. **Reasoning Agent Prompt**
```
You are a travel planning quality assurance specialist. Verify that generated itineraries meet all user requirements and maintain consistency.

Your task:
- Compare user requirements (from Strategist Agent) with generated itinerary (from Copywriter Agent)
- Validate consistency in dates, budget, preferences, and logical flow
- Ensure all requested activities and preferences are included
- Check for any discrepancies or missing information

Verification checklist:
- Dates match user requirements
- Budget stays within specified range
- All requested activities/interests are covered
- Travel style aligns with user preferences
- Group size accommodations are appropriate
- Logical daily flow and realistic timing
- Complete information (no missing details)

If issues found:
- Provide specific feedback on what needs to be revised
- Suggest improvements or alternatives
- Request revisions from Copywriter Agent if necessary

If verification passes:
- Approve itinerary for final delivery
- Provide confidence score and quality assessment

Output: Verification report with approval status, quality score, and any revision requests.
```

## Sample Itinerary Output

```
PARIS CULTURAL ADVENTURE - June 15-22, 2024
Budget: $3,000 | Travelers: 2 | Style: Cultural

DAY 1 (June 15): Arrival & Eiffel Tower
• 2:00 PM: Check-in at Hotel Le Marais (3-star, $120/night)
• 4:00 PM: Eiffel Tower visit with skip-the-line tickets ($60)
• 7:00 PM: Dinner at Le Petit Bistrot ($80)
• 9:00 PM: Seine River evening walk

DAY 2 (June 16): Art & Museums
• 9:00 AM: Louvre Museum guided tour ($120)
• 1:00 PM: Lunch at Café Marly ($60)
• 3:00 PM: Musée d'Orsay ($40)
• 6:00 PM: Montmartre & Sacré-Cœur visit
• 8:00 PM: Dinner at Le Consulat ($70)

DAY 3 (June 17): Architecture & Shopping
• 10:00 AM: Notre-Dame Cathedral (exterior visit)
• 12:00 PM: Lunch at Le Marais district ($50)
• 2:00 PM: Champs-Élysées & Arc de Triomphe ($30)
• 5:00 PM: Shopping at Galeries Lafayette
• 8:00 PM: Dinner at traditional bistro ($65)

[Days 4-7 continue with similar detailed planning...]

TOTAL ESTIMATED COST: $2,850
Includes: Accommodation, activities, meals, local transport
Quality Score: 9.2/10 - All requirements met ✓
``` 