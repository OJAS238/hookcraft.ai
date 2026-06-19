import streamlit as st
import time
import json
import plotly.graph_objects as go
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="HookCraft AI Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Premium Dark UI CSS Injection
st.markdown("""
<style>
    .stApp { 
        background: radial-gradient(circle at 90% 10%, rgba(255, 0, 127, 0.05), transparent 40%),
                    radial-gradient(circle at 10% 90%, rgba(0, 223, 216, 0.05), transparent 40%),
                    #07090e; 
        color: #ffffff; 
    }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .hero-banner {
        background: linear-gradient(135deg, rgba(13, 17, 23, 0.8) 0%, rgba(7, 9, 14, 0.9) 100%);
        border: 1px solid rgba(0, 223, 216, 0.2);
        border-radius: 16px;
        padding: 35px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .stTextArea textarea { 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        background-color: #0d1117 !important; 
        color: #e2e8f0 !important; 
        border-radius: 12px !important;
        font-size: 15px !important;
        padding: 15px !important;
    }
    .stTextArea textarea:focus { 
        border: 1px solid #00dfd8 !important; 
        box-shadow: 0 0 15px rgba(0, 223, 216, 0.15) !important;
    }
    
    div.stButton > button { 
        background: linear-gradient(90deg, #ff007f, #d00067) !important; 
        color: #ffffff !important; 
        font-weight: 700 !important; 
        border-radius: 10px !important; 
        border: none !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover { 
        background: linear-gradient(90deg, #00dfd8, #00b3b0) !important; 
        color: #07090e !important;
        transform: translateY(-2px);
    }
    
    .saas-card {
        background: #0d1117;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .failure-card {
        background: rgba(255, 0, 127, 0.03);
        border: 1px solid rgba(255, 0, 127, 0.2);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .empty-state-slot {
        border: 2px dashed rgba(0, 223, 216, 0.15);
        padding: 50px 30px;
        text-align: center;
        border-radius: 16px;
        background: rgba(13, 17, 23, 0.4);
        color: #718096;
    }
    
    .phrase-pill {
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        margin: 5px 5px 5px 0px;
    }
    .pill-strong { background: rgba(0, 223, 216, 0.1); border: 1px solid #00dfd8; color: #00dfd8; }
    .pill-medium { background: rgba(255, 171, 0, 0.1); border: 1px solid #ffab00; color: #ffab00; }
    .pill-weak { background: rgba(255, 0, 127, 0.1); border: 1px solid #ff007f; color: #ff007f; }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration for API Key Input
with st.sidebar:
    st.markdown("### 🔑 Authentication")
    user_api_key = st.text_input(
        "Enter Groq API Key:",
        type="password",
        placeholder="gsk_...",
        help="Get your API key from console.groq.com"
    )
    if user_api_key:
        st.success("API key stored securely!")
    else:
        st.warning("Please enter your API key to unlock.")

# Session State Control
if "current_results" not in st.session_state:
    st.session_state.current_results = None
if "current_execution_time" not in st.session_state:
    st.session_state.current_execution_time = None
if "pipeline_executed" not in st.session_state:
    st.session_state.pipeline_executed = False

def clear_old_results():
    st.session_state.current_results = None
    st.session_state.current_execution_time = None
    st.session_state.pipeline_executed = False

# Hero Presentation Banner
st.markdown("""
<div class="hero-banner">
    <span style="background: rgba(0, 223, 216, 0.1); color: #00dfd8; padding: 6px 16px; border-radius: 50px; font-size: 12px; font-weight: bold; letter-spacing: 1px;">PRODUCTION LABS v2.5</span>
    <h1 style="margin: 15px 0 5px 0; font-size: 42px; letter-spacing: -1px; background: linear-gradient(90deg, #ffffff, #a0aec0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Introducing HookCraft AI</h1>
    <p style="color: #00dfd8; font-size: 16px; max-width: 600px; margin: 0 auto; font-family: 'Inter';">Predictive retention modeling framework. Optimize scripts via Llama-3.3-70B before cameras roll.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 📋 Content Workspace")
    user_input = st.text_area(
        "Script Draft Input Area:", 
        placeholder="Type or paste your opening video hook here...",
        height=180,
        label_visibility="collapsed",
        key="workspace_input",
        on_change=clear_old_results
    )
        
    input_is_invalid = len(user_input.strip()) < 10 or not user_api_key
    
    btn_cols = st.columns([3, 1.2])
    with btn_cols[0]:
        submit_btn = st.button(
            "🧠 Predict Audience Retention", 
            disabled=input_is_invalid, 
            use_container_width=True
        )
    with btn_cols[1]:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.clear()
            st.rerun()
            
    if not user_api_key:
        st.error("⚠️ *Authentication missing. Provide your Groq API Key in the sidebar.*")
    elif input_is_invalid:
        st.caption("🔒 *Console locked. Awaiting draft script values to execute pipeline.*")

# Real-time Cloud Pipeline Execution
if submit_btn and not input_is_invalid:
    start_time = time.time()
    with st.spinner("Calling Groq Network Inferences..."):
        try:
            client = Groq(api_key=user_api_key)
            
            system_instructions = (
                "You are an AI video retention analytics engine. Analyze the video script hook provided by the user. "
                "You MUST output exactly a JSON object matching this structure. Do not output anything else. "
                "No introductory conversation, no markdown formatting blocks. Just raw valid JSON string.\n"
                "Structure requirements:\n"
                "{\n"
                '  "score": integer_value_0_to_100,\n'
                '  "why_it_fails": "Detailed paragraph explaining the exact psychological flaws in the original hook, why users will swipe away, and what structural parts are too generic or lack tension.",\n'
                '  "retention": {"0-3s Window": "XX%", "3-10s Window": "XX%", "10-30s Window": "XX%"},\n'
                '  "radar_categories": ["Curiosity", "Fear of Missing Out", "Authority", "Novelty", "Trust"],\n'
                '  "radar_values": [5 integers between 0 and 100 corresponding to the categories above],\n'
                '  "chunks": [\n'
                '     {"text": "Short phrase from hook", "strength": "strong" or "medium" or "weak", "explanation": "Brief token impact analysis"}\n'
                '  ],\n'
                '  "variations": [\n'
                '     {"title": "The Curiosity Gap Variation", "text": "A viral re-engineered version leveraging missing critical details to force a watch till the end."},\n'
                '     {"title": "The FOMO / Urgency Variation", "text": "A viral re-engineered version creating intense artificial time-scarcity or hidden competition."},\n'
                '     {"title": "The Pattern Interruption Variation", "text": "A viral re-engineered version that completely subverts common viewer expectations or says something jarring."}\n'
                "  ]\n"
                "}"
            )

            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            st.session_state.current_results = json.loads(chat_completion.choices[0].message.content)
            st.session_state.pipeline_executed = True
            
        except Exception as api_err:
            st.error(f"Groq API Error: {str(api_err)}")
            st.session_state.pipeline_executed = False
            
    st.session_state.current_execution_time = time.time() - start_time

# Live View Render
with col2:
    st.markdown("### 🖥️ Deep Metric Analytics")
    
    if st.session_state.pipeline_executed and st.session_state.current_results:
        res = st.session_state.current_results
        st.markdown(f"⏱️ *Processing complete in **{st.session_state.current_execution_time:.2f}s** via Groq Speculative Engine.*")
        
        # Upper KPI Metrics block
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        m_col1, m_col2 = st.columns([1, 2])
        with m_col1:
            st.markdown("<p style='color: #718096; font-size: 11px; font-weight: bold; margin:0;'>HOOK STRENGTH</p>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: #00dfd8; font-size: 56px; margin: 5px 0 0 0; line-height:1;'>{res.get('score', 0)}<span style='font-size:18px; color:#4a5568;'>/100</span></h1>", unsafe_allow_html=True)
        with m_col2:
            st.markdown("<p style='color: #718096; font-size: 11px; font-weight: bold; margin:0 0 5px 0;'>RETENTION RISK TIMELINE PREDICTION</p>", unsafe_allow_html=True)
            ret_data = " &nbsp;&nbsp;|&nbsp;&nbsp; ".join([f"**{k}:** <span style='color:#00dfd8;'>{v}</span>" for k, v in res.get('retention', {}).items()])
            st.markdown(f"<p style='margin:5px 0 0 0; font-size:15px;'>{ret_data}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Why It Might Fail - Deep-Dive Block
        if "why_it_fails" in res:
            st.markdown('<div class="failure-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='color: #ff007f; margin:0 0 10px 0;'>❌ Why it might fail:</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #e2e8f0; font-size:14px; line-height:1.6; margin:0;'>{res['why_it_fails']}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Dynamic Visualizations Layer
        vis_col1, vis_col2 = st.columns([1.1, 1])
        with vis_col1:
            st.markdown('<div class="saas-card" style="padding: 20px 15px 0px 15px;">', unsafe_allow_html=True)
            st.caption("PSYCHOLOGY PROFILE DATA")
            
            fig = go.Figure(data=go.Scatterpolar(
                r=res.get('radar_values', [50, 50, 50, 50, 50]),
                theta=res.get('radar_categories', ["Curiosity", "Fear of Missing Out", "Authority", "Novelty", "Trust"]),
                fill='toself',
                fillcolor='rgba(255, 0, 127, 0.15)',
                line=dict(color='#ff007f', width=2)
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=False, range=[0, 100]),
                    bgcolor='rgba(0,0,0,0)',
                    angularaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)')
                ),
                showlegend=False,
                margin=dict(l=35, r=35, t=30, b=30),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e0', size=11)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with vis_col2:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.caption("COGNITIVE CHUNK ANALYSIS")
            st.write("")
            
            for chunk in res.get('chunks', []):
                pill_color = f"pill-{chunk.get('strength', 'medium').lower()}"
                st.markdown(f'<span class="phrase-pill {pill_color}">"{chunk.get("text")}"</span><br><small style="color:#718096;">→ {chunk.get("explanation")}</small>', unsafe_allow_html=True)
                st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Output Alternatives Display Card
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #00dfd8; margin-bottom: 15px;'>🧠 The Psychological Remap (3 Viral Variations):</h4>", unsafe_allow_html=True)
        for idx, var in enumerate(res.get('variations', []), 1):
            st.markdown(f"**{idx}. {var.get('title')}**")
            st.markdown(f"<p style='color: #cbd5e0; background: rgba(255,255,255,0.015); padding: 12px; border-left: 3px solid #ff007f; border-radius: 6px; font-style: italic; margin-top:5px; margin-bottom:15px;'>\"{var.get('text')}\"</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # Standing by State Dashboard Layer
        st.markdown('<div class="empty-state-slot">', unsafe_allow_html=True)
        st.markdown("""
            <div style="font-size: 40px; margin-bottom: 15px;">⚡</div>
            <h4 style="color: #ffffff; margin: 0 0 10px 0; font-size: 18px;">Analytics Console Standing By</h4>
            <p style="color: #718096; font-size: 14px; max-width: 380px; margin: 0 auto; line-height: 1.5; margin-bottom: 30px;">
                Input your hook in the workspace panel to run real-time predictive retention arrays, phrase chunk coloring, and radar chart telemetry loops.
            </p>
        """, unsafe_allow_html=True)
        
        preview_cols = st.columns(3)
        with preview_cols[0]:
            st.metric(label="Target Latency", value="< 1.00s")
        with preview_cols[1]:
            st.metric(label="Model Context", value="Llama-3.3")
        with preview_cols[2]:
            st.metric(label="Inference Route", value="Groq Cloud")
            
        st.markdown('</div>', unsafe_allow_html=True)
