import sys
import os
import subprocess
import cgi

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../database/'))
import database_pb2

def get_daily_style(player):
	return player.daily_style

def get_weekly_style(player):
	return player.weekly_style

def get_monthly_style(player):
	return player.monthly_style

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
		players_by_id[player] = database_pb2.players_entry()

	for player in weekly_leaders.leaders:
		players_by_id[player] = database_pb2.players_entry()

	for player in monthly_leaders.leaders:
		players_by_id[player] = database_pb2.players_entry()

	# Look up all players in the database.
	for key in players_by_id.keys():
		run = [leaderboards, "-d", database, "get_player", str(key)]
		process = subprocess.Popen(run, stdout=subprocess.PIPE)
		process.wait()

		try:
			players_by_id[key].ParseFromString(process.stdout.read())
		except:
			print 'Error getting player ' + str(key)
			continue

	# Now we have a list of all players. Time to make some HTML.

	html =  "<div id='leaderboard_short'>"

	if len(daily_leaders.leaders) > 0:
		html += "<div><strong>Daily Leader:</strong> "
	
		player = players_by_id[daily_leaders.leaders[0]]

		if player.account_id == 0:
			html += "<em>Error</em>"
		else:
			profile_id = 76561197960265728 + player.account_id
			unsafe_player_name = player.name
			safe_player_name = cgi.escape( unsafe_player_name )
			style = int(player.daily_style)
			html += "<a href='http://steamcommunity.com/profiles/" + str(profile_id) + "'>" + safe_player_name + "</a> - " + str(style) + " style\n"

		html += "</div>"

	if len(weekly_leaders.leaders) > 0:
		html += "<div><strong>Weekly Leader:</strong> "

		player = players_by_id[weekly_leaders.leaders[0]]

		if player.account_id == 0:
			html += "<em>Error</em>"
		else:
			profile_id = 76561197960265728 + player.account_id
			unsafe_player_name = player.name
			safe_player_name = cgi.escape( unsafe_player_name )
			style = int(player.weekly_style)
			html += "<a href='http://steamcommunity.com/profiles/" + str(profile_id) + "'>" + safe_player_name + "</a> - " + str(style) + " style\n"

		html += "</div>"

	if len(monthly_leaders.leaders) > 0:
		html += "<div><strong>Monthly Leader:</strong> "

		player = players_by_id[monthly_leaders.leaders[0]]

		if player.account_id == 0:
			html += "<em>Error</em>"
		else:
			profile_id = 76561197960265728 + player.account_id
			unsafe_player_name = player.name
			safe_player_name = cgi.escape( unsafe_player_name )
			style = int(player.monthly_style)
			html += "<a href='http://steamcommunity.com/profiles/" + str(profile_id) + "'>" + safe_player_name + "</a> - " + str(style) + " style\n"

		html += "</div>"

	html += "<a class='seeall' href='http://data.doubleactiongame.com/leaderboard'>See all</a>"
	html += "</div>"

	fp = open(output + '/short.html', 'w')
	fp.write(html.encode('utf8'))
	fp.close()

	html =  "<div id='leaderboard'>"

	html += "<div class='leaders'>"
	html += "<h2>Daily Leaders</h2>"
	html += "<table><col width='30'><tr><th></th><th>Player Name</th><th>Style</th></tr>\n"
	html += output_n_rows(daily_leaders, players_by_id, get_daily_style, 10)
	html += "</table>"
	html += "<a href='/leaderboard/?daily'>See more...</a>"
	html += "</div>"

	html += "<div class='leaders'>"
	html += "<h2>Weekly Leaders</h2>"
	html += "<table><col width='30'><tr><th></th><th>Player Name</th><th>Style</th></tr>\n"
	html += output_n_rows(weekly_leaders, players_by_id, get_weekly_style, 10)
	html += "</table>"
	html += "<a href='/leaderboard/?weekly'>See more...</a>"
	html += "</div>"

	html += "<div class='leaders'>"
	html += "<h2>Monthly Leaders</h2>"
	html += "<table><col width='30'><tr><th></th><th>Player Name</th><th>Style</th></tr>\n"
	html += output_n_rows(monthly_leaders, players_by_id, get_monthly_style, 10)
	html += "</table>"
	html += "<a class='seeall' href='/leaderboard/?monthly'>See more...</a>"
	html += "</div>"

	html += "</div>"

	fp = open(output + '/all.html', 'w')
	fp.write(html.encode('utf8'))
	fp.close()

	html =  "<div id='leaderboard'>"

	html += "<div class='leaders'>"
	html += "<h2>Daily Leaders</h2>"
	html += "<table><col width='30'><tr><th></th><th>Player Name</th><th>Style</th></tr>\n"
	html += output_n_rows(daily_leaders, players_by_id, get_daily_style, 100)
	html += "</table>"
	html += "<a class='seeall' href='/leaderboard/'>Return</a>"
	html += "</div>"

	html += "</div>"

	fp = open(output + '/daily.html', 'w')
	fp.write(html.encode('utf8'))
	fp.close()

	html =  "<div id='leaderboard'>"

	html += "<div class='leaders'>"
	html += "<h2>Weekly Leaders</h2>"
	html += "<table><col width='30'><tr><th></th><th>Player Name</th><th>Style</th></tr>\n"
	html += output_n_rows(weekly_leaders, players_by_id, get_weekly_style, 100)
	html += "</table>"
	html += "<a class='seeall' href='/leaderboard/'>Return</a>"
	html += "</div>"

	html += "</div>"

	fp = open(output + '/weekly.html', 'w')
	fp.write(html.encode('utf8'))
	fp.close()

	html =  "<div id='leaderboard'>"

	html += "<div class='leaders'>"
	html += "<h2>Monthly Leaders</h2>"
	html += "<table><col width='30'><tr><th></th><th>Player Name</th><th>Style</th></tr>\n"
	html += output_n_rows(monthly_leaders, players_by_id, get_monthly_style, 100)
	html += "</table>"
	html += "<a class='seeall' href='/leaderboard/'>Return</a>"
	html += "</div>"

	html += "</div>"

	fp = open(output + '/monthly.html', 'w')
	fp.write(html.encode('utf8'))
	fp.close()

def output_n_rows(leaders, players_by_id, stylefunc, n):
	rank = 1
	html = ''
	for player_id in leaders.leaders:
		player = players_by_id[player_id]

		if player.account_id == 0:
			html += "<tr><td>" + str(rank) + "</td><td class='player'>Error</td><td></td></tr>"
		else:
			profile_id = 76561197960265728 + player.account_id
			unsafe_player_name = player.name
			safe_player_name = cgi.escape( unsafe_player_name )
			style = int(stylefunc(player))
			html += "<tr class='rank" + str(rank) + " account" + str(player.account_id) + "'><td>" + str(rank) + "</td><td class='player'><a href='http://steamcommunity.com/profiles/" + str(profile_id) + "'>" + safe_player_name + "</a></td><td>" + str(style) + "</td></tr>\n"
		rank += 1

		if rank > n:
			return html

	return html
