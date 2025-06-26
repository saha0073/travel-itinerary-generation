import streamlit as st
from agent_lc.agent import Agent
from agent_lc.prompts import WEB_SEARCH_PROMPT, TRAVEL_PLANNER_PROMPT
from groq import Groq
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import time
import uuid
from agent_lc.chat_history import chat_history_manager

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Travel Planning System",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if "user_requirements" not in st.session_state:
    st.session_state.user_requirements = ""
if "strategist_response" not in st.session_state:
    st.session_state.strategist_response = ""
if "copywriter_response" not in st.session_state:
    st.session_state.copywriter_response = ""
if "verification_response" not in st.session_state:
    st.session_state.verification_response = ""
if "session_id_strategist" not in st.session_state:
    st.session_state.session_id_strategist = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False
if "current_agent" not in st.session_state:
    st.session_state.current_agent = "none"
if "agent_outputs" not in st.session_state:
    st.session_state.agent_outputs = {"strategist": "", "copywriter": "", "verification": ""}

def initialize_agents():
    """Initialize all agents"""
    try:
        # Initialize Strategist Agent with chat history
        strategist_agent = Agent(prompt_text=WEB_SEARCH_PROMPT, agent_type="web_search")
        strategist_executor = strategist_agent.get_agent_with_history()
        
        # Initialize Copywriter Agent
        copywriter_agent = Agent(prompt_text=TRAVEL_PLANNER_PROMPT, agent_type="travel_planner")
        copywriter_executor = copywriter_agent.get_agent_executor()
        
        # Initialize Groq client for DeepSeek
        groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        return strategist_executor, copywriter_executor, groq_client
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None

def get_copywriter_agent_prompt(user_requirements, strategist_analysis):
    """Run the copywriter agent to create itinerary"""
    try:
        
        prompt = f"""
        Based on the user requirements collected by the Strategist Agent, create a detailed travel itinerary.
        
        User Requirements: {user_requirements}
        Strategist Analysis: {strategist_analysis}
        
        Please create a comprehensive day-by-day itinerary including:
        - Hotel recommendations with pricing
        - Flight options with pricing
        - Daily activities and attractions
        - Restaurant recommendations
        - Budget breakdown
        """
        
        return prompt
    except Exception as e:
        return f"Error in copywriter agent: {str(e)}"

def run_verification_agent(user_requirements, strategist_analysis, copywriter_itinerary):
    """Run the verification agent using DeepSeek"""
    try:
        _, _, groq_client = initialize_agents()
        if groq_client is None:
            return "Error: Could not initialize verification agent"
        
        verification_prompt = f"""
        You are a travel planning quality assurance specialist. Compare the user requirements with the generated itinerary to ensure consistency and completeness.
        
        USER REQUIREMENTS:
        {user_requirements}
        
        STRATEGIST AGENT ANALYSIS:
        {strategist_analysis}
        
        COPYWRITER AGENT ITINERARY:
        {copywriter_itinerary}
        
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
        
        with st.spinner("🔍 DeepSeek Agent is verifying your itinerary..."):
            verification_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a travel planning quality assurance specialist. Your job is to verify that generated itineraries meet all user requirements and maintain consistency."},
                    {"role": "user", "content": verification_prompt}
                ],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.0
            )
        
        return verification_completion.choices[0].message.content
    except Exception as e:
        return f"Error in verification agent: {str(e)}"

def process_travel_request(user_input):
    """Process the complete travel request through all agents"""
    try:
        # Initialize agents
        strategist_executor, copywriter_executor, groq_client = initialize_agents()
        if strategist_executor is None or copywriter_executor is None:
            return "Error: Could not initialize agents"
        
        # Step 1: Strategist Agent - Analyze requirements
        st.session_state.current_agent = "strategist"
        with st.spinner("🤔 Strategist Agent is analyzing your requirements..."):
            strategist_response = strategist_executor.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": st.session_state["session_id_strategist"]}}
            )
            strategist_output = strategist_response.get('output')
        
        # Step 2: Copywriter Agent - Create itinerary
        st.session_state.current_agent = "copywriter"
        with st.spinner("✍️ Copywriter Agent is creating your itinerary..."):
            copywriter_prompt = get_copywriter_agent_prompt(user_input, strategist_output)
            copywriter_response = copywriter_executor.invoke({
                "input": copywriter_prompt
            })
            copywriter_output = copywriter_response.get('output')
        
        # Step 3: Verification Agent - Verify itinerary
        st.session_state.current_agent = "verification"
        with st.spinner("🔍 DeepSeek Agent is verifying your itinerary..."):
            verification_output = run_verification_agent(user_input, strategist_output, copywriter_output)
        
        return strategist_output, copywriter_output, verification_output
        
    except Exception as e:
        st.error(f"Error in process_travel_request: {str(e)}")
        return f"Error processing request: {str(e)}", "", ""

def main():
    # Header
    st.title("✈️ AI Travel Planning System")
    st.markdown("**Multi-Agent Travel Itinerary Generator**")
    
    # Sidebar for progress tracking
    with st.sidebar:
        st.header("📋 System Status")
        
        if st.session_state.processing_complete:
            st.success("✅ All Agents Completed")
            st.success("🤔 Strategist Agent: Done")
            st.success("✍️ Copywriter Agent: Done")
            st.success("🔍 DeepSeek Agent: Done")
        else:
            if st.session_state.current_agent == "strategist":
                st.info("⏳ Strategist Agent: Working...")
                st.success("✅ Copywriter Agent: Ready")
                st.success("✅ DeepSeek Agent: Ready")
            elif st.session_state.current_agent == "copywriter":
                st.success("✅ Strategist Agent: Done")
                st.info("⏳ Copywriter Agent: Working...")
                st.success("✅ DeepSeek Agent: Ready")
            elif st.session_state.current_agent == "verification":
                st.success("✅ Strategist Agent: Done")
                st.success("✅ Copywriter Agent: Done")
                st.info("⏳ DeepSeek Agent: Working...")
            else:
                st.info("⏳ Waiting for travel request")
                st.info("🤔 Strategist Agent: Ready")
                st.info("✍️ Copywriter Agent: Ready")
                st.info("🔍 DeepSeek Agent: Ready")
        
        # Reset button
        if st.button("🔄 Start New Planning Session"):
            st.session_state.user_requirements = ""
            st.session_state.strategist_response = ""
            st.session_state.copywriter_response = ""
            st.session_state.verification_response = ""
            st.session_state.session_id_strategist = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.processing_complete = False
            st.session_state.current_agent = "none"
            st.session_state.agent_outputs = {"strategist": "", "copywriter": "", "verification": ""}
            st.rerun()
    
    # Main chat interface
    st.header("💬 AI Travel Planning Chat")
    st.markdown("**Tell us about your travel plans and we'll create a complete itinerary for you!**")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Describe your travel plans (e.g., 'I want to travel to Manali from Delhi, September 1-10, 2025. Please create a travel itinerary.')"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Process the complete request
        st.info("🚀 Starting travel planning process...")
        strategist_output, copywriter_output, verification_output = process_travel_request(prompt)
        
        # Add agent responses to chat
        if strategist_output and not strategist_output.startswith("Error"):
            st.session_state.messages.append({"role": "assistant", "content": f"🤔 **Strategist Agent Analysis:**\n\n{strategist_output}"})
            st.chat_message("assistant").write(f"🤔 **Strategist Agent Analysis:**\n\n{strategist_output}")
            st.session_state.agent_outputs["strategist"] = strategist_output
        
        if copywriter_output and not copywriter_output.startswith("Error"):
            st.session_state.messages.append({"role": "assistant", "content": f"✍️ **Copywriter Agent Itinerary:**\n\n{copywriter_output}"})
            st.chat_message("assistant").write(f"✍️ **Copywriter Agent Itinerary:**\n\n{copywriter_output}")
            st.session_state.agent_outputs["copywriter"] = copywriter_output
        
        if verification_output and not verification_output.startswith("Error"):
            st.session_state.messages.append({"role": "assistant", "content": f"🔍 **DeepSeek Verification Report:**\n\n{verification_output}"})
            st.chat_message("assistant").write(f"🔍 **DeepSeek Verification Report:**\n\n{verification_output}")
            st.session_state.agent_outputs["verification"] = verification_output
        
        # Mark processing as complete
        st.session_state.processing_complete = True
        
        # Show completion message
        st.success("🎉 Travel planning completed! Check the chat above for your complete itinerary and verification report.")
        
        # Force rerun to update sidebar
        st.rerun()

if __name__ == "__main__":
    main() 