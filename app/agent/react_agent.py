from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from app.agent.tools import read_file, write_file_and_commit
from app.agent.prompts import SYSTEM_PROMPT
from app.config import settings

def create_doc_agent():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",  # Changed to smaller model
        api_key=settings.GROQ_API_KEY,
        temperature=0.2
    )
    
    tools = [read_file, write_file_and_commit]
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )
    
    return agent