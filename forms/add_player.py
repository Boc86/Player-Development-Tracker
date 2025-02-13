import hydralit as hy
from functions.database import save_changes, strip_name
import supabase

supabase_url = hy.secrets["supabase_url"]
supabase_key = hy.secrets["supabase_key"]
supabase_client = supabase.create_client(supabase_url, supabase_key)

def add_player_form():
    team_names_data = supabase_client.table("team").select("team_name").execute().data
    positions_data = supabase_client.table("position").select("position_name").execute().data

    # Extract team names and position names from the data
    team_names = [team["team_name"] for team in team_names_data]
    positions = [position["position_name"] for position in positions_data]

    with hy.form(key="Add Player"):
        hy.write("Add Player")
        first_name = hy.text_input("First Name", key="first_name")
        sur_name = hy.text_input("Surname", key="sur_name")
        email = hy.text_input("Email", key="email")
        team = hy.selectbox("Team", options=team_names, key="team", index=None)
        position = hy.selectbox("Possition", options=positions, key="position", index=None)
        

        add_player_button: bool = hy.form_submit_button(label="Add Plyer")

        if add_player_button:
            
            team_data = supabase_client.table("team").select("id").eq("team_name", team).execute().data
            position_data = supabase_client.table("position").select("id").eq("position_name", position).execute().data

            if not team_data:
                hy.error(f"Team '{team}' not found.")
                return  # Stop execution if team is not found

            if not position_data:
                hy.error(f"Position '{position}' not found.")
                return  # Stop execution if position is not found

            team_id = team_data[0]["id"]
            position_id = position_data[0]["id"]

            data = [first_name, sur_name, email, team_id, position_id]
            save_changes("add_player", data)