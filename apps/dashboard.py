import hydralit as hy
from hydralit import HydraHeadApp
import pandas as pd
import supabase
from functions.radar_chart import radar_chart
import streamlit as st

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


def create_player_radar(hd):
    try:
        r = [hd["passing"], hd["catching"],
             hd["tackling"], hd["kicking"],
             hd["rucking"], hd["scrummaging"],
             hd["attack"], hd["defence"],
             hd["positional_awareness"], hd["confidence"]]
        theta = ["Passing", "Catching", "Tackling", "Kicking", "Rucking",
                 "Scrummaging", "Attack", "Defence", "Positional Awareness", "Confidence"]

        data = {"r": r, "theta": theta}
        return radar_chart(data, "Player Stats")
    except Exception as e:
        print(f"Error creating radar chart: {str(e)}")  # Debug print
        return None


def get_score_color(score):
    """Returns a color based on score value (0=red, 5=green, 10=blue)"""
    if score <= 5:
        red = int(255 * (5 - score) / 5)
        green = int(255 * score / 5)
        return f"rgb({red}, {green}, 0)"
    else:
        green = int(255 * (10 - score) / 5)
        blue = int(255 * (score - 5) / 5)
        return f"rgb(0, {green}, {blue})"


def display_player_card(title, value):
    """Display a card with colored score"""
    st.markdown(
        f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 5px;">
            <h4>{title}</h4>
            <p style="color: {get_score_color(value)}; font-size: 20px; font-weight: bold;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


class DashboardApp(HydraHeadApp):

    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.supabase_url = hy.secrets["supabase_url"]
        self.supabase_key = hy.secrets["supabase_key"]
        self.supabase_client = supabase.create_client(self.supabase_url, self.supabase_key)

    def run(self):
        try:
            cole, colf, colg = st.columns([1, 1, 2])
            with cole:

                current_user_id = hy.session_state["user_id"]
                if hy.session_state["role"] == "1":
                    teams = self.supabase_client.table("team").select("*").execute()
                else:
                    filter_string = f'coach_id.eq.{current_user_id},assistant_coach1_id.eq.{current_user_id},assistant_coach2_id.eq.{current_user_id},assistant_coach3_id.eq.{current_user_id},assistant_coach4_id.eq.{current_user_id},assistant_coach5_id.eq.{current_user_id},director_of_rugby_id.eq.{current_user_id}'
                    teams = self.supabase_client.table("team").select("*").or_(filter_string).execute()
                
                team_names = [team["team_name"] for team in teams.data]

                selected_team_name = st.selectbox("Select Team", options=team_names, key="team_name",
                                                    index=0 if team_names else None)

                selected_team = next((team for team in teams.data if team["team_name"] == selected_team_name), None)

            with colf:
                if selected_team:
                    players = self.supabase_client.table("player").select("*").eq("team_id", selected_team["id"]).execute()

                    player_options = [f"{p['first_name']} {p['sur_name']}" for p in players.data]
                    player_map = {f"{p['first_name']} {p['sur_name']}": p for p in players.data}

                    selected_player_name = st.selectbox("Select Player", options=player_options, key="player_name",
                                                        index=0 if player_options else None)

                    if selected_player_name:
                        selected_player = player_map[selected_player_name]

                        player_scores = self.supabase_client.table("development_score").select("*").eq("player_id",
                            selected_player["id"]).execute()

                        if player_scores.data:
                            latest_score = player_scores.data[-1]

                            positions = self.supabase_client.table("position").select("*").execute().data
                            position_map = {pos["id"]: pos["position_name"] for pos in positions}
                            position = position_map.get(selected_player["position_id"], "Unknown")
                        
                        else:
                            st.warning("No development scores found for this player")
                    else:
                        st.warning("No player selected")
                else:
                    st.warning("No team selected")

            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f"""
                <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h3>Player Bio</h3>
                    <div style="display: flex;">
                        <div style="flex: 1;">
                            <p><strong>First Name:</strong> {selected_player['first_name']}</p>
                            <p><strong>Surname:</strong> {selected_player['sur_name']}</p>
                            <p><strong>Email:</strong> {selected_player['email']}</p>
                            <p><strong>Position:</strong> {position}</p>
                            <p><strong>Comments:</strong> {latest_score['comments']}</p>
                        </div>
                        <div style="flex: 1;">
                        </div>""", unsafe_allow_html=True)

                fig = create_player_radar(latest_score)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

            with col2:
                score_cols = st.columns(2)
                scores = [
                    ("Passing", latest_score["passing"]),
                    ("Catching", latest_score["catching"]),
                    ("Tackling", latest_score["tackling"]),
                    ("Kicking", latest_score["kicking"]),
                    ("Rucking", latest_score["rucking"]),
                    ("Scrummaging", latest_score["scrummaging"]),
                    ("Attack", latest_score["attack"]),
                    ("Defence", latest_score["defence"]),
                    ("Positional Awareness", latest_score["positional_awareness"]),
                    ("Confidence", latest_score["confidence"])
                ]

                for i, (title, value) in enumerate(scores):
                    with score_cols[i % 2]:
                        display_player_card(title, value)

        except Exception as e:
            st.error(f"Error in dashboard: {str(e)}")
            return None