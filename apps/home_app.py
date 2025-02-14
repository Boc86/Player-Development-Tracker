import hydralit as hy
import streamlit as st
from hydralit import HydraHeadApp

MENU_LAYOUT = [1,1,1,7,2]

class HomeApp(HydraHeadApp):

    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    
    def run(self):
        try:
            with hy.container():

                st.markdown("<h1 style='text-align:left; color:white;'>Welcome to KRFC Player Development Tracker</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:left;'>Your central hub for managing player development and team performance.</p>", unsafe_allow_html=True)

                col1, col2 = hy.columns([3,5])
                with col1:

                    st.markdown(
                        """
                        <div style='background-color: rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                            <h3 style='color: white; margin-bottom: 20px;'>Key Features</h3>
                            <div style='text-align: left; color: white; line-height: 1.6; padding-right: 20px;'>
                                - Admin Panel: Manage users and teams with ease.<br>
                                - Team Management: Organise and manage your teams effectively.<br>
                                - Player Management: Keep track of player stats and development scores.<br>
                                - Player Dashboards: Track individual player stats.<br>
                                - AI Insights: Get insights at team and individual levels.
                            </div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        """
                        <div style='background-color: rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                            <h3 style='color: white; margin-bottom: 20px;'>Get Started</h3>
                            <div style='text-align: left; color: white; line-height: 1.6; padding-right: 20px;'>
                                - Use the navigation menu at the top to access the different sections of the app.
                            </div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

        except Exception as e:
            st.error(f"Error in home app: {str(e)}")
            return None