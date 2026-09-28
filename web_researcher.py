from crewai import Agent
from config import make_llm
from web_tools import web_search, read_webpage

def create_web_researcher():
    return Agent(role="Web Researcher", goal="Find reliable web sources and concise evidence.", backstory="You prioritize primary, official, academic, institutional, and reputable sources.", llm=make_llm(1100), tools=[web_search, read_webpage], verbose=False, allow_delegation=False)
