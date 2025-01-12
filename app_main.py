import streamlit as st
from token_validator import StreamlitJWTValidator
import os
from typing import Optional, Dict

class StreamlitAuth:
    def __init__(self):
        self.validator = StreamlitJWTValidator()
        self._initialize_session_state()

    def _initialize_session_state(self):
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "user" not in st.session_state:
            st.session_state.user = None

    def check_authentication(self) -> bool:
        # Check URL params first
        if not st.session_state.authenticated:
            user_info = self.validator.check_token_in_params()
            if user_info:
                return True

        return st.session_state.authenticated

    def logout(self):
        self.validator.logout()
        st.rerun()

def main():
    st.set_page_config(page_title="Medical Portal", layout="wide")
    auth = StreamlitAuth()

    # Authentication check
    if not auth.check_authentication():
        st.warning("Please log in through the main portal")
        st.stop()
        return

    # Main application UI
    st.title("Medical Portal")
    
    # User info display
    user = st.session_state.user
    st.sidebar.write(f"Welcome, {user['name']}")
    if st.sidebar.button("Logout"):
        auth.logout()

    # Protected content
    tabs = st.tabs(["Profile", "Records", "Appointments"])
    with tabs[0]:
        st.header("Profile")
        st.write(f"Email: {user['email']}")
    
    with tabs[1]:
        st.header("Medical Records")
        # Add medical records content
    
    with tabs[2]:
        st.header("Appointments")
        # Add appointments content

if __name__ == "__main__":
    main()
