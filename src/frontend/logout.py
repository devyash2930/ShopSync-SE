# logout.py

import streamlit as st

flag =True

def callfunc():
    flag=False
    return flag

def fetch_title():
    return "Logout"

def fetch_state():
    return callfunc()

def app():
    # Set the logout status
    st.session_state.logged_in = False
    callfunc()
    st.session_state.user_email = None
    st.session_state.redirect = None

    # Display a logout message
    st.success("Logged out successfully!")

    # Provide a link to the login page
    # st.markdown("[Go to Login Page](#)")

    # Optionally, you can redirect to the account page directly
    if st.button("Login Again"):
        st.session_state['logged_in'] = False
        callfunc()
        st.rerun()  # Reload the app to go back to the Account page
