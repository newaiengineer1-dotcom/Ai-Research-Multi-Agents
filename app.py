import os
from datetime import datetime
import streamlit as st
from crew import run_research

st.set_page_config(page_title="Research Multi-Agent",page_icon="🔬",layout="wide")
st.markdown("""<style>
.stApp{background:#0b1020}.hero{padding:28px;border-radius:20px;background:linear-gradient(135deg,#111a33,#172554);border:1px solid #26355f;margin-bottom:22px}.hero h1{margin:0;color:#fff;font-size:2.4rem}.hero p{color:#cbd5e1}.agent{padding:12px 15px;border-radius:12px;background:#111827;border:1px solid #273449;margin-bottom:7px}.working{border-color:#60a5fa;background:#13213b}.name{color:#f8fafc;font-weight:700}.state{color:#94a3b8;font-size:.9rem}</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🔬 Research Multi-Agent Team</h1><p>Six sequential CrewAI agents using Groq GPT-OSS 120B and web research.</p></div>',unsafe_allow_html=True)

AGENTS=["Research Director","Web Researcher","Source Analyst","Fact Checker","Research Synthesizer","Report Writer"]
if "states" not in st.session_state: st.session_state.states={a:"Waiting" for a in AGENTS}
if "report" not in st.session_state: st.session_state.report=""

def render():
    html=[]
    for name in AGENTS:
        state=st.session_state.states[name]; cls="agent working" if state=="Working" else "agent"
        icon="🟡" if state=="Working" else ("🟢" if state=="Completed" else "⚪")
        html.append(f'<div class="{cls}"><div class="name">{icon} {name}</div><div class="state">{state}</div></div>')
    box.markdown("".join(html),unsafe_allow_html=True)

left,right=st.columns([2,1])
with left: topic=st.text_area("Research question",placeholder="Example: What are the main benefits and challenges of battery energy storage systems?",height=130)
with right:
    depth=st.selectbox("Research depth",["Quick","Standard","Deep"])
    source_limit=st.slider("Maximum sources",3,6,5)

st.markdown("### Agent Activity"); box=st.empty(); render()

def callback(name,state): st.session_state.states[name]=state; render()

if st.button("🚀 Start Multi-Agent Research",type="primary",use_container_width=True):
    if not topic.strip(): st.warning("Please enter a research question first."); st.stop()
    if not os.getenv("GROQ_API_KEY"): st.error("GROQ_API_KEY is not configured. Add it to Streamlit Secrets."); st.stop()
    st.session_state.states={a:"Waiting" for a in AGENTS}; st.session_state.report=""; render()
    try:
        with st.spinner("Research team is working sequentially..."):
            st.session_state.report=run_research(topic.strip(),depth,source_limit,callback)
    except Exception as exc:
        st.error(f"Research failed: {exc}")
        st.info("If Groq reports a TPM limit, wait about one minute and run the research once. Temporary 429 errors are retried automatically.")

if st.session_state.report:
    st.markdown("### Final Research Report")
    st.success("Research completed successfully.")
    st.markdown(st.session_state.report)
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button("⬇️ Download Markdown Report",st.session_state.report,f"research_report_{stamp}.md","text/markdown",use_container_width=True)
