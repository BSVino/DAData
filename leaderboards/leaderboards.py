import sys
import os
import subprocess
import cgi

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../database/'))
import database_pb2

def calc_leaders(database, leaderboards, output):
	run = [leaderboards, "-d", database, "calc_leaders"]
	process = subprocess.Popen(run)
	process.wait()

	run = [leaderboards, "-d", database, "get_leaders", "daily"]
	process = subprocess.Popen(run, stdout=subprocess.PIPE)
	process.wait()

	content = process.stdout.read()

	daily_leaders = database_pb2.leaders_entry()

	try:
		daily_leaders.ParseFromString(content)
	except:
		return

	run = [leaderboards, "-d", database, "get_leaders", "weekly"]
	process = subprocess.Popen(run, stdout=subprocess.PIPE)
	process.wait()

	content = process.stdout.read()

	weekly_leaders = database_pb2.leaders_entry()

	try:
		weekly_leaders.ParseFromString(content)
	except:
		return

	run = [leaderboards, "-d", database, "get_leaders", "monthly"]
	process = subprocess.Popen(run, stdout=subprocess.PIPE)
	process.wait()

	content = process.stdout.read()

	monthly_leaders = database_pb2.leaders_entry()

	try:
		monthly_leaders.ParseFromString(content)
	except:
		return

	players_by_id = {}

	# Initialize all players to empty lists, just so we have the keys, to avoid repeated lookups of players in multiple lists.
	for player in daily_leaders.leaders:
		players_by_id[player] = []

	for player in weekly_leaders.leaders:
		players_by_id[player] = []

	for player in monthly_leaders.leaders:
		players_by_id[player] = []

	# Look up all players in the database.
	for key in players_by_id.keys():
		run = [leaderboards, "-d", database, "get_player", str(key)]
		process = subprocess.Popen(run, stdout=subprocess.PIPE)
		process.wait()

		pb_player = database_pb2.players_entry()

		pb_player.ParseFromString(process.stdout.read())
		players_by_id[key] = pb_player

	# Now we have a list of all players. Time to make some HTML.

	html =  "<div id='leaderboard'>"

	html += "<div class='leaders'>"
	html += "<h2>Daily Leaders</h2>"
	html += "<table><tr><th>Player Name</th><th>Score</th></tr>"
	for player_id in daily_leaders.leaders:
		player = players_by_id[player_id]
		profile_id = 76561197960265728 + player.account_id
		unsafe_player_name = player.name
		safe_player_name = cgi.escape( unsafe_player_name )
		style = int(player.daily_style)
		html += "<tr><td class='player'><a href='http://steamcommunity.com/profiles/" + str(profile_id) + "'>" + safe_player_name + "</a></td><td>" + str(style) + "</td></tr>"
	html += "</table>"
	html += "</div>"

	html += "<div class='leaders'>"
	html += "<h2>Weekly Leaders</h2>"
	html += "<table><tr><th>Player Name</th><th>Score</th></tr>"
	for player_id in weekly_leaders.leaders:
		player = players_by_id[player_id]
		profile_id = 76561197960265728 + player.account_id
		unsafe_player_name = player.name
		safe_player_name = cgi.escape( unsafe_player_name )
		style = int(player.weekly_style)
		html += "<tr><td class='player'><a href='http://steamcommunity.com/profiles/" + str(profile_id) + "'>" + safe_player_name + "</a></td><td>" + str(style) + "</td></tr>"
	html += "</table>"
	html += "</div>"

	html += "<div class='leaders'>"
	html += "<h2>Monthly Leaders</h2>"
	html += "<table><tr><th>Player Name</th><th>Score</th></tr>"
	for player_id in monthly_leaders.leaders:
		player = players_by_id[player_id]
		profile_id = 76561197960265728 + player.account_id
		unsafe_player_name = player.name
		safe_player_name = cgi.escape( unsafe_player_name )
		style = int(player.monthly_style)
		html += "<tr><td class='player'><a href='http://steamcommunity.com/profiles/" + str(profile_id) + "'>" + safe_player_name + "</a></td><td>" + str(style) + "</td></tr>"
	html += "</table>"
	html += "</div>"

	html += "</div>"

	fp = open(output, 'w')
	fp.write(html.encode('utf8'))
	fp.close()
