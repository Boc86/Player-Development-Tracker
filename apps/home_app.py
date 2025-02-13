import os
import streamlit as st
from hydralit import HydraHeadApp

MENU_LAYOUT = [1,1,1,7,2]

class HomeApp(HydraHeadApp):

    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    
    def run(self):
        try:
            st.markdown("<h1 style='text-align:center; color:white;'>Welcome to KRFC Player Development Tracker</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:left;'>Your central hub for managing player development and team performance.</p>", unsafe_allow_html=True)

            st.write("### Key Features:")
            st.write("- **Player Dashboards:** Track individual player stats and development scores.")
            st.write("- **Team Management:** Organize and manage your teams effectively.")
            st.write("- **Admin Panel:** Manage users and teams with ease.")

            st.write("### Get Started:")
            st.write("- Use the navigation menu on the left to explore the different sections of the app.")
        except Exception as e:
            st.error(f"Error in home app: {str(e)}")
            return None