import hydralit as hy
from hydralit import HydraHeadApp
import sqlite3
import pandas as pd
from functions.database import save_changes
from forms.add_team import add_team_form

MENU_LAYOUT = [1,1,1,7,2]

@hy.dialog("Add Team")
def show_add_team_form():
    add_team_form()

class AdminApp(HydraHeadApp):

    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    
    def run(self):

        conn = sqlite3.connect('player_tracker.db')
        cursor = conn.cursor()
        
        

        with hy.expander("Users"):
            try:
                hy.write("User Admin Panel")
                users = cursor.execute(f"SELECT * FROM user").fetchall()
                user_data = pd.DataFrame.from_records(users, columns=[i[0] for i in cursor.description])
                df = hy.data_editor(user_data, hide_index=True, num_rows="dynamic")

                save = hy.button("Save")
                if save:
                    save_changes("user", df)

            except Exception as e:  
                return None
        
        with hy.expander("Teams"):
            try:
                hy.write("Team Admin Panel")
                teams = cursor.execute(f"SELECT * FROM team").fetchall()
                team_data = pd.DataFrame.from_records(teams, columns=[i[0] for i in cursor.description])
                db = hy.data_editor(team_data, hide_index=True, num_rows="dynamic")

                add = hy.button("Add Team")
                if add:
                    show_add_team_form()
                
                save = hy.button("Save Changes")
                if save:
                    save_changes("team_save", db)
                

            except Exception as e:  
                return None