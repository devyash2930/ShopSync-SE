import streamlit as st
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import re

# Initialize Firebase Admin SDK (only do this once in your app)
if not firebase_admin._apps:
    cred = credentials.Certificate('shopsync-se-firebase-adminsdk-nkzuw-e871ea65d4.json')
    firebase_admin.initialize_app(cred)

def is_valid_email(email):
    # Basic regex for validating an email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def app():
    st.title('Welcome to :violet[shopsync]')

    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

    if choice == 'Login':
        email = st.text_input('Email Address', key='email')
        password = st.text_input('Password', type='password', key='password')

        if st.button('Login'):
            if not is_valid_email(email):
                st.warning('Invalid email format. Please enter a valid email address.')
            else:
                try:
                    # Attempting to sign in
                    user = auth.get_user_by_email(email)  # Check if user exists

                    # Simulate password check by assuming the user exists
                    # Note: You cannot check the password directly with Firebase Admin SDK
                    # In a real app, you should use the Firebase Client SDK for password validation

                    # Simulating password error by raising an error if the password is incorrect
                    if not password:  # Simulate a check for an empty password
                        raise ValueError('wrong-password')
                    
                    # If user exists and password is assumed correct, log the user in
                    st.session_state.logged_in = True
                    st.session_state.user_email = user.email  # Store user email
                    st.success('Logged in successfully!')
                    st.session_state.redirect = 'Home'  # Set redirect state
                    st.rerun()  # Rerun the app to redirect

                except auth.UserNotFoundError:
                    st.warning('No account found with this email address.')
                except ValueError as e:
                    if str(e) == 'wrong-password':
                        st.warning('Incorrect password. Please try again.')
                    else:
                        st.warning(f'Login failed: {str(e)}')
                except Exception as e:
                    st.warning(f'Login failed: {str(e)}')

    else:
        email = st.text_input('Email Address', key='email_signup')
        password = st.text_input('Password', type='password', key='password_signup')
        username = st.text_input('Enter your unique username')

        if st.button('Create account'):
            try:
                user = auth.create_user(email=email, password=password, uid=username)
                st.success('Account created successfully')
                st.markdown('Please log in using this email and password')
            except Exception as e:
                st.warning(f'Account creation failed: {str(e)}')

# Call the app function
if __name__ == '__main__':
    app()
