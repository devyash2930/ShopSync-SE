import streamlit as st
from streamlit_option_menu import option_menu
import account  # Ensure this module handles user authentication
# import src.frontend.slash_user_interface as slash_user_interface # Your home interface
import slash_user_interface as slash_user_interface
import favourites
import logout  # Import the logout module
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='streamlit')

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
                menu_icon='shop',
                default_index=default_index,
                styles={
                    "container": {"padding": "5!important", "background-color": 'white'},
                    "icon": {"color": "black", "font-size": "23px"}, 
                    "nav-link": {"color": "black", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
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
            
        elif app == "Favourites":
            if st.session_state.get('logged_in'):
                favourites.app()
            else:
                st.warning("You need to log in to access the favourites page.")
        
        elif app == "Logout":
            logout.app()  # Call the logout function

# To run the app
if __name__ == '__main__':
    app = MultiApp()
    app.add_app("Account", account.app)
    app.add_app("Home", slash_user_interface.app)
    app.add_app("Favourites", favourites.app)
    app.run()
