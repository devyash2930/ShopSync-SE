import streamlit as st

from streamlit_option_menu import option_menu

import account as account
import slash_user_interface as slash_user_interface

st.set_page_config(page_title='ShopSync', layout= "wide")

class MultiApp:
    def __init__(self):
        self.apps = []
    
    def add_app(self,title,function):
        self.apps.append({
            "title":title,
            "function": function
        })
    
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='ShopSync',
                options=['Account', 'Home', 'Favourites','Logout'],
                icons=['person-circle', 'house-fill', 'star-fill', 'box-arrow-right'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
            )
        
        if app=="Account":
            account.app()
        
        elif app=="Home":
            slash_user_interface.app()
    
    run()