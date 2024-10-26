import streamlit as st
import firebase_admin

from firebase_admin import credentials
from firebase_admin import auth

# cred = credentials.Certificate('frontend/shopsync-se-firebase-adminsdk-nkzuw-ca6838f54f.json')
cred = credentials.Certificate('shopsync-se-firebase-adminsdk-nkzuw-e871ea65d4.json')

# firebase_admin.initialize_app(cred)

def app():
    st.title('Welcome to :violet[shopsync]')

    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

    def f():
        try:
            user = auth.get_user_by_email(email)
            # st.success('Account logged in successfully')
            # print(user.uid)
        
        except:
            st.warning('Login failed')

    if choice=='Login':

        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        st.button('Login', on_click=f)

    else:
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        username = st.text_input('Enter your unique username')

        if st.button('Create account'):
            user = auth.create_user(email = email, password = password, uid=username)

            st.success('Account created successfully')
            st.markdown('Please login using this email and password')