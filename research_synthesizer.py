from crewai import Agent
from config import make_llm
from web_tools import web_search

def create_research_synthesizer():
    return Agent(role="Research Synthesizer", goal="Turn verified evidence into a compact evidence brief.", backstory="You synthesize evidence without hiding disagreement or uncertainty.", llm=make_llm(1300), tools=[web_search], verbose=False, allow_delegation=False)
