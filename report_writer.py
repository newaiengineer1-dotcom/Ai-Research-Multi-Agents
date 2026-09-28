from crewai import Agent
from config import make_llm

def create_report_writer():
    return Agent(role="Report Writer", goal="Write a clear professional report from supplied evidence.", backstory="You use only supplied evidence and clearly state limitations.", llm=make_llm(2000), tools=[], verbose=False, allow_delegation=False)
