from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from app.agent.tools import read_file, create_pull_request, write_file_and_commit
from app.agent.prompts import SYSTEM_PROMPT
from app.config import settings

def create_doc_agent():
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        api_key=settings.GROQ_API_KEY,
        temperature=0.2
    )
    
    tools = [read_file, write_file_and_commit, create_pull_request]
    
    template = """{system_prompt}
    
    You have access to these tools: {tools}
    
    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought: {agent_scratchpad}"""
    
    prompt = PromptTemplate.from_template(template)
    
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )
    
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return executor