from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
from nba_api.stats.static import teams
import numpy as np
import requests as rq
import pandas as pd

shots = shotchartdetail.ShotChartDetail(player_id=201939, team_id=1610612744)
data = shots.get_data_frames()[0]
print(data.head())
df = pd.DataFrame(data)
df.to_csv('shotchartdetail.csv')

# get_players returns a list of dictionaries, each representing a player.
"""
nba_players = players.get_players()
print(f"Number of players fetched: {len(nba_players)}")
nba_players[:5]

player_search = [
    player for player in nba_players if player["full_name"] == "Stephen Curry"
][0]
player_search

print(player_search)
"""

# get_teams returns a list of 30 dictionaries, each an NBA team.
"""
nba_teams = teams.get_teams()
print(f"Number of teams fetched: {len(nba_teams)}")
nba_teams[:3]
team_search = [team for team in nba_teams if team["full_name"] == "Golden State Warriors"][0]
team_search
print(team_search)
"""
