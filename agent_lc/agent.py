from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from .tools import Tools  
from dotenv import load_dotenv
import os
import time
from .chat_history import chat_history_manager

# Load environment variables
load_dotenv()

class Agent:
    def __init__(self, prompt_text, agent_type):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_text),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.llm = ChatOpenAI(
            model_name="gpt-4o",  # Using a more stable model
            temperature=0.7, 
            streaming=False,  # Disable streaming to prevent errors
            api_key=api_key,
            max_retries=3,  # Add retry logic
            request_timeout=60  # Increase timeout
        )
        
        if agent_type == "web_search":
            self.tools = Tools.setup_tool_web_search()
        elif agent_type == "travel_planner":
            self.tools = Tools.setup_tool_travel_planner()
        elif agent_type == "cross_check":
            self.tools = Tools.setup_tool_cross_check()
            
        print(agent_type, " : ", self.tools)

        self.agent = create_openai_tools_agent(
            self.llm.with_config({"tags": ["agent_llm"]}), self.tools, self.prompt
        )

    def get_agent_executor(self):
        return AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            max_iterations=5,  # Limit iterations to prevent loops
            early_stopping_method="generate"  # Stop early if needed
        )
    
    def get_agent_with_history(self):
        return RunnableWithMessageHistory(
            self.get_agent_executor(),
            chat_history_manager.get_history_by_session_id,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    