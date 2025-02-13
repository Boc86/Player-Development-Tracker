import hydralit as hy
from hydralit import HydraHeadApp
import pandas as pd
from functions.database import save_changes
from forms.add_team import add_team_form
import supabase
import streamlit as st

MENU_LAYOUT = [1, 1, 1, 7, 2]


@hy.dialog("Add Team")
def show_add_team_form():
    add_team_form()


class AdminApp(HydraHeadApp):

    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.supabase_url = hy.secrets["supabase_url"]
        self.supabase_key = hy.secrets["supabase_key"]
        self.supabase_client = supabase.create_client(self.supabase_url, self.supabase_key)

    def run(self):

        with st.expander("User Management"):
            try:
                st.markdown("<h2 style='text-align:left;'>User Admin Panel</h2>", unsafe_allow_html=True)
                response = self.supabase_client.table("user").select("*").execute()
                users = response.data
                user_data = pd.DataFrame(users)
                data = st.data_editor(user_data)

                save = st.button("Save User Changes", key="save_users")
                if save:
                    save_changes("user", data)

            except Exception as e:
                st.error(f"Error in user admin panel: {str(e)}")
                return None

        with st.expander("Team Management"):
            try:
                st.markdown("<h2 style='text-align:left;'>Team Admin Panel</h2>", unsafe_allow_html=True)
                response = self.supabase_client.table("team").select("*").execute()
                teams = response.data
                team_data = pd.DataFrame(teams)
                data = st.data_editor(team_data)

                col1, col2, _, _ = st.columns([1, 1, 5, 5])
                with col1:
                    add = st.button("Add Team", on_click=show_add_team_form)
                with col2:
                    save = st.button("Save Team Changes", key="save_teams")
                    if save:
                        save_changes("team_save", data)

            except Exception as e:
                st.error(f"Error in team admin panel: {str(e)}")
                return None