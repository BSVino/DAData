#!/usr/bin/python

import tarfile     #Working with tarballs
import argparse
import os
import time
import sys
import datetime

import dadb

parser = argparse.ArgumentParser(description="Store protobuf data in a database.")

parser.add_argument('-i', '--input', nargs=1, metavar='directory', help='The directory containing .pb files of data', required=True)
parser.add_argument('-d', '--database', nargs=1, metavar='file', help='The file name of the database to store the results', required=True)
parser.add_argument('-a', '--archive', nargs=1, metavar='directory', help='The directory to output archived .tgz files', required=True)

args = parser.parse_args()

start_time = time.time()

f = []
for (dirpath, dirnames, filenames) in os.walk(args.input[0]):
  f.extend(filenames)

print "Opening " + (str)(len(f)) + " files..."

pbdata = []
for file in f:
  if not file.endswith(".pb"):
    continue

  fp = open(args.input[0] + "/" + file, 'rb')
  pbuffer = fp.read()
  fp.close()

  pbdata.append(pbuffer)

start_store_time = time.time()

print "Storing " + (str)(len(pbdata)) + " buffers..."

db_file = open(args.database[0], 'a')

skipped = 0

lowest_timestamp = time.time()
highest_timestamp = 0

for file in pbdata:
  gamedata = dadb.db_store(file, db_file)
  if gamedata == None:
    skipped += 1
    continue

  if gamedata.timestamp < lowest_timestamp:
    lowest_timestamp = gamedata.timestamp

  if gamedata.timestamp > highest_timestamp:
    highest_timestamp = gamedata.timestamp

print "Buffers date range: [" + datetime.datetime.fromtimestamp(lowest_timestamp).strftime("%c") + "] to [" + datetime.datetime.fromtimestamp(highest_timestamp).strftime("%c") + "]"

start_archive_time = time.time()

print "Archiving..."

tar = tarfile.open(args.archive[0] + "/data-archive-" + str(time.time()) + ".tgz", "w:gz")
for file in f:
  tar.add(args.input[0] + "/" + file)

tar.close()

print "Cleaning up archived files..."

for file in f:
  os.remove(args.input[0] + "/" + file)

end_time = time.time()

print "Skipped " + str(skipped) + " bad files."

print "Finished in " + (str)(end_time - start_time) + " seconds."
print "Opening: " + (str)(start_store_time - start_time) + " seconds."
print "Storing: " + (str)(start_archive_time - start_store_time) + " seconds."
print "Archiving: " + (str)(end_time - start_archive_time) + " seconds."
