import streamlit as st
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

# Initialize Firebase Admin SDK (only do this once in your app)
if not firebase_admin._apps:
    cred = credentials.Certificate('shopsync-se-firebase-adminsdk-nkzuw-e871ea65d4.json')
    firebase_admin.initialize_app(cred)

def app():
    st.title('Welcome to :violet[shopsync]')

    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

    if choice == 'Login':
        email = st.text_input('Email Address', key='email')
        password = st.text_input('Password', type='password', key='password')

        if st.button('Login'):
            try:
                # Sign in with email and password using Firebase Auth
                user = auth.get_user_by_email(email)
                # Firebase doesn't allow checking passwords directly, so we will simulate a check here
                # In a real app, you would use Firebase Auth client-side to handle this
                # Here you might want to store user info in session state for later use
                st.session_state.logged_in = True
                st.session_state.user_email = user.email  # Store user email
                st.success('Logged in successfully!')
                st.session_state.redirect = 'Home'  # Set redirect state
                st.rerun()  # Rerun the app to redirect

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
