#!/usr/bin/python

import argparse
import os
import time
import sys
import datetime
import tarfile

import data_pb2     #Protocol buffer

parser = argparse.ArgumentParser(description="Dump the data of an individual buffer to stdout for debugging purposes.")

parser.add_argument('file', nargs=1, metavar='file', help = 'The buffer file')
parser.add_argument('-z', '--fromtgz', nargs=1, metavar='file', help='Grab the file from this .tgz archive', required=False)

args = parser.parse_args()

if args.fromtgz:
  tar = tarfile.open(args.fromtgz[0], "r:gz")
  tar.extract(args.file[0])

f = open(args.file[0], "rb")
buffer = f.read()
f.close()

if args.fromtgz:
  os.remove(args.file[0])

gamedata = data_pb2.GameData()

try:
  gamedata.ParseFromString(buffer)
except:
  print "Buffer is bad."
  sys.exit()

print "Server: " + gamedata.server_name + " running map: " + gamedata.map_name

da_version = 0
if gamedata.HasField("da_version"):
  print "da_version: " + str(gamedata.da_version)
  da_version = gamedata.da_version

if gamedata.debug:
  print "Debug ON"
else:
  print "Debug OFF"

if gamedata.HasField("cheats"):
  if gamedata.cheats:
    print "Cheats ON"
  else:
    print "Cheats OFF"

if gamedata.HasField("teamplay"):
  if gamedata.teamplay:
    print "Teamplay ON"
  else:
    print "Teamplay OFF"

print "Timestamp: " + str(gamedata.timestamp) + " (" + datetime.datetime.fromtimestamp(gamedata.timestamp).strftime('%c') + ")"
print str(len(gamedata.positions.position)) + " player positions (" + str(len(gamedata.positions.position)*10/60) + " player minutes)"

if gamedata.HasField("kills"):
  print str(len(gamedata.kills.position)) + " player kill positions"

if gamedata.HasField("deaths"):
  print str(len(gamedata.deaths.position)) + " player death positions"

if gamedata.HasField("connections"):
  print str(gamedata.connections) + " player connections"

if gamedata.HasField("disconnections"):
  print str(gamedata.disconnections) + " disconnections"

if gamedata.HasField("unique_players_this_map"):
  print str(gamedata.unique_players_this_map) + " unique players"

if len(gamedata.characters_chosen) and da_version < 1:
  print "Characters chosen is present but corrupt."
elif len(gamedata.characters_chosen) and da_version >= 1:
  print str(len(gamedata.characters_chosen)) + " characters chosen"

if len(gamedata.weapons_chosen):
  if da_version <= 1:
    print str(len(gamedata.weapons_chosen)) + " weapons chosen (may include bots)"
  else:
    print str(len(gamedata.weapons_chosen)) + " weapons chosen"
elif len(gamedata.weapons_chosen_s):
  print str(len(gamedata.weapons_chosen_s)) + " weapons chosen (string)"

if len(gamedata.skills_chosen):
  if da_version <= 1:
    print str(len(gamedata.skills_chosen)) + " skills chosen (may include bots)"
  else:
    print str(len(gamedata.skills_chosen)) + " skills chosen"
elif len(gamedata.skills_chosen_s):
  print str(len(gamedata.skills_chosen_s)) + " skills chosen (string)"

if len(gamedata.votes):
  print str(len(gamedata.votes)) + " votes taken"

if gamedata.HasField("map_time"):
  print "Map time: " + str(gamedata.map_time/60) + " minutes"

if gamedata.HasField("thirdperson_active"):
  print

  if da_version >= 3:
    print str(gamedata.thirdperson_active/60) + " third person player minutes"
  else:
    print str(gamedata.thirdperson_active*10/60) + " third person player minutes"

  if da_version >= 3:
    print str(gamedata.thirdperson_inactive/60) + " first person player minutes"
  else:
    print str(gamedata.thirdperson_inactive*10/60) + " first person player minutes"

if gamedata.HasField("vr_active"):
  print
  print str(gamedata.vr_active/60) + " VR active player minutes"
  print str(gamedata.vr_inactive/60) + " VR inactive player minutes"

if gamedata.HasField("platform_windows"):
  print
  print str(gamedata.platform_windows/60) + " MS Windows player minutes"
  print str(gamedata.platform_linux/60) + " Linux player minutes"
  print str(gamedata.platform_osx/60) + " OSX player minutes"
