import streamlit as st
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import requests
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Firebase Web API Key from environment variable
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")  # Set your key here if not in environment

# Set the theme (optional, replace with your preferred theme)
st.set_page_config(page_title="ShopSync", layout="centered", initial_sidebar_state="expanded")

# Initialize Firebase Admin SDK (only do this once in your app)
if not firebase_admin._apps:
    cred = credentials.Certificate('shopsync-se-firebase-adminsdk-nkzuw-e871ea65d4.json')
    firebase_admin.initialize_app(cred)

def is_valid_email(email):
    # Basic regex for validating an email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def verify_password(email, password):
    """Verify email and password using Firebase REST API."""
    try:
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}",
            json={"email": email, "password": password, "returnSecureToken": True}
        )
        response_data = response.json()
        # st.write("Response Data:", response_data)  # Log the response for debugging

        if "idToken" in response_data:
            return True  # Successful login
        elif "error" in response_data:
            error_message = response_data["error"]["message"]
            if error_message == "EMAIL_NOT_FOUND":
                st.warning("No account found with this email address.")
            elif error_message == "INVALID_PASSWORD":
                st.warning("Incorrect password. Please try again.")
            else:
                st.warning(f"Login failed: {error_message}")
        return False
    except Exception as e:
        st.warning(f"Login failed: {str(e)}")
        return False

def app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

    # Main application logic
    if st.session_state.logged_in:
        st.title('Welcome to :violet[ShopSync]')
        st.write('You are logged in as:', st.session_state.user_email)
        st.button("Logout", on_click=logout)  # Add logout button
    else:
        # Handle login and signup
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

        if choice == 'Login':
            email = st.text_input('Email Address', key='email')
            password = st.text_input('Password', type='password', key='password')

            if st.button('Login'):
                if not email and not password:
                    st.warning('Please enter the credentials.')
                elif not email:
                    st.warning('Please enter the email.')
                elif not is_valid_email(email):
                    st.warning('Invalid email format. Please enter a valid email address.')
                elif not password:
                    st.warning('Please enter the password.')
                else:
                    if verify_password(email, password):
                        # If login successful, update session state
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success('Logged in successfully!')
                        st.rerun()  # Rerun the app to reflect login state

        else:
            email = st.text_input('Email Address', key='email_signup')
            password = st.text_input('Password', type='password', key='password_signup')
            username = st.text_input('Enter your unique username')

            if st.button('Create account'):
                missing_fields = []

                if not email:
                    missing_fields.append('Email Address')
                elif not is_valid_email(email):
                    st.warning('Invalid email format. Please enter a valid email address.')
                
                if not password:
                    missing_fields.append('Password')
                if not username:
                    missing_fields.append('Unique Username')

                if len(missing_fields) == 3:
                    st.warning('Please enter the credentials.')
                elif missing_fields:
                    st.warning(f'Please fill the following field(s): {", ".join(missing_fields)}')
                else:
                    try:
                        user = auth.create_user(email=email, password=password, uid=username)
                        st.success('Account created successfully')
                        st.markdown('Please log in using this email and password')
                    except auth.EmailAlreadyExistsError:
                        st.warning('The email is already registered. Please use another email or log in.')
                    except Exception as e:
                        st.warning(f'Account creation failed: {str(e)}')

def logout():
    # Clear session state on logout
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.success("You have been logged out.")
    st.rerun()  # Rerun the app to reflect logout state

# Call the app function
if __name__ == '__main__':
    app()
