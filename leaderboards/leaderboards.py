import sys
import os
import subprocess

sys.path.append(os.path.abspath('../database/'))
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

	print str(len(daily_leaders.leaders)) + " daily leaders"
	print str(len(weekly_leaders.leaders)) + " weekly leaders"
	print str(len(monthly_leaders.leaders)) + " monthly leaders"

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
	print "DAILY LEADERS"
	print

	for player in daily_leaders.leaders:
		print players_by_id[player].name + " - " + str(players_by_id[player].daily_style)

	print
	print
	print "WEEKLY LEADERS"
	print

	for player in weekly_leaders.leaders:
		print players_by_id[player].name + " - " + str(players_by_id[player].weekly_style)

	print
	print
	print "MONTHLY LEADERS"
	print

	for player in monthly_leaders.leaders:
		print players_by_id[player].name + " - " + str(players_by_id[player].monthly_style)
