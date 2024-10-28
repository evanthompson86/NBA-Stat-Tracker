from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

# to store each nba players name and their stats
class Player:
    def __init__(self, name, ppg, apg, orpg, drpg):
        self.name = name
        self.ppg = ppg
        self.apg = apg
        self.orpg = orpg
        self.drpg = drpg

# setup website to scrape for stats on each nba player
url = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"
response = requests.get(url)
scrape_page = response.text
parse = BeautifulSoup(scrape_page, "html.parser")

# get name, points per game, assists per game, and rebounds per game of each nba player from the URL
names = parse.findAll("td", attrs={"data-stat":"name_display"})
ppg = parse.findAll("td", attrs={"data-stat":"pts_per_g"})
apg = parse.findAll("td", attrs={"data-stat":"ast_per_g"})
offensive_rpg = parse.findAll("td", attrs={"data-stat":"orb_per_g"})
defensive_rpg = parse.findAll("td", attrs={"data-stat":"drb_per_g"})

# empty list to store each player
list_of_players = []

# stores each players name and corresponding stats in the list_of_players
for (a, b, c, d, e) in zip (names, ppg, apg, offensive_rpg, defensive_rpg):
    new_player = Player(a.text, b.text, c.text, d.text, e.text)
    list_of_players.append(new_player)



top_10_points = list_of_players[:10]

sorted_by_apg = sorted(list_of_players, key=lambda x: float(x.apg) if x.apg.replace('.', '', 1).isdigit() else 0.0, reverse=True)
top_10_assists = sorted_by_apg[:10]

sorted_by_orpg = sorted(list_of_players, key=lambda x: float(x.orpg) if x.orpg.replace('.', '', 1).isdigit() else 0.0, reverse=True)
top_10_orpg = sorted_by_orpg[:10]

sorted_by_drpg = sorted(list_of_players, key=lambda x: float(x.drpg) if x.drpg.replace('.', '', 1).isdigit() else 0.0, reverse=True)
top_10_drpg = sorted_by_drpg[:10]


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('players.html', points=top_10_points, assists=top_10_assists, 
                           offensives=top_10_orpg, defensives=top_10_drpg)

if __name__ == "__main__":
    app.run(debug=True)

