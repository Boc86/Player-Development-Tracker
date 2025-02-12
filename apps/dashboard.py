import os
import streamlit as st
from hydralit import HydraHeadApp

MENU_LAYOUT = [1,1,1,7,2]

class DashboardApp(HydraHeadApp):

    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    
    def run(self):
        try:
            st.markdown("<h1 style='text-align:center;padding: 0px 0px;color:black;font-size:200%;'>Home</h1>",unsafe_allow_html=True) 
        except Exception as e:  
            return None