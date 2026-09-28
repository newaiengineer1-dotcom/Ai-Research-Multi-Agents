from crewai import Agent
from config import make_llm
from web_tools import web_search

def create_research_director():
    return Agent(role="Research Director", goal="Plan a focused evidence-based investigation.", backstory="You create short, practical research plans and evidence-oriented search directions.", llm=make_llm(900), tools=[web_search], verbose=False, allow_delegation=False)
