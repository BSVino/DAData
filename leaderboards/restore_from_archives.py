#!/usr/bin/python

import tarfile		 #Working with tarballs
import argparse
import os
import time
import sys
import datetime
import subprocess

import leaderboards

sys.path.append(os.path.abspath('../daily-data/'))

import data_pb2

parser = argparse.ArgumentParser(description="Unpack the archives and re-create the leaderboard database.")

parser.add_argument('-a', '--archive', nargs=1, metavar='archives_directory', help='The directory containing the archives', required=True)
parser.add_argument('-f', '--files', nargs=1, metavar='unarchived_directory', help='The directory containing the un-archived files', required=True)
parser.add_argument('-d', '--database', nargs=1, metavar='database_directory', help='The directory containing the lmdb database to store the results', required=True)
parser.add_argument('-l', '--leaderboards', nargs=1, metavar='leaderboards_binary', help='The location of the leaderboards binary', required=True)
parser.add_argument('-o', '--output', nargs=1, metavar='output_file', help='The file to write the result html', required=True)

args = parser.parse_args()

start_time = time.time()

print "Clearing database."
for fp in os.listdir(args.database[0]):
	file_path = os.path.join(args.database[0], fp)
	try:
		if os.path.isfile(file_path):
			os.unlink(file_path)
	except:
		pass

if not os.path.exists(args.database[0]):
	os.makedirs(args.database[0])

f = []
for (dirpath, dirnames, filenames) in os.walk(args.archive[0]):
	f.extend(filenames)

one_hour = 60 * 60
one_day = one_hour * 24
one_week = one_day * 7
one_month = one_day * 31

print "Opening " + (str)(len(f)) + " archives..."

skipped = 0
duplicates = 0
added = 0
total_added = 0

files = {}

files_by_date = {}

for file in f:
	if not file.endswith(".tgz"):
		continue

	archive = tarfile.open(args.archive[0] + "/" + file, 'r')

	print
	print "Storing archive " + args.archive[0] + "/" + file + " with " + str(len(archive.getmembers())) + " buffers..."

	lowest_timestamp = time.time()
	highest_timestamp = 0

	for member in archive.getmembers():
		if len(member.name) < 4 or member.name[-3:] != '.pb':
			continue

		buffer=archive.extractfile(member)
		content=buffer.read()

		if len(content) == 0:
			continue

		gamedata = data_pb2.GameData()

		try:
			gamedata.ParseFromString(content)
		except:
			skipped += 1
			continue

		if member.name in files:
			# We've archived a file with this name already. Check to make sure it's not a duplicate
			if gamedata.timestamp == files[member.name]:
				# It's a duplicate
				duplicates += 1
				continue

		files[member.name] = gamedata.timestamp

		if gamedata.timestamp + one_month < time.time():
			continue

		if len(gamedata.player_list) == 0:
			continue

		files_by_date[gamedata.timestamp] = content

		added += 1
		total_added += 1

		if gamedata.timestamp < lowest_timestamp:
			lowest_timestamp = gamedata.timestamp

		if gamedata.timestamp > highest_timestamp:
			highest_timestamp = gamedata.timestamp

	archive.close()

	print "Added " + str(added) + " buffers to the archive. Skipped " + str(skipped) + " bad buffers and " + str(duplicates) + " duplicates."

	if added > 0:
		print "Added files date range: [" + datetime.datetime.fromtimestamp(lowest_timestamp).strftime("%c") + "] to [" + datetime.datetime.fromtimestamp(highest_timestamp).strftime("%c") + "]"

	duplicates = 0
	added = 0
	skipped = 0


print "Done. Total buffers added from archive: " + str(total_added)

f = []
for (dirpath, dirnames, filenames) in os.walk(args.files[0]):
	f.extend(filenames)

print "Opening " + (str)(len(f)) + " loose files..."

for file in f:
	if not file.endswith(".pb"):
		continue

	fp = open(args.files[0] + "/" + file, 'rb')
	content = fp.read()
	fp.close()

	gamedata = data_pb2.GameData()

	try:
		gamedata.ParseFromString(content)
	except:
		skipped += 1
		continue

	if gamedata.timestamp + one_month < time.time():
		continue

	if len(gamedata.player_list) == 0:
		continue

	files_by_date[gamedata.timestamp] = content

print "Adding " + str(len(files_by_date)) + " buffers to the database."

for key in sorted(files_by_date.keys()):
	content = files_by_date[key]

	gamedata = data_pb2.GameData()

	try:
		gamedata.ParseFromString(content)
	except:
		skipped += 1
		continue

	run = [args.leaderboards[0], "-d", args.database[0], "store"]
	process = subprocess.Popen(run, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	process.stdin.write(content)
	process.stdin.flush()
	process.stdin.close()
	process.wait()

	for line in iter(process.stdout.readline,''):	
		print line,

	if process.returncode != 0:
		print "Error running leaderboards:"
		sys.exit(1)

	days_ago = (time.time() - key)/one_day

	if days_ago > 7:
		print "Clearing weekly"
		run = [args.leaderboards[0], "-d", args.database[0], "reset_weekly"]
		process = subprocess.Popen(run)
		process.wait()
	elif days_ago > 1:
		print "Clearing daily"
		run = [args.leaderboards[0], "-d", args.database[0], "reset_daily"]
		process = subprocess.Popen(run)
		process.wait()

print "Calculating leaders..."

leaderboards.calc_leaders(args.database[0], args.leaderboards[0], args.output[0])

end_time = time.time()

print "Finished in " + (str)(end_time - start_time) + " seconds."
