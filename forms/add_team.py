import hydralit as hy
from functions.database import save_changes, strip_name
import supabase

supabase_url = hy.secrets["supabase_url"]
supabase_key = hy.secrets["supabase_key"]
supabase_client = supabase.create_client(supabase_url, supabase_key)

def add_team_form():
    response = supabase_client.table("user").select("first_name, sur_name").in_("role_id", [1, 2, 4]).execute()
    cleaned_coaches = strip_name(response.data)

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

        add_team_button: bool = hy.form_submit_button(label="Add Team")

        if add_team_button:
            if not coach == None:
                coach_id = supabase_client.table("user").select("id").eq("first_name", coach.split(" ")[0]).eq("sur_name", coach.split(" ")[1]).execute().data[0]["id"]
            else:
                coach_id = coach

            if not assistant_coach1 == None:
                assistant_coach1_id = supabase_client.table("user").select("id").eq("first_name", coach.split(" ")[0]).eq("sur_name", coach.split(" ")[1]).execute().data[0]["id"]
            else:
                assistant_coach1_id = assistant_coach1

            if not assistant_coach2 == None:
                assistant_coach2_id = supabase_client.table("user").select("id").eq("first_name", coach.split(" ")[0]).eq("sur_name", coach.split(" ")[1]).execute().data[0]["id"]
            else:
                assistant_coach2_id = assistant_coach2

            if not assistant_coach3 == None:
                assistant_coach3_id = supabase_client.table("user").select("id").eq("first_name", coach.split(" ")[0]).eq("sur_name", coach.split(" ")[1]).execute().data[0]["id"]
            else:
                assistant_coach3_id = assistant_coach3

            if not assistant_coach4 == None:
                assistant_coach4_id = supabase_client.table("user").select("id").eq("first_name", coach.split(" ")[0]).eq("sur_name", coach.split(" ")[1]).execute().data[0]["id"]
            else:
                assistant_coach4_id = assistant_coach4

            if not assistant_coach5 == None:
                assistant_coach5_id = supabase_client.table("user").select("id").eq("first_name", coach.split(" ")[0]).eq("sur_name", coach.split(" ")[1]).execute().data[0]["id"]
            else:
                assistant_coach5_id = assistant_coach5
            
            if not director_of_rugby == None:
                director_of_rugby_id = supabase_client.table("user").select("id").eq("first_name", coach.split(" ")[0]).eq("sur_name", coach.split(" ")[1]).execute().data[0]["id"]
            else:
                director_of_rugby_id = director_of_rugby

            data = [team_name, coach_id, assistant_coach1_id, assistant_coach2_id, assistant_coach3_id, assistant_coach4_id, assistant_coach5_id, director_of_rugby_id]
            save_changes("team_add", data)