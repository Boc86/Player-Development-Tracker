import supabase
import hydralit as hy
import pandas as pd

supabase_url = hy.secrets["supabase_url"]
supabase_key = hy.secrets["supabase_key"]
supabase_client = supabase.create_client(supabase_url, supabase_key)

def strip_name(data):
    cleaned_names = [f"{name['first_name']} {name['sur_name']}" for name in data]
    return cleaned_names

class user:
    def __init__(self, id, first_name, sur_name, email, password_hash, role_id, created_at):
        self.id = id
        self.first_name = first_name
        self.sur_name = sur_name
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id
        self.created_at = created_at

class role:
    def __init__(self, id, role_name):
        self.id = id
        self.role_name = role_name

class player:
    def __init__(self, id, first_name, sur_name, email, team_id, position_id):
        self.id = id
        self.first_name = first_name
        self.sur_name = sur_name
        self.email = email
        self.team_id = team_id
        self.position_id = position_id

class position:
    def __init__(self, id, position_name):
        self.id = id
        self.position_name = position_name

class team: 
    def __init__(self, id, team_name, coach_id, assistant_coach1_id, assistant_coach2_id, assistant_coach3_id, assistant_coach4_id, assistant_coach5_id, director_of_rugby_id):
        self.id = id
        self.team_name = team_name
        self.coach_id = coach_id
        self.assistant_coach1_id = assistant_coach1_id
        self.assistant_coach2_id = assistant_coach2_id
        self.assistant_coach3_id = assistant_coach3_id
        self.assistant_coach4_id = assistant_coach4_id
        self.assistant_coach5_id = assistant_coach5_id
        self.director_of_rugby_id = director_of_rugby_id

class development_score:
    def __init__(self, id, player_id, comments, passing, catching, tackling, kicking, rucking, scrummaging, attack, defence, positional_awareness, confidence):
        self.id = id
        self.player_id = player_id
        self.comments = comments
        self.passing = passing
        self.catching = catching
        self.tackling = tackling
        self.kicking = kicking
        self.rucking = rucking
        self.scrummaging = scrummaging
        self.attack = attack
        self.defence = defence
        self.positional_awareness = positional_awareness
        self.confidence = confidence

def save_changes(table, data):
    if table == "user":
        try:
            df = pd.DataFrame(data)
            print(df)
            for index, row in df.iterrows():
                supabase_client.table("user").update({
                    "first_name": row["first_name"],
                    "sur_name": row["sur_name"],
                    "email": row["email"],
                    "password_hash": row["password_hash"],
                    "role_id": row["role_id"]
                }).eq("id", row["id"]).execute()
                
            hy.success("Users updated successfully")

        except Exception as error:
            hy.error(error)
    
    elif table == "team_add":
        try:
            supabase_client.table("team").insert({
                "team_name": data[0],
                "coach_id": data[1],
                "assistant_coach1_id": data[2],
                "assistant_coach2_id": data[3],
                "assistant_coach3_id": data[4],
                "assistant_coach4_id": data[5],
                "assistant_coach5_id": data[6],
                "director_of_rugby_id": data[7]
            }).execute()
            
            hy.success("Team added successfully")
            hy.rerun()
        
        except Exception as error:
            hy.error(error)
    
    elif table == "team_save":
        try:
            db = pd.DataFrame(data)
            for index, row in db.iterrows():
                supabase_client.table("team").update({
                    "team_name": row["team_name"],
                    "coach_id": row["coach_id"],
                    "assistant_coach1_id": row["assistant_coach1_id"],
                    "assistant_coach2_id": row["assistant_coach2_id"],
                    "assistant_coach3_id": row["assistant_coach3_id"],
                    "assistant_coach4_id": row["assistant_coach4_id"],
                    "assistant_coach5_id": row["assistant_coach5_id"],
                    "director_of_rugby_id": row["director_of_rugby_id"]
                }).eq("id", row["id"]).execute()
                
            hy.success("Team updated successfully")

        except Exception as error:
            hy.error(error)
    
    elif table == "add_player":
        try:

            supabase_client.table("player").insert({
                "first_name": data[0],
                "sur_name": data[1],
                "email": data[2],
                "team_id": data[3],
                "position_id": data[4]
            }).execute()

            supabase_client.table("development_score").insert({
                "player_id": supabase_client.table("player").select("id").eq("first_name", data[0]).eq("sur_name", data[1]).execute().data[0]["id"],
                "passing": 0,
                "catching": 0,
                "tackling": 0,
                "kicking": 0,
                "rucking": 0,
                "scrummaging": 0,
                "attack": 0,
                "defence": 0,
                "positional_awareness": 0,
                "confidence": 0
            }).execute()

            hy.success("Player added successfully")
            hy.rerun()
        
        except Exception as error:
            hy.error(error)
        
    if table == "save_player":
        try:
            db = pd.DataFrame(data)
            for index, row in db.iterrows():
                response = supabase_client.table("development_score").update({
                    "passing": row["passing"],
                    "catching": row["catching"],
                    "tackling": row["tackling"],
                    "kicking": row["kicking"],
                    "rucking": row["rucking"],
                    "scrummaging": row["scrummaging"],
                    "attack": row["attack"],
                    "defence": row["defence"],
                    "positional_awareness": row["positional_awareness"],
                    "confidence": row["confidence"],
                    "comments": row["comments"]
                }).eq("player_id", row["player_id"]).execute()
            
                position_id = supabase_client.table("position").select("id").eq("position_name", row["position_id"]).execute().data[0]["id"]
                response = supabase_client.table("player").update({
                    "first_name": row["first_name"],
                    "sur_name": row["sur_name"],
                    "email": row["email"],
                    "position_id": position_id   
                }).eq("id", row["player_id"]).execute()

            hy.success("Player updated successfully")
            hy.rerun()
        
        except Exception as error:
            hy.error(error)

