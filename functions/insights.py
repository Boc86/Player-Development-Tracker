import hydralit as hy
import requests
import json

def get_insights(player_data, what):
    try:
        # Format the message properly
        if what == "player":
            who = "player"
        elif what == "team":
            who = "team"

        messages = [{
            "role": "user",
            "content": f"You are a highly skilled rugby coach at assessing team and player stats and making recomendations and insights based on the data provided, including recommending training drills to improve weaknesses. All scores are out of a mixumum of 10 with 0 being a danger to themselves or orthers, 5 being where they need to be and 10 exceeding all expectations. Do not make anything up only use the information provided. Provide {who} insights from the following data: {player_data}"
        }]
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {hy.secrets['openrouter_ai_token']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-2.0-pro-exp-02-05:free",
                "messages": messages,
                "temperature": 0.9,
                "max_tokens": 2000,
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
        return None
    except Exception as e:
        print(f"Error in get_insights: {str(e)}")
        return None