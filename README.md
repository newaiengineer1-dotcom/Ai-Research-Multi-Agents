# Research Multi-Agent Team

A beginner-friendly six-agent research app using Streamlit, CrewAI, Groq GPT-OSS 120B, LiteLLM, DuckDuckGo search, and BeautifulSoup.

## Agents
1. Research Director
2. Web Researcher
3. Source Analyst
4. Fact Checker
5. Research Synthesizer
6. Report Writer

## Important Groq fix
The app is designed for an 8K TPM environment: prompts and outputs are intentionally compact, agents run sequentially, there is a 5-second delay between stages, and 429 errors are automatically retried. Groq rate limits are organization-level; code cannot increase the organization's limit.

The project also includes the CrewAI workaround for the `cache_breakpoint` field that Groq rejects.

## Local setup
Use Python 3.12.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
streamlit run app.py
```

## Streamlit Cloud
1. Upload all files to GitHub.
2. Create/select the Streamlit app with `app.py` as the main file.
3. Use Python 3.12 if the deployment setting asks for it.
4. Add this secret:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

5. Deploy or reboot.

Never upload your API key, `.env`, `.venv`, or `.streamlit/secrets.toml`.

## First test
Use a short question and select `Quick`. Do not click the research button repeatedly while a run is active.
