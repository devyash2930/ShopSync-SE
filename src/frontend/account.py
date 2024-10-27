import streamlit as st
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import re

# Set the theme (optional, replace with your preferred theme)
st.set_page_config(page_title="ShopSync", layout="centered", initial_sidebar_state="expanded")

# Initialize Firebase Admin SDK (only do this once in your app)
if not firebase_admin._apps:
    cred = credentials.Certificate('shopsync-se-firebase-adminsdk-nkzuw-ca6838f54f.json')
    firebase_admin.initialize_app(cred)

# Initialize session state variables
# if 'theme' not in st.session_state:
# #     st.session_state.theme = 'light'  # Default theme
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'user_email' not in st.session_state:
#     st.session_state.user_email = None

# def apply_theme():
#     # Function to apply the theme
#     if st.session_state.theme == 'dark':
#         st.markdown(
#             """
#             <style>
#             .main {background-color: #282828; color: white;}
#             </style>
#             """,
#             unsafe_allow_html=True
#         )

def is_valid_email(email):
    # Basic regex for validating an email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    # apply_theme()  # Apply the theme

    # Main application logic
    if st.session_state.logged_in:
        st.title('Welcome to :violet[shopsync]')
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
                    try:
                        # Attempting to sign in
                        user = auth.get_user_by_email(email)  # Check if user exists

                        # Simulate password check
                        if not password:  # Simulate a check for an empty password
                            raise ValueError('wrong-password')

                        # If user exists and password is assumed correct, log the user in
                        st.session_state.logged_in = True
                        st.session_state.user_email = user.email  # Store user email
                        st.success('Logged in successfully!')
                        st.rerun()  # Rerun the app to reflect login state

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
