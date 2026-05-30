import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True
    
    st.markdown(
        """
        <div class="login-shell">
            <div class="login-card">
                <div class="login-badge">AI Form Coach</div>
                <h1>Train smarter with live movement feedback.</h1>
                <p>
                    Enter a unique name to start a private workout session with rep tracking,
                    posture cues, and a voice coach that reacts in real time.
                </p>
                <p>
                    The experience is designed like a modern training console: focused, fast,
                    and built around your next set.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Name (unique)", placeholder="unique name e.g. princekhunt")
        submit_button = st.form_submit_button("Start Session", width="stretch")

    if submit_button:
        if not username:
            st.error("Name cannot be empty.")
            return False
        
        user = get_or_create_user(username)
    
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]

        st.rerun()

    return False