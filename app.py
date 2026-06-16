import streamlit as st
from groq import Groq

# 1. Configure the AI Brain
GROQ_API_KEY = st.text_input("🔑 Enter Groq API Key:", type="password")
client = Groq(api_key=GROQ_API_KEY)

# 2. Force Wide-Screen Layout to use all screen space
st.set_page_config(page_title="HookCraft AI", page_icon="🧠", layout="wide")

# --- CUSTOM CSS INJECTION FOR AN ELITE SaaS DASHBOARD ---
st.markdown("""
    <style>
        /* Dark Cyberpunk Theme Background */
        .stApp {
            background: linear-gradient(135deg, #07090e 0%, #0f131a 100%);
            color: #f0f2f6;
            font-family: 'Inter', sans-serif;
        }
        
        /* Left/Right Container Column Adjustments */
        [data-testid="stHorizontalBlock"] {
            gap: 2rem !important;
        }
        
        /* Header Title Styling */
        .main-title {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #ff007f, #7928ca, #00dfd8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0rem;
            letter-spacing: -1px;
        }
        .sub-title {
            font-size: 1.1rem;
            color: #718096;
            margin-bottom: 2rem;
        }

        /* Input Panel Wrapper Card */
        .input-panel {
            background: #121620;
            border: 1px solid #232936;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }

        /* TEXT AREA TYPING VISIBILITY FIX */
        .stTextArea textarea {
            background-color: #1a202c !important;
            color: #ffffff !important;
            font-size: 1.1rem !important;
            border: 2px solid #2d3748 !important;
            border-radius: 12px !important;
            padding: 15px !important;
        }
        .stTextArea textarea:focus {
            border-color: #ff007f !important;
            box-shadow: 0 0 15px rgba(255, 0, 127, 0.2) !important;
        }
        
        /* FIX FOR THE UNSEEN "CTRL + ENTER" HINT TEXT */
        .stTextArea label p, 
        .stTextArea [data-testid="stWidgetInstructions"] small,
        .stTextArea div div div div div {
            color: #ff007f !important; /* High-visibility Neon Pink */
            font-weight: 800 !important;
            font-size: 0.95rem !important;
        }
        
        [data-testid="stWidgetInstructions"] {
            color: #ff007f !important;
            font-weight: 800 !important;
        }
        
        /* Neon Action Button */
        .stButton>button {
            width: 100%;
            background: linear-gradient(90deg, #ff007f 0%, #7928ca 100%) !important;
            color: white !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
            padding: 14px 20px !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 20px rgba(255, 0, 127, 0.4);
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(255, 0, 127, 0.6);
        }
        
        /* Premium Output Glassmorphism Card */
        .output-card {
            background: rgba(22, 28, 42, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-left: 6px solid #00dfd8;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            font-size: 1.15rem;
            line-height: 1.7;
        }
        
        /* Beautiful Glowing Placeholder card layout */
        .placeholder-card {
            border: 2px dashed #00dfd8 !important; /* Radiant Neon Teal Border */
            background: rgba(0, 223, 216, 0.02) !important;
            border-radius: 16px;
            padding: 5rem 2rem;
            text-align: center;
            color: #ffffff !important;
            font-size: 1.2rem;
            box-shadow: 0 0 20px rgba(0, 223, 216, 0.05);
        }
    </style>
""", unsafe_allow_html=True)

# 3. Premium Main Header
st.markdown('<h1 class="main-title">🧠 HookCraft AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Pre-Production Cognitive Mapping & Script Optimization Engine</p>', unsafe_allow_html=True)

# 4. SPLIT TWO-COLUMN SaaS LAYOUT
left_column, right_column = st.columns([2, 3])

# --- LEFT SIDE: INPUT & CONTROLS ---
with left_column:
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Engine Parameters")
    
    platform = st.selectbox("🎯 Target Platform", ["TikTok Reels / Shorts (9:16)", "YouTube Long-form (16:9)", "LinkedIn Video"])
    tone = st.select_slider("🔥 Content Persona Intensity", options=["Casual", "Intriguing", "Aggressive / Viral"])
    
    st.markdown("---")
    
    user_hook = st.text_area("⚡ Paste Your Video Hook Script Here:", 
                             placeholder="e.g., 'In this video, I will show you how to earn money fast...'",
                             height=180)
    
    st.write("")
    analyze_button = st.button("Run Psychology Mapping 🔥")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT SIDE: RESULTS & ANALYTICS ---
with right_column:
    if analyze_button:
        if not GROQ_API_KEY:
            st.error("Please enter your Groq API Key in the entry box at the top left!")
        elif user_hook.strip() == "":
            st.warning("Please input a script line first!")
        else:
            with st.spinner("Decoding linguistic framework evaluation..."):
                try:
                    psychology_prompt = f"""
                    You are a Viral Video Psychologist and Short-Form Retention Expert optimizing for a {tone} tone on {platform}. 
                    Analyze the following video hook: "{user_hook}"
                    
                    Provide your response in the following neat format:
                    
                    ### 📊 Hook Score: [Give a score out of 100]
                    
                    ### ❌ Why it might fail:
                    [Provide a blunt, 2-sentence psychological reason why people will swipe away]
                    
                    ### 🧠 The Psychological Remap (3 Viral Variations):
                    1. **The Curiosity Gap Variation:** [Rewrite the hook to hide key information, forcing them to watch]
                    2. **The FOMO / Urgency Variation:** [Rewrite it to make them feel like they are missing out on a secret]
                    3. **The Pattern Interruption Variation:** [Start with a shocking, contrarian statement]
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": psychology_prompt}],
                    )
                    
                    metrics_col1, metrics_col2 = st.columns(2)
                    metrics_col1.metric("💡 Core Model", "Llama-3.3-70b")
                    metrics_col2.metric("⚡ Status", "Optimization Synced")
                    
                    st.markdown(f'<div class="output-card">{completion.choices[0].message.content}</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred. Details: {e}")
    else:
        st.markdown("""
            <div class="placeholder-card">
                🤖 <br><br>
                <b>Awaiting Creator Script Input</b><br>
                <span style="font-size:0.9rem; color:#a0aec0;">
                    Fill out the configuration parameters on the left and click "Run Psychology Mapping" 
                    or press <b style="color:#ff007f;">Ctrl + Enter</b> to generate your advanced analytics dashboard.
                </span>
            </div>
        """, unsafe_allow_html=True)