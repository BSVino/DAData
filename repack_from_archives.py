#!/usr/bin/python

import tarfile     #Working with tarballs
import argparse
import os
import time
import sys
import datetime

import dadb

import data_pb2

parser = argparse.ArgumentParser(description="Unpack the archives and re-create the database.")

parser.add_argument('-a', '--archive', nargs=1, metavar='directory', help='The directory containing the archives', required=True)
parser.add_argument('-d', '--database', nargs=1, metavar='file', help='The file name of the database to store the results', required=True)

args = parser.parse_args()

start_time = time.time()

f = []
for (dirpath, dirnames, filenames) in os.walk(args.archive[0]):
  f.extend(filenames)

print "Opening " + (str)(len(f)) + " archives..."

skipped = 0
duplicates = 0
added = 0
total_added = 0

database = open(args.database[0], 'w')

files = {}

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

    dadb.db_store(content, database)
    added += 1
    total_added += 1

    if gamedata.timestamp < lowest_timestamp:
      lowest_timestamp = gamedata.timestamp

    if gamedata.timestamp > highest_timestamp:
      highest_timestamp = gamedata.timestamp

  archive.close()

  print "Added " + str(added) + " buffers to the archive. Skipped " + str(skipped) + " bad buffers and " + str(duplicates) + " duplicates."
  duplicates = 0
  added = 0
  skipped = 0

  print "Archive date range: [" + datetime.datetime.fromtimestamp(lowest_timestamp).strftime("%c") + "] to [" + datetime.datetime.fromtimestamp(highest_timestamp).strftime("%c") + "]"

print "Done. Total buffers in archive: " + str(total_added)

end_time = time.time()

print "Finished in " + (str)(end_time - start_time) + " seconds."
