from crewai import Agent
from config import make_llm
from web_tools import web_search, read_webpage

def create_fact_checker():
    return Agent(role="Fact Checker", goal="Verify important factual claims using independent evidence.", backstory="You identify uncertainty and never invent supporting evidence.", llm=make_llm(1100), tools=[web_search, read_webpage], verbose=False, allow_delegation=False)
