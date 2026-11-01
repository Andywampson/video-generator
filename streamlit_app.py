import os
from datetime import date

import streamlit as st

BOSS_NAME = "dr.dryy"
BOSS_SECRET_KEY = os.getenv("BOSS_SECRET_KEY", "")
STRIPE_CHECKOUT_URL = os.getenv("STRIPE_CHECKOUT_URL", "")
FREE_GENERATIONS_PER_DAY = 3

st.set_page_config(page_title=f"{BOSS_NAME}'s Video Studio", layout="wide")

if "is_premium" not in st.session_state:
    st.session_state.is_premium = False
if st.session_state.get("generation_date") != date.today():
    st.session_state.generation_date = date.today()
    st.session_state.daily_free_generations = FREE_GENERATIONS_PER_DAY
if "system_status" not in st.session_state:
    st.session_state.system_status = "ONLINE"

if st.session_state.system_status == "ONLINE":
    st.markdown(
        f"""
        <div style="background:#111;padding:15px;border-radius:8px;border:2px solid #d5ad42;text-align:center;margin-bottom:20px;">
            <h3 style="color:#f2cc60;margin:0;font-family:monospace;">
                SYSTEM STATUS: OPERATIONAL
            </h3>
            <p style="color:#fff;margin:5px 0 0;font-size:14px;">
                Prototype session managed by <strong>{BOSS_NAME}</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.error(f"This session has been paused by {BOSS_NAME.upper()}.")
    with st.sidebar:
        st.subheader("Boss Emergency Core")
        if not BOSS_SECRET_KEY:
            st.caption("Set BOSS_SECRET_KEY to enable administrative controls.")
        else:
            boss_key = st.text_input("Boss key", type="password", key="restart_boss_key")
            if st.button("Restart this session"):
                if boss_key == BOSS_SECRET_KEY:
                    st.session_state.system_status = "ONLINE"
                    st.rerun()
                st.error("Invalid boss key.")
    st.stop()

with st.sidebar:
    st.header("Your Account")
    if st.session_state.is_premium:
        st.success("Premium access unlocked for this session")
    else:
        st.warning("Free tier")
        st.write(f"Remaining free demos this session: **{st.session_state.daily_free_generations}**")
        st.markdown("### Premium Pass: $3.00")
        if STRIPE_CHECKOUT_URL.startswith("https://"):
            st.link_button("Unlock with Stripe", STRIPE_CHECKOUT_URL, use_container_width=True)
        else:
            st.caption("Configure STRIPE_CHECKOUT_URL with your Stripe Payment Link to enable checkout.")

    st.markdown("---")
    st.subheader("Boss Command Core")
    if not BOSS_SECRET_KEY:
        st.caption("Set BOSS_SECRET_KEY to enable administrative controls.")
    else:
        boss_input = st.text_input("Verify boss identity", type="password", key="boss_identity")
        if boss_input == BOSS_SECRET_KEY:
            st.success(f"Identity verified. Standing by, {BOSS_NAME}.")
            if st.button("Pause this session"):
                st.session_state.system_status = "TERMINATED"
                st.rerun()
            if st.button("Grant premium for this session"):
                st.session_state.is_premium = True
                st.rerun()

st.title(f"{BOSS_NAME.upper()}'s $3 AI Video Generator")
st.caption("Prototype interface. Video generation and payment verification are not connected.")

main_col, ad_col = st.columns((3, 1))

with main_col:
    prompt = st.text_input("Describe the video you want to create:")
    if st.button("Generate Video", type="primary"):
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
        elif not st.session_state.is_premium and st.session_state.daily_free_generations <= 0:
            st.error(f"No free demos remain. Configure checkout or contact {BOSS_NAME}.")
        else:
            if not st.session_state.is_premium:
                st.info("Sponsored advertisement placeholder")
                st.session_state.daily_free_generations -= 1
            st.warning("No video was generated. Connect a video-generation backend to enable this feature.")

with ad_col:
    if not st.session_state.is_premium:
        st.subheader("Sponsored Links")
        st.info("Advertisement placement")
