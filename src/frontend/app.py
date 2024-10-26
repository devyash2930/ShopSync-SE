import streamlit as st
from streamlit_option_menu import option_menu
import account  # Ensure this module handles user authentication
import slash_user_interface  # Your home interface

class MultiApp:
    def __init__(self):
        self.apps = []
    
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    
    def run(self):
        # Determine the default selected app based on login status
        default_index = 0 if not st.session_state.get('logged_in') else 1

        with st.sidebar:
            app = option_menu(
                menu_title='ShopSync',
                options=['Account', 'Home', 'Favourites', 'Logout'],
                icons=['person-circle', 'house-fill', 'star-fill', 'box-arrow-right'],
                menu_icon='chat-text-fill',
                default_index=default_index,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21" if st.session_state.get('logged_in') else "#02ab21"},
                }
            )
        
        # Call the corresponding app function based on the selected option
        if app == "Account":
            account.app()
        
        elif app == "Home":
            if st.session_state.get('logged_in'):
                slash_user_interface.app()
            else:
                st.warning("You need to log in to access the Home page.")
        
        elif app == "Logout":
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.redirect = None
            st.success("Logged out successfully.")
            st.rerun()

# To run the app
if __name__ == '__main__':
    app = MultiApp()
    app.add_app("Account", account.app)
    app.add_app("Home", slash_user_interface.app)
    app.run()
