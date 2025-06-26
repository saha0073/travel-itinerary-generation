from agent_lc.agent import Agent
from agent_lc.prompts import WEB_SEARCH_PROMPT, TRAVEL_PLANNER_PROMPT
from pathlib import Path
import logging
import time
import json
from datetime import datetime
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

def save_final_analysis(test_name: str, run_id: str, verification_results: str):
    """Save the final analysis results to a log file"""
    try:
        # Create logs directory
        log_dir = Path("analysis_logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename with test_id and run_id
        log_file = log_dir / f"final_analysis_{test_name}_{run_id}.json"
        
        # Prepare the analysis data
        analysis_data = {
            "test_name": test_name,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "verification_results": verification_results
        }
        
        # Save the analysis
        with open(log_file, 'w') as f:
            json.dump(analysis_data, f, indent=2)
            
        print(f"\nFinal analysis saved to: {log_file}")
    except Exception as e:
        logger.error(f"Error saving final analysis: {str(e)}")

def main(test_name: str, run_id: str):
    # Initialize the first agent (Strategist Agent - Web Search)
    print("Initializing Strategist Agent...")
    strategist_agent = Agent(prompt_text=WEB_SEARCH_PROMPT, agent_type="web_search")
    strategist_agent_executor = strategist_agent.get_agent_executor()
    
    # Initialize the second agent (Copywriter Agent - Travel Planner)
    print("Initializing Copywriter Agent...")
    copywriter_agent = Agent(prompt_text=TRAVEL_PLANNER_PROMPT, agent_type="travel_planner")
    copywriter_agent_executor = copywriter_agent.get_agent_executor()
    
    # Initialize Groq client for DeepSeek verification
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    
    # Step 1: Strategist Agent collects requirements
    print("\n=== Step 1: Strategist Agent Collecting Requirements ===")
    user_query = "I want to make Manali travel plan, for 2nd September 2025 to 10th September 2025. We are 2 people and interested in adventure activities, mountain views, and local culture. Budget is around $2000."
    
    # Add retry logic for strategist agent
                max_retries = 3
                for attempt in range(max_retries):
                    try:
            strategist_response = strategist_agent_executor.invoke({
                "input": f"Collect travel requirements from this user request: {user_query}"
            })
            break
                    except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to get strategist response after {max_retries} attempts: {str(e)}")
                return
            print(f"Attempt {attempt + 1} failed, retrying... Error: {str(e)}")
            time.sleep(2)  # Wait before retry
    
    print("Strategist Agent Response:")
    print(strategist_response["output"])
    
    # Step 2: Copywriter Agent creates itinerary
    print("\n=== Step 2: Copywriter Agent Creating Itinerary ===")
    copywriter_prompt = f"""
    Based on the user requirements collected by the Strategist Agent, create a detailed travel itinerary.
    
    User Requirements: {user_query}
    Strategist Analysis: {strategist_response["output"]}
    
    Please create a comprehensive day-by-day itinerary including:
    - Hotel recommendations with pricing
    - Flight options with pricing
    - Daily activities and attractions
    - Restaurant recommendations
    - Budget breakdown
    """
    
    # Add retry logic for copywriter agent
    for attempt in range(max_retries):
        try:
            copywriter_response = copywriter_agent_executor.invoke({
                "input": copywriter_prompt
            })
            break
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to get copywriter response after {max_retries} attempts: {str(e)}")
                return
            print(f"Attempt {attempt + 1} failed, retrying... Error: {str(e)}")
            time.sleep(2)  # Wait before retry
    
    print("Copywriter Agent Response:")
    print(copywriter_response["output"])
    
    # Step 3: DeepSeek Agent verifies consistency
    print("\n=== Step 3: DeepSeek Agent Verifying Consistency ===")
    
    verification_prompt = f"""
    You are a travel planning quality assurance specialist. Compare the user requirements with the generated itinerary to ensure consistency and completeness.
    
    USER REQUIREMENTS:
    {user_query}
    
    STRATEGIST AGENT ANALYSIS:
    {strategist_response["output"]}
    
    COPYWRITER AGENT ITINERARY:
    {copywriter_response["output"]}
    
    Please verify:
    1. Does the itinerary match all user requirements? (destination, dates, budget, interests)
    2. Are all requested activities included?
    3. Does the budget stay within the specified range?
    4. Is the itinerary logical and well-structured?
    5. Are there any missing critical information?
    
    Provide a verification report with:
    - Overall consistency score (1-10)
    - List of any discrepancies found
    - Recommendations for improvements
    - Final approval status
    """
    
    try:
        print("Sending verification request to DeepSeek...")
        verification_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a travel planning quality assurance specialist. Your job is to verify that generated itineraries meet all user requirements and maintain consistency."},
                {"role": "user", "content": verification_prompt}
            ],
            model="deepseek-r1-distill-llama-70b",
            temperature=0.0
        )
        
        verification_results = verification_completion.choices[0].message.content
        print("\nDeepSeek Verification Results:")
        print(verification_results)
        
        # Save the final analysis
        save_final_analysis(
            test_name=test_name,
            run_id=run_id,
            verification_results=verification_results
        )
        
    except Exception as e:
        logger.error(f"Error during verification: {str(e)}")
        print(f"\nError during verification: {str(e)}")
        print("Please check the logs for details.")

if __name__ == "__main__":
    # Example test name and run ID
    test_name = "travel_itinerary_generation"
    run_id = "run_20250607_134626"
    main(test_name, run_id) 
