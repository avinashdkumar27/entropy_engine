import streamlit as st
import matplotlib.pyplot as plt
from core.strength_logic import analyze_password
from core.attack_models import ATTACK_MODELS

st.set_page_config(page_title="Entropy Engine", page_icon="🧠", layout="centered")

st.title("🧠 Entropy Engine")
st.subheader("Advanced Password Intelligence System")

# Form
password = st.text_input("Enter Password", type="password")
attack_model = st.selectbox("Select Attack Model", list(ATTACK_MODELS.keys()))
analyze_btn = st.button("Analyze Password")

if analyze_btn or password:
    if not password:
        st.warning("Please enter a password.")
    else:
        with st.spinner("Analyzing..."):
            res = analyze_password(password, attack_model)
            
        # Display meter
        st.markdown(f"### Strength: <span style='color:{res['meter_color']}'>{res['meter_label']}</span>", unsafe_allow_html=True)
        st.progress((res['final_score'] + 1) / 5)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Entropy", f"{res['entropy']} bits")
        col2.metric("zxcvbn Score", f"{res['zxcvbn_score']} / 4")
        col3.metric("Combinations", f"{res['combinations']:.1e}")
        
        st.metric(f"Time to Crack ({attack_model})", res['crack_time_display'])
        
        if res['warnings']:
            st.warning(res['warnings'])
        
        if res['suggestions']:
            with st.expander("Suggestions to improve"):
                for s in res['suggestions']:
                    st.write(f"- {s}")
        
        # Breach Status
        if res['pwned_count'] > 0:
            st.error(f"⚠️ FOUND IN {res['pwned_count']} KNOWN DATA BREACHES! Change this password immediately.")
        else:
            st.success("✅ Not found in known data breaches.")
            
        # Log Scale Graph
        st.markdown("---")
        st.subheader("Attack Model Simulation (Log Scale)")
        
        crack_times = res["crack_times_all"]
        models = list(crack_times.keys())
        times = [max(1e-5, crack_times[m]) for m in models]
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(models, times, color=['#FF4C4C', '#FFA500', '#FFD700', '#32CD32'])
        ax.set_yscale("log")
        ax.set_ylabel("Time to Crack (Seconds)")
        ax.set_xlabel("Attack Models")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        st.pyplot(fig)
