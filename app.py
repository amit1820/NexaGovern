"""
NexaGovern — AI Agent Visibility & Governance Platform (MVP)
Professional dashboard — clean design, no emojis, polished UI.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import re

from risk_engine import (
    classify_risk_tier, generate_gap_analysis,
    HIGH_RISK_USE_CASES, DATA_SENSITIVITY, HIGH_RISK_REQUIREMENTS,
)
from sample_data import COMMON_AGENTS, SAMPLE_POLICIES, SAMPLE_VIOLATIONS

st.set_page_config(page_title="NexaGovern", page_icon="N", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif}
.main .block-container{padding:1rem 2rem 2rem 2rem;max-width:1280px}
#MainMenu,footer,header{visibility:hidden}
.stDeployButton{display:none}
.brand-header{background:linear-gradient(135deg,#0B1929 0%,#132F4C 50%,#0A3D62 100%);padding:1.8rem 2.5rem;border-radius:16px;margin-bottom:2rem;position:relative;overflow:hidden;border:1px solid rgba(0,180,216,0.15)}
.brand-header::before{content:'';position:absolute;top:-50%;right:-10%;width:300px;height:300px;background:radial-gradient(circle,rgba(0,180,216,0.08) 0%,transparent 70%);border-radius:50%}
.brand-name{font-size:1.75rem;font-weight:700;color:#FFF;letter-spacing:-0.5px;margin:0}
.brand-tagline{font-size:0.9rem;font-weight:400;color:#64B5F6;margin:0.25rem 0 0 0;letter-spacing:0.3px}
.metric-card{background:#0B1929;border:1px solid #1E3A5F;border-radius:12px;padding:1.25rem 1.5rem;transition:border-color 0.2s}
.metric-card:hover{border-color:#00B4D8}
.metric-value{font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:600;color:#E3F2FD;line-height:1;margin-bottom:0.35rem}
.metric-label{font-size:0.75rem;font-weight:500;color:#78909C;text-transform:uppercase;letter-spacing:0.8px}
.metric-accent-cyan .metric-value{color:#00B4D8}
.metric-accent-red .metric-value{color:#EF5350}
.metric-accent-orange .metric-value{color:#FFA726}
.metric-accent-green .metric-value{color:#66BB6A}
.section-title{font-size:1.1rem;font-weight:600;color:#E3F2FD;margin:2rem 0 1rem 0;padding-bottom:0.5rem;border-bottom:1px solid #1E3A5F;letter-spacing:-0.2px}
.agent-card{background:#0B1929;border:1px solid #1E3A5F;border-radius:10px;padding:1.1rem 1.4rem;margin-bottom:0.75rem;transition:border-color 0.2s,transform 0.1s}
.agent-card:hover{border-color:#2196F3;transform:translateY(-1px)}
.agent-name{font-size:0.95rem;font-weight:600;color:#E3F2FD;margin:0 0 0.3rem 0}
.agent-meta{font-size:0.8rem;color:#78909C;margin:0;line-height:1.5}
.agent-desc{font-size:0.82rem;color:#90A4AE;margin:0.4rem 0 0 0;line-height:1.5}
.badge{display:inline-block;padding:3px 12px;border-radius:100px;font-size:0.7rem;font-weight:600;letter-spacing:0.5px;text-transform:uppercase}
.badge-high{background:rgba(239,83,80,0.15);color:#EF5350;border:1px solid rgba(239,83,80,0.3)}
.badge-limited{background:rgba(255,167,38,0.15);color:#FFA726;border:1px solid rgba(255,167,38,0.3)}
.badge-minimal{background:rgba(102,187,106,0.15);color:#66BB6A;border:1px solid rgba(102,187,106,0.3)}
.badge-critical{background:rgba(239,83,80,0.15);color:#EF5350;border:1px solid rgba(239,83,80,0.3)}
.badge-open{background:rgba(239,83,80,0.1);color:#EF5350}
.badge-resolved{background:rgba(102,187,106,0.1);color:#66BB6A}
.violation-card{background:#0B1929;border:1px solid #1E3A5F;border-radius:10px;padding:1rem 1.3rem;margin-bottom:0.6rem}
.violation-card.sev-critical{border-left:3px solid #EF5350}
.violation-card.sev-high{border-left:3px solid #FFA726}
.violation-card.sev-medium{border-left:3px solid #FDD835}
.policy-card{background:#0B1929;border:1px solid #1E3A5F;border-radius:10px;padding:1rem 1.3rem;margin-bottom:0.6rem}
.policy-active{border-left:3px solid #66BB6A}
.policy-inactive{border-left:3px solid #546E7A}
.gap-item{background:#0B1929;border:1px solid #1E3A5F;border-radius:8px;padding:0.9rem 1.2rem;margin-bottom:0.5rem}
.gap-met{border-left:3px solid #66BB6A}
.gap-notmet{border-left:3px solid #EF5350}
.alert-box{border-radius:10px;padding:1.2rem 1.5rem;margin:0.8rem 0}
.alert-danger{background:rgba(239,83,80,0.08);border:1px solid rgba(239,83,80,0.25)}
.alert-success{background:rgba(102,187,106,0.08);border:1px solid rgba(102,187,106,0.25)}
.alert-info{background:rgba(33,150,243,0.08);border:1px solid rgba(33,150,243,0.25)}
[data-testid="stSidebar"]{background:#070F1A}
.stTabs [data-baseweb="tab-list"]{gap:0;border-bottom:1px solid #1E3A5F}
.stTabs [data-baseweb="tab"]{font-weight:500;font-size:0.85rem;padding:0.75rem 1.5rem;color:#78909C;letter-spacing:0.2px}
.stTabs [aria-selected="true"]{color:#00B4D8 !important;border-bottom-color:#00B4D8 !important}
.js-plotly-plot .plotly .modebar{display:none !important}
.connector-item{display:flex;align-items:center;gap:0.6rem;padding:0.5rem 0;border-bottom:1px solid #0F2136}
.connector-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-active{background:#66BB6A}
.dot-pending{background:#FFA726}
.connector-name{font-size:0.82rem;font-weight:500;color:#B0BEC5}
.connector-status{font-size:0.7rem;color:#546E7A;margin-left:auto}
.compliance-bar-bg{background:#1E3A5F;border-radius:6px;height:8px;width:100%;margin-top:0.5rem}
.compliance-bar-fill{height:8px;border-radius:6px;transition:width 0.5s ease}
</style>
""", unsafe_allow_html=True)

if "agents" not in st.session_state:
    st.session_state.agents = []
    for agent in COMMON_AGENTS:
        c = classify_risk_tier(agent["use_case"], agent["data_types"], agent["has_human_oversight"], agent["decision_impact"])
        st.session_state.agents.append({**agent, "classification": c})
if "policies" not in st.session_state:
    st.session_state.policies = SAMPLE_POLICIES.copy()
if "violations" not in st.session_state:
    st.session_state.violations = SAMPLE_VIOLATIONS.copy()

agents = st.session_state.agents

st.markdown('<div class="brand-header"><p class="brand-name">NexaGovern</p><p class="brand-tagline">AI Agent Visibility and Governance Platform</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### Connected Platforms")
    for name, status, active in [("OpenAI / Azure OpenAI","Active",True),("Slack","Active",True),("HuggingFace","Active",True),("Microsoft Copilot","Pending",False)]:
        dot = "dot-active" if active else "dot-pending"
        st.markdown(f'<div class="connector-item"><div class="connector-dot {dot}"></div><span class="connector-name">{name}</span><span class="connector-status">{status}</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### EU AI Act Deadline")
    days_left = (datetime(2026,8,2) - datetime.now()).days
    pct_r = max(0, min(100, int((1 - days_left/365)*100)))
    bc = "#EF5350" if days_left < 90 else "#FFA726" if days_left < 180 else "#00B4D8"
    st.markdown(f'<div style="text-align:center;margin:0.5rem 0"><div style="font-family:JetBrains Mono,monospace;font-size:2rem;font-weight:600;color:{bc}">{days_left}</div><div style="font-size:0.75rem;color:#78909C;text-transform:uppercase;letter-spacing:0.5px">Days Remaining</div></div><div class="compliance-bar-bg"><div class="compliance-bar-fill" style="width:{pct_r}%;background:{bc}"></div></div><p style="font-size:0.7rem;color:#546E7A;margin-top:0.5rem;text-align:center">High-risk provisions enforceable Aug 2, 2026</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Overview")
    hr = sum(1 for a in agents if a["classification"]["tier"]=="HIGH")
    ov = sum(1 for v in st.session_state.violations if v["status"]=="Open")
    for lb, vl, cl in [("Total AI Systems",str(len(agents)),"#E3F2FD"),("High Risk",str(hr),"#EF5350"),("Open Violations",str(ov),"#FFA726")]:
        st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #0F2136"><span style="font-size:0.8rem;color:#78909C">{lb}</span><span style="font-family:JetBrains Mono,monospace;font-size:0.9rem;font-weight:600;color:{cl}">{vl}</span></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Discovery", "Policy Engine", "Risk Dashboard", "Gap Analysis"])

with tab1:
    st.markdown('<div class="section-title">AI Systems Inventory</div>', unsafe_allow_html=True)
    c1,c2,_ = st.columns([2,2,6])
    with c1: df_ = st.selectbox("Department",["All"]+sorted(set(a["department"] for a in agents)),key="d1")
    with c2: rf_ = st.selectbox("Risk Tier",["All","HIGH","LIMITED","MINIMAL"],key="r1")
    flt = agents
    if df_!="All": flt=[a for a in flt if a["department"]==df_]
    if rf_!="All": flt=[a for a in flt if a["classification"]["tier"]==rf_]
    for a in flt:
        c=a["classification"]; bc_=f"badge-{c['tier'].lower()}"
        st.markdown(f'<div class="agent-card"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><p class="agent-name">{a["name"]}</p><p class="agent-meta">{a["platform"]}  |  {a["department"]}  |  Risk Score: {c["score"]}/100</p></div><span class="badge {bc_}">{c["tier"]}</span></div><p class="agent-desc">{a["description"]}</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Register New AI System</div>', unsafe_allow_html=True)
    with st.form("add_agent"):
        c1,c2=st.columns(2)
        with c1:
            nn=st.text_input("System Name",placeholder="e.g., Revenue Forecast Model")
            np_=st.selectbox("Platform",["OpenAI","Azure OpenAI","HuggingFace","Slack Bot","Microsoft Copilot","Custom (Python/sklearn)","Custom (Other)","Third-party SaaS"])
            nd=st.selectbox("Department",["Finance","HR","Risk / Lending","Compliance","Customer Support","Marketing","Engineering","Operations","Multiple","Other"])
        with c2:
            uco=[("general","General purpose / productivity")]+[(k,v["label"]) for k,v in HIGH_RISK_USE_CASES.items()]
            nu=st.selectbox("Primary Use Case",uco,format_func=lambda x:x[1])
            do=[(k,v["label"]) for k,v in DATA_SENSITIVITY.items()]
            ndt=st.multiselect("Data Types Accessed",do,format_func=lambda x:x[1])
            io=[("informational","Informational only"),("recommendation","Makes recommendations"),("automated_decision","Makes automated decisions")]
            ni=st.selectbox("Decision Impact",io,format_func=lambda x:x[1])
        nde=st.text_area("Description",placeholder="What does this system do?",height=80)
        no=st.checkbox("Human oversight mechanism exists",value=True)
        if st.form_submit_button("Classify and Register",use_container_width=True) and nn:
            uk=nu[0] if isinstance(nu,tuple) else nu; dk=[d[0] if isinstance(d,tuple) else d for d in ndt]; ik=ni[0] if isinstance(ni,tuple) else ni
            cl=classify_risk_tier(uk,dk,no,ik)
            st.session_state.agents.append({"name":nn,"platform":np_,"department":nd,"use_case":uk,"description":nde,"data_types":dk,"decision_impact":ik,"has_human_oversight":no,"classification":cl})
            st.success(f"{nn} registered as {cl['tier']} RISK (score: {cl['score']}/100)")
            for r in cl["reasons"]: st.warning(r)

with tab2:
    st.markdown('<div class="section-title">Governance Policies</div>', unsafe_allow_html=True)
    for p in st.session_state.policies:
        ac="policy-active" if p["active"] else "policy-inactive"; st_="Active" if p["active"] else "Inactive"
        sc="badge-critical" if p["severity"]=="Critical" else "badge-limited" if p["severity"]=="High" else "badge-minimal"
        st.markdown(f'<div class="policy-card {ac}"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><p class="agent-name">{p["name"]}</p><p class="agent-meta">{p["description"]}</p></div><div style="display:flex;gap:0.5rem;align-items:center"><span class="badge {sc}">{p["severity"]}</span><span style="font-size:0.7rem;color:{"#66BB6A" if p["active"] else "#546E7A"}">{st_}</span></div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Policy Violations</div>', unsafe_allow_html=True)
    for v in st.session_state.violations:
        sv=f"sev-{v['severity'].lower()}"; stc="badge-open" if v["status"]=="Open" else "badge-resolved"
        st.markdown(f'<div class="violation-card {sv}"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><p class="agent-name">{v["agent"]}</p><p class="agent-meta">{v["policy"]}</p><p class="agent-desc">{v["detail"]}</p></div><div style="text-align:right;flex-shrink:0"><span class="badge {stc}">{v["status"]}</span><p style="font-size:0.7rem;color:#546E7A;margin:0.3rem 0 0 0">{v["timestamp"]}</p></div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">PII Detection — Live Prompt Scanner</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.82rem;color:#78909C;margin-bottom:1rem">Simulates monitoring an OpenAI API call for personally identifiable information before it reaches the model.</p>', unsafe_allow_html=True)
    dp=st.text_area("Enter a prompt to scan:",value="Summarize the account for customer John Smith, email john.smith@example.com, card ending 4532.",height=100,label_visibility="collapsed")
    st.markdown('<p style="font-size:0.75rem;color:#546E7A">Try including names, email addresses, credit card numbers, or SSNs.</p>', unsafe_allow_html=True)
    if st.button("Scan for PII",use_container_width=True):
        fi=[]
        if re.search(r'[A-Z][a-z]+ [A-Z][a-z]+',dp): fi.append(("Person Name","High"))
        if re.search(r'[\w.-]+@[\w.-]+\.\w+',dp): fi.append(("Email Address","High"))
        if re.search(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b|\bcard\s+(?:ending|number)\s+\d{4}\b',dp,re.I): fi.append(("Credit Card Number","Critical"))
        if re.search(r'\b\d{3}-\d{2}-\d{4}\b',dp): fi.append(("SSN","Critical"))
        if fi:
            st.markdown(f'<div class="alert-box alert-danger"><p style="color:#EF5350;font-weight:600;font-size:0.95rem;margin:0 0 0.5rem 0">POLICY VIOLATION — {len(fi)} PII element(s) detected</p><p style="color:#FFCDD2;font-size:0.85rem;margin:0">This prompt would be blocked before reaching the LLM.</p></div>', unsafe_allow_html=True)
            for item,sev in fi:
                bc__="badge-critical" if sev=="Critical" else "badge-high"
                st.markdown(f'<div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #1E3A5F"><span class="badge {bc__}">{sev}</span><span style="color:#E3F2FD;font-size:0.85rem">{item} detected</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="alert-box alert-info" style="margin-top:1rem"><p style="color:#90CAF9;font-size:0.85rem;margin:0"><strong>Action taken:</strong> Prompt blocked. Violation logged to audit trail. Compliance officer notified.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box alert-success"><p style="color:#A5D6A7;font-size:0.85rem;margin:0">No PII detected. Prompt cleared for submission.</p></div>', unsafe_allow_html=True)

with tab3:
    agents=st.session_state.agents; total=len(agents)
    high=sum(1 for a in agents if a["classification"]["tier"]=="HIGH")
    limited=sum(1 for a in agents if a["classification"]["tier"]=="LIMITED")
    minimal=sum(1 for a in agents if a["classification"]["tier"]=="MINIMAL")
    cp=round((1-high/max(total,1))*100)
    ms=[(str(total),"Total Systems","metric-accent-cyan"),(str(high),"High Risk","metric-accent-red"),(str(limited),"Limited Risk","metric-accent-orange"),(str(minimal),"Minimal Risk","metric-accent-green"),(f"{cp}%","Compliance Score","metric-accent-cyan")]
    cols=st.columns(5)
    for i,(v,l,ac) in enumerate(ms):
        with cols[i]: st.markdown(f'<div class="metric-card {ac}"><div class="metric-value">{v}</div><div class="metric-label">{l}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    cc1,cc2=st.columns(2)
    with cc1:
        st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)
        td=pd.DataFrame({"Tier":["High","Limited","Minimal"],"Count":[high,limited,minimal]})
        ft=px.pie(td,values="Count",names="Tier",color="Tier",color_discrete_map={"High":"#EF5350","Limited":"#FFA726","Minimal":"#66BB6A"},hole=0.5)
        ft.update_traces(textinfo="value+percent",textfont_size=13,textfont_color="#E3F2FD")
        ft.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Inter",color="#B0BEC5",size=12),legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5,font=dict(size=11)),margin=dict(l=20,r=20,t=20,b=40),height=320)
        st.plotly_chart(ft,use_container_width=True)
    with cc2:
        st.markdown('<div class="section-title">Risk by Department</div>', unsafe_allow_html=True)
        dr={}
        for a in agents:
            d=a["department"]
            if d not in dr: dr[d]=[]
            dr[d].append(a["classification"]["score"])
        dd=pd.DataFrame([{"Department":d,"Score":round(sum(s)/len(s),1)} for d,s in dr.items()]).sort_values("Score",ascending=True)
        fd=go.Figure(go.Bar(x=dd["Score"],y=dd["Department"],orientation="h",marker=dict(color=dd["Score"],colorscale=[[0,"#66BB6A"],[0.5,"#FFA726"],[1,"#EF5350"]],line=dict(width=0)),text=dd["Score"],textposition="outside",textfont=dict(color="#B0BEC5",size=11)))
        fd.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Inter",color="#B0BEC5",size=11),xaxis=dict(range=[0,110],gridcolor="rgba(255,255,255,0.05)",zeroline=False,showticklabels=False),yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),margin=dict(l=10,r=50,t=10,b=20),height=320,showlegend=False)
        st.plotly_chart(fd,use_container_width=True)

    st.markdown('<div class="section-title">Individual System Risk Scores</div>', unsafe_allow_html=True)
    sa=sorted(agents,key=lambda a:a["classification"]["score"],reverse=True)
    fa=go.Figure(go.Bar(x=[a["classification"]["score"] for a in sa],y=[a["name"] for a in sa],orientation="h",marker=dict(color=[a["classification"]["tier_color"] for a in sa],line=dict(width=0)),text=[a["classification"]["score"] for a in sa],textposition="outside",textfont=dict(color="#B0BEC5",size=11)))
    fa.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Inter",color="#B0BEC5",size=11),xaxis=dict(range=[0,115],gridcolor="rgba(255,255,255,0.05)",zeroline=False,title=""),yaxis=dict(gridcolor="rgba(255,255,255,0.05)",autorange="reversed"),margin=dict(l=10,r=50,t=10,b=20),height=max(280,len(agents)*42),showlegend=False)
    st.plotly_chart(fa,use_container_width=True)

with tab4:
    st.markdown('<div class="section-title">EU AI Act Compliance Gap Analysis</div>', unsafe_allow_html=True)
    hra=[a for a in st.session_state.agents if a["classification"]["tier"]=="HIGH"]
    if not hra:
        st.markdown('<div class="alert-box alert-success"><p style="color:#A5D6A7;font-size:0.9rem;margin:0">No high-risk AI systems detected. EU AI Act Articles 9-15 obligations do not currently apply.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-box alert-danger"><p style="color:#FFCDD2;font-size:0.9rem;margin:0"><strong>{len(hra)} high-risk system(s)</strong> require compliance with EU AI Act Articles 9-15, 17, 26-27 before August 2026.</p></div>', unsafe_allow_html=True)
        sn=st.selectbox("Select system for analysis:",[a["name"] for a in hra])
        sel=next(a for a in hra if a["name"]==sn)
        ex=st.multiselect("Measures already in place:",[(r["id"],f"{r['article']}: {r['title']}") for r in HIGH_RISK_REQUIREMENTS],format_func=lambda x:x[1],default=[])
        ei=[e[0] if isinstance(e,tuple) else e for e in ex]
        if st.button("Generate Gap Analysis",use_container_width=True):
            gaps=generate_gap_analysis(sn,sel["classification"],ei)
            met=sum(1 for g in gaps if g["status"]=="met"); tg=len(gaps); pct=round(met/max(tg,1)*100)
            bc_="#66BB6A" if pct>=70 else "#FFA726" if pct>=40 else "#EF5350"
            st.markdown(f'<div class="metric-card" style="margin:1rem 0"><div style="display:flex;justify-content:space-between;align-items:center"><div><p class="agent-name" style="font-size:1.1rem">{sn}</p><p class="agent-meta">{met} of {tg} requirements met</p></div><div class="metric-value" style="font-size:2.5rem;color:{bc_}">{pct}%</div></div><div class="compliance-bar-bg" style="margin-top:1rem"><div class="compliance-bar-fill" style="width:{pct}%;background:{bc_}"></div></div></div>', unsafe_allow_html=True)
            for g in gaps:
                gc="gap-met" if g["status"]=="met" else "gap-notmet"; sc_="#66BB6A" if g["status"]=="met" else "#EF5350"; st_="Met" if g["status"]=="met" else "Not Met"
                act_html=f"<p style='color:#EF9A9A;font-size:0.8rem;margin:0.3rem 0 0 0'>Action: {g['action']}</p>" if g["action"] else ""
                st.markdown(f'<div class="gap-item {gc}"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><p style="color:#E3F2FD;font-weight:600;font-size:0.9rem;margin:0">{g["article"]}: {g["title"]}</p><p style="color:#78909C;font-size:0.8rem;margin:0.25rem 0 0 0">{g["description"]}</p>{act_html}</div><span style="color:{sc_};font-size:0.8rem;font-weight:600;white-space:nowrap">{st_}</span></div></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Classification Reasons</div>', unsafe_allow_html=True)
            for r in sel["classification"]["reasons"]:
                st.markdown(f'<div style="padding:0.4rem 0;border-bottom:1px solid #1E3A5F"><p style="color:#FFCC80;font-size:0.85rem;margin:0">{r}</p></div>', unsafe_allow_html=True)

st.markdown('<br><div style="text-align:center;padding:1.5rem 0;border-top:1px solid #1E3A5F"><p style="color:#546E7A;font-size:0.75rem;margin:0;letter-spacing:0.3px">NexaGovern  |  AI Agent Visibility and Governance  |  Frankfurt School MIM Entrepreneurship 2026</p></div>', unsafe_allow_html=True)