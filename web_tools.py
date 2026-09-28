import re
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from pydantic import Field

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the public web with DuckDuckGo. Input is a search query."
    max_results: int = Field(default=5, description="Maximum number of results.")
    def _run(self, query: str) -> str:
        limit=max(1,min(int(self.max_results),8))
        url="https://html.duckduckgo.com/html/?q="+quote_plus(query)
        r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=20); r.raise_for_status()
        soup=BeautifulSoup(r.text,"html.parser"); out=[]
        for item in soup.select(".result"):
            link=item.select_one(".result__a"); snip=item.select_one(".result__snippet")
            if not link: continue
            href=link.get("href","").strip(); title=link.get_text(" ",strip=True); text=snip.get_text(" ",strip=True) if snip else ""
            if href and title: out.append(f"TITLE: {title}\nURL: {href}\nSNIPPET: {text[:300]}")
            if len(out)>=limit: break
        return "\n\n".join(out) if out else "No search results found."

class ReadWebpageTool(BaseTool):
    name: str = "read_webpage"
    description: str = "Read a public webpage URL and return a short clean text extract."
    def _run(self, url: str) -> str:
        if not re.match(r"^https?://",url.strip(),re.I): return "Invalid URL."
        r=requests.get(url.strip(),headers={"User-Agent":"Mozilla/5.0"},timeout=25,allow_redirects=True); r.raise_for_status()
        soup=BeautifulSoup(r.text,"html.parser")
        for tag in soup(["script","style","noscript","svg","nav","footer","header"]): tag.decompose()
        text=re.sub(r"\s+"," ",soup.get_text(" ",strip=True))
        return text[:7000]

web_search=WebSearchTool(max_results=5)
read_webpage=ReadWebpageTool()
