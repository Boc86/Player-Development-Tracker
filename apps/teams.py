import hydralit as hy
from hydralit import HydraHeadApp
import pandas as pd
from functions.database import save_changes
from functions.insights import get_insights
from forms.add_player import add_player_form
import supabase
import statistics as stat
from functions.radar_chart import radar_chart
import streamlit as st
import json

MENU_LAYOUT = [1, 1, 1, 7, 2]

change_column_config = {
    "id_player": None,
    "first_name": "First Name",
    "sur_name": "Surname",
    "email": "Email",
    "team_id": None,
    "position_id": "Position",
    "id_dev": None,
    "player_id": None,
    "comments": "Comments",
    "passing": "Passing",
    "catching": "Catching",
    "tackling": "Tackling",
    "kicking": "Kicking",
    "rucking": "Rucking",
    "scrummaging": "Scrummaging",
    "attack": "Attack",
    "defence": "Defence",
    "positional_awareness": "Positional Awareness",
    "confidence": "Confidence"
}

@hy.dialog("Team Insights", width="large")
def team_insights_dialog(data):
    hy.markdown(data)


def create_team_radar(hd):
    try:
        r = [stat.mean(hd["passing"]), stat.mean(hd["catching"]),
             stat.mean(hd["tackling"]), stat.mean(hd["kicking"]),
             stat.mean(hd["rucking"]), stat.mean(hd["scrummaging"]),
             stat.mean(hd["attack"]), stat.mean(hd["defence"]),
             stat.mean(hd["positional_awareness"]), stat.mean(hd["confidence"])]
        theta = ["Passing", "Catching", "Tackling", "Kicking", "Rucking",
                 "Scrummaging", "Attack", "Defence", "Positional Awareness", "Confidence"]

        data = {"r": r, "theta": theta}
        return radar_chart(data, "Team Stats")
    except Exception as e:
        print(f"Error creating radar chart: {str(e)}")  # Debug print
        return None


@hy.dialog("Add Player")
def show_add_player_form():
    add_player_form()


class TeamsApp(HydraHeadApp):

    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.supabase_url = hy.secrets["supabase_url"]
        self.supabase_key = hy.secrets["supabase_key"]
        self.supabase_client = supabase.create_client(self.supabase_url, self.supabase_key)

    def run(self):
        try:

            current_user_id = hy.session_state["user_id"]
            if hy.session_state["role"] == "1":
                teams = self.supabase_client.table("team").select("*").execute()
            else:
                filter_string = f'coach_id.eq.{current_user_id},assistant_coach1_id.eq.{current_user_id},assistant_coach2_id.eq.{current_user_id},assistant_coach3_id.eq.{current_user_id},assistant_coach4_id.eq.{current_user_id},assistant_coach5_id.eq.{current_user_id},director_of_rugby_id.eq.{current_user_id}'
                teams = self.supabase_client.table("team").select("*").or_(filter_string).execute()
            
            team_names = [team["team_name"] for team in teams.data]
            team_names.sort()

            col1, col2 = st.columns([2, 1])

            with col1:
                selcol = st.columns(3)
                with selcol[0]:
                    selected_team_name = st.selectbox("Select Team", options=team_names, key="team_name",
                                                        index=0 if team_names else None)

                selected_team = next((team for team in teams.data if team["team_name"] == selected_team_name), None)

                if selected_team:
                    team_id = selected_team["id"]
                    team_players = self.supabase_client.table("player").select("*").eq("team_id", team_id).execute().data

                    all_player_ids = [player["id"] for player in team_players]
                    player_scores = self.supabase_client.table("development_score").select("*").in_("player_id",
                                                                                                      all_player_ids).execute().data
                    player_scores_df = pd.DataFrame(player_scores)

                    team_players_df = pd.DataFrame(team_players)

                    positions = self.supabase_client.table("position").select("*").execute().data
                    position_map = {pos["id"]: pos["position_name"] for pos in positions}

                    if not team_players_df.empty:
                        if not player_scores_df.empty:
                            merged_df = pd.merge(team_players_df, player_scores_df, left_on="id", right_on="player_id",
                                                  suffixes=('_player', '_dev'))
                        else:
                            merged_df = team_players_df
                            st.warning("No development scores found for players in this team.")

                        merged_df["position_id"] = merged_df["position_id"].map(position_map)

                        st.subheader("Players")
                        sorted_df = merged_df.sort_values(by="sur_name").reset_index(drop=True)
                        hd = hy.data_editor(sorted_df, hide_index=True, num_rows="dynamic",
                                            column_config=change_column_config)
                    else:
                        st.info("No players found for this team.")
                else:
                    st.warning("No team selected.")
                
                with selcol[1]:
                    coaches = self.supabase_client.table("team").select("coach_id", "assistant_coach1_id", "assistant_coach2_id", "assistant_coach3_id", "assistant_coach4_id", "assistant_coach5_id").eq("id", selected_team["id"]).execute().data
                    hy.write(f"Coaches:")
                    for coach in coaches:
                        for key, value in coach.items():
                            if value is not None:
                                coach_name = self.supabase_client.table("user").select("first_name", "sur_name").eq("id", value).execute().data[0]
                                hy.write(f"{coach_name['first_name']} {coach_name['sur_name']}, ")
                
                with selcol[2]:
                    # Format team data for insights
                    team_data = {
                        'team_name': selected_team_name,
                        'player_count': len(hd),
                        'average_scores': {
                            'passing': stat.mean(hd['passing']),
                            'catching': stat.mean(hd['catching']),
                            'tackling': stat.mean(hd['tackling']),
                            'kicking': stat.mean(hd['kicking']),
                            'rucking': stat.mean(hd['rucking']),
                            'scrummaging': stat.mean(hd['scrummaging']),
                            'attack': stat.mean(hd['attack']),
                            'defence': stat.mean(hd['defence']),
                            'positional_awareness': stat.mean(hd['positional_awareness']),
                            'confidence': stat.mean(hd['confidence'])
                        },
                        'players': [
                            {
                                'name': f"{row['first_name']} {row['sur_name']}",
                                'position': row['position_id'],
                                'scores': {
                                    'passing': row['passing'],
                                    'catching': row['catching'],
                                    'tackling': row['tackling'],
                                    'kicking': row['kicking'],
                                    'rucking': row['rucking'],
                                    'scrummaging': row['scrummaging'],
                                    'attack': row['attack'],
                                    'defence': row['defence'],
                                    'positional_awareness': row['positional_awareness'],
                                    'confidence': row['confidence']
                                }
                            }
                            for _, row in hd.iterrows()
                        ]
                    }
                with selcol[2]:
                    generate_insights = st.button("Generate Team Insights", key="generate_insights")
                    if generate_insights:
                        insights = get_insights(json.dumps(team_data), "team")
                        if insights:
                            team_insights_dialog(insights)
                        else:
                            hy.error("Failed to generate team insights")
                                

                with col2:
                    if selected_team and not team_players_df.empty:
                        st.subheader("Team Stats")
                        fig = create_team_radar(hd)
                        if fig is not None:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.error("Failed to create radar chart")

            cola, colb, _ = st.columns([1, 1, 8])
            with cola:
                add = st.button("Add Player", use_container_width=True)
                if add:
                    show_add_player_form()
            with colb:
                save = st.button("Save Changes", use_container_width=True)
                if save:
                    save_changes("save_player", hd)


        except Exception as e:
            st.error(f"Error in teams app: {str(e)}")
            return None