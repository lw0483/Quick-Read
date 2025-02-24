import requests
import array
import io
from bs4 import BeautifulSoup

class Player:
    def __init__(self, name, position, team, college, href):
        self.name = name
        self.position = position
        self.team = team
        self.college = college
        self.href = href
		

# get player name from user then split into a first and last name
playerName = input("Enter a player's name: ")
names = playerName.split(" ")
firstName = names[0]
lastName = names[1]

# setup page with the url plus the player's last name initial
URL = "https://www.pro-football-reference.com"
page = requests.get(URL + "/players/" + lastName[0])

# use Beutiful soup to parse the page and find the list of all players with the same starting intial for last name
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="div_players")

# finds all player pages matching the name given by the user
playerPages = results.find_all("a", string=playerName)

# loops through each player page, constructs each as an object to add to an array
players = []
for playerPage in playerPages:
	href = playerPage.get("href")
	page = requests.get(URL + href)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find("div", id="meta")
    
	# finds the spot where Position is written in bold, then finds the next element and removes ": "
	position = results.find("strong", string="Position").next_sibling.strip()[2:]

	# finds the team tag for the player 
	# if they are not currently on a team this tag won't exist
	teamTag = results.find("strong", string="Team")
	
	if (teamTag):
		team = teamTag.find_next("a").get_text().strip()
	else :
		team = "No Team"

	# finds the spot where College is in bold, then finds the next link object and extracts its name (in this case the college's name)
	college = results.find("strong", string="College").find_next("a").get_text().strip()

	players.append(Player(playerName, position, team, college, href))
	


for player in players :
	print(player.name, "\n", player.position, "\n", player.team, "\n", player.college, "\n", player.href)
	




