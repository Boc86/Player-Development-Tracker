import hydralit as hy
from functions.database import save_changes, strip_name
import sqlite3

def add_team_form():
    conn = sqlite3.connect('player_tracker.db')
    cursor = conn.cursor()

    coaches = cursor.execute("SELECT first_name, sur_name FROM user WHERE role_id = 1 OR role_id = 2 OR role_id = 4").fetchall()
    cleaned_coaches = strip_name(coaches)

    with hy.form(key="Add Team"):
        hy.write("Add Team")
        team_name = hy.text_input("Team Name", key="team_name")
        coach = hy.selectbox("Coach", options=cleaned_coaches, key="coach", index=None)
        assistant_coach1 = hy.selectbox("Assistant Coach 1", options=cleaned_coaches, key="assistant_coach1", index=None)
        assistant_coach2 = hy.selectbox("Assistant Coach 2", options=cleaned_coaches, key="assistant_coach2", index=None)
        assistant_coach3 = hy.selectbox("Assistant Coach 3", options=cleaned_coaches, key="assistant_coach3", index=None)
        assistant_coach4 = hy.selectbox("Assistant Coach 4", options=cleaned_coaches, key="assistant_coach4", index=None)
        assistant_coach5 = hy.selectbox("Assistant Coach 5", options=cleaned_coaches, key="assistant_coach5", index=None)
        director_of_rugby = hy.selectbox("Director of Rugby", options=cleaned_coaches, key="director_of_rugby", index=None)

        add_team_button = hy.form_submit_button(label="Add Team")

        if add_team_button:
            data = [team_name, coach, assistant_coach1, assistant_coach2, assistant_coach3, assistant_coach4, assistant_coach5, director_of_rugby]
            print(data)
            #save_changes("team_add", data)