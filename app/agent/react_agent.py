from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from app.agent.tools import make_write_file_tool
from app.config import settings


def create_doc_agent(repo_path: str):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.GROQ_API_KEY,
        temperature=0.2,
    )

    tools = [make_write_file_tool(repo_path)]

    return create_react_agent(model=llm, tools=tools)
