from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
from app.config import settings

def build_llm():
    return LLM(
        model="groq/openai/gpt-oss-20b",  # ← CORRECT FORMAT!
        api_key=settings.GROQ_API_KEY,
        temperature=0.2,
    )

def run_doc_crew(file_path: str, file_content: str) -> str:
    """Runs a 2-agent crew (Writer, Reviewer-Editor) and returns the final file content."""
    llm = build_llm()

    writer = Agent(
        role="Documentation Writer",
        goal="Add Google-style docstrings and pytest unit tests to Python code",
        backstory="An expert Python developer who writes clear, accurate documentation and thorough tests.",
        llm=llm,
        verbose=False,
    )

    reviewer = Agent(
        role="Reviewer and Editor",
        goal="Review the writer's output and produce the final corrected file",
        backstory="A senior engineer who reviews code for correctness and outputs only the final clean file.",
        llm=llm,
        verbose=False,
    )

    write_task = Task(
        description=f"""File: {file_path}

{file_content}

Add Google-style docstrings to all functions/classes missing them, and add pytest unit tests. Output the complete updated file content only.""",
        expected_output="The complete updated Python file with docstrings and tests added.",
        agent=writer,
    )

    review_task = Task(
        description="Review the writer's file for correctness and completeness, fix any issues, and output ONLY the final complete Python file content — no explanations, no markdown fences.",
        expected_output="The final complete Python file content, ready to commit.",
        agent=reviewer,
        context=[write_task],
    )

    crew = Crew(
        agents=[writer, reviewer],
        tasks=[write_task, review_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)