from crewai import Agent
from config import make_llm
from web_tools import read_webpage

def create_source_analyst():
    return Agent(role="Source Analyst", goal="Assess source quality, relevance, and limitations.", backstory="You distinguish strong evidence from weak or incomplete evidence.", llm=make_llm(900), tools=[read_webpage], verbose=False, allow_delegation=False)
