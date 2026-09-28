# CrewAI/Groq compatibility workaround for unsupported cache_breakpoint.
try:
    import crewai.llms.cache as crew_cache
    crew_cache.mark_cache_breakpoint = lambda msg: msg
except Exception:
    pass

import re
import time
from crewai import Crew, Process, Task
from research_director import create_research_director
from web_researcher import create_web_researcher
from source_analyst import create_source_analyst
from fact_checker import create_fact_checker
from research_synthesizer import create_research_synthesizer
from report_writer import create_report_writer

BETWEEN_AGENTS_SECONDS = 5
MAX_RETRIES = 6

def _wait_for_rate_limit(error_text, attempt):
    m = re.search(r"try again in\s+([0-9.]+)s", error_text, re.I)
    seconds = float(m.group(1))+2 if m else 12+(attempt*8)
    time.sleep(min(seconds,65))

def _run_stage(agent, description, expected_output):
    task=Task(description=description, expected_output=expected_output, agent=agent)
    crew=Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    for attempt in range(MAX_RETRIES):
        try:
            result=crew.kickoff()
            return result.raw if hasattr(result,"raw") else str(result)
        except Exception as exc:
            text=str(exc); low=text.lower()
            limited=("ratelimit" in low or "rate limit" in low or "rate_limit_exceeded" in low or "tokens per minute" in low or "429" in low)
            if not limited: raise
            if attempt == MAX_RETRIES-1:
                raise RuntimeError("Groq rate limit remained active after automatic retries. Wait about one minute and run the research once.") from exc
            _wait_for_rate_limit(text,attempt)

def _pause(): time.sleep(BETWEEN_AGENTS_SECONDS)

def run_research(topic, depth="Quick", source_limit=5, status_callback=None):
    depth_instruction={"Quick":"Keep the investigation compact and focus only on the most useful evidence.","Standard":"Perform a balanced investigation with several independent sources.","Deep":"Cover important subtopics and look for conflicting evidence, but keep every stage compact."}.get(depth,"Keep the investigation compact.")
    def status(name,state):
        if status_callback: status_callback(name,state)

    status("Research Director","Working"); director=create_research_director()
    plan=_run_stage(director,f"""Research question:
{topic}

Depth: {depth}
{depth_instruction}
Create a COMPACT research plan. Give exactly 5 important subquestions and the evidence needed for each. Maximum 500 words. Use web_search at least once. Do not write the final report.""","A compact 5-question research plan under 500 words.")
    status("Research Director","Completed"); _pause()

    status("Web Researcher","Working"); researcher=create_web_researcher()
    research=_run_stage(researcher,f"""Question:
{topic}

Plan:
{plan}

Find up to {source_limit} useful sources. {depth_instruction}
You MUST use web_search and read_webpage. For each source return only TITLE, URL, KEY EVIDENCE. Maximum 90 words per source. Prefer official, primary, academic, institutional, or reputable sources. Do not invent URLs or facts.""","A compact source dossier with titles, URLs, and evidence.")
    status("Web Researcher","Completed"); _pause()

    status("Source Analyst","Working"); analyst=create_source_analyst()
    source_analysis=_run_stage(analyst,f"""Question:
{topic}

Sources:
{research}

Evaluate the most useful sources. Use read_webpage on relevant URLs. For each important source give SOURCE, QUALITY, RELEVANCE, LIMITATION. Maximum 600 words total. Do not rewrite the sources.""","A compact source-quality assessment under 600 words.")
    status("Source Analyst","Completed"); _pause()

    status("Fact Checker","Working"); checker=create_fact_checker()
    fact_check=_run_stage(checker,f"""Question:
{topic}

Research:
{research}

Source analysis:
{source_analysis}

Verify only the most important claims. Use web_search and read_webpage. Return up to 8 items using CLAIM, STATUS, EVIDENCE, URL. STATUS must be SUPPORTED, CONFLICTING, or UNVERIFIED. Maximum 800 words.""","A compact fact-checking brief with claim status and URLs.")
    status("Fact Checker","Completed"); _pause()

    status("Research Synthesizer","Working"); synthesizer=create_research_synthesizer()
    synthesis=_run_stage(synthesizer,f"""Question:
{topic}

Research:
{research}

Source analysis:
{source_analysis}

Fact check:
{fact_check}

Create a compact evidence brief. Include key findings, strongest evidence, disagreements, uncertainties, and source URLs. Maximum 1000 words. Do not repeat the full research dossier. Do not invent evidence.""","A compact evidence brief under 1000 words.")
    status("Research Synthesizer","Completed"); _pause()

    status("Report Writer","Working"); writer=create_report_writer()
    report=_run_stage(writer,f"""Research question:
{topic}

Evidence brief:
{synthesis}

Fact-check:
{fact_check}

Write the final research report in Markdown. Include Executive Summary, Methodology, Main Findings, Analysis, Limitations, Unresolved Questions, and References. Use only supplied evidence and URLs. Do not invent statistics, quotations, sources, or URLs. Maximum 1800 words.""","A professional Markdown research report with references.")
    status("Report Writer","Completed")
    return report
