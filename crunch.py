#!/usr/bin/python

import struct
import argparse
import os
import time
import sys
import re
import operator

import data_pb2     #Protocol buffer

parser = argparse.ArgumentParser(description="Crunch Double Action data, generate a static webpage.")

parser.add_argument('-d', '--database', nargs=1, metavar='file', help = 'The database file', required=True)
parser.add_argument('-ht', '--html', nargs=1, metavar='directory', help='The html template files location', required=True)
parser.add_argument('-o', '--output', nargs=1, metavar='directory', help='The output directory to place the results', required=True)

args = parser.parse_args()

start_time = time.time()

print "Reading database..."

f = open(args.database[0], "rb")
database = f.read()
f.close()

read = 0
skipped = 0
location = 0

buffers = []

while location < len(database):
  read = read + 1

  # First we packed a four byte length of the next buffer
  length = struct.unpack('L', database[location:location+struct.calcsize('L')])[0]

  # Advance the location four bytes, now location points to the buffer itself
  location = location + struct.calcsize('L')

  gamedata = data_pb2.GameData()

  # Advance to the next location now in case there's a bad buffer
  location = location + length

  try:
    gamedata.ParseFromString(database[location-length:location])
  except:
    skipped = skipped + 1
    continue

  buffers.append(gamedata)

print "Read " + str(read) + " buffers. There were " + str(skipped) + " bad buffers."

start_crunch_time = time.time()

print "Crunching data..."

maps_days = 365
one_month_ago = time.time() - 60 * 60 * 24 * maps_days

recent_maps = {}
for buffer in buffers:
  if buffer.timestamp < one_month_ago:
    continue

  if buffer.debug or buffer.cheats:
    continue

  if len(buffer.map_name) == 0:
    continue

  if re.match('^[\w_]+$', buffer.map_name) is None:
    continue

  if buffer.map_name == "dablogomenu":
    continue

  if not buffer.map_name in recent_maps:
    recent_maps[buffer.map_name] = 0

  recent_maps[buffer.map_name] += 1

sorted_recent_maps = sorted(recent_maps.iteritems(), key=operator.itemgetter(1))

if len(sorted_recent_maps) > 15:
  sorted_recent_maps = sorted_recent_maps[-15:]

start_generate_time = time.time()

f = open(args.html[0] + "/header.html", "r")
header = f.read()
f.close()

f = open(args.html[0] + "/footer.html", "r")
footer = f.read()
f.close()

f = open(args.output[0] + "/index.html", "w")
f.write(header)

maps_list = ""
maps_played_list = ""
for map in sorted_recent_maps:
  if map[1] < 3:
    continue
  maps_list = maps_list + "'" + map[0] + "', "
  maps_played_list = maps_played_list + str(map[1]) + ", "

maps_list = maps_list[:-2]
maps_played_list = maps_played_list[:-2]

f.write('<div id="recent_maps" style="width:100%; height:400px;"></div>')
f.write("""
<script>
$(function () {
   $('#recent_maps').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Popular maps last """ + str(maps_days) + """ days'
        },
        xAxis: {
            categories: [""" + maps_list + """]
        },
        yAxis: {
            title: {
                text: 'Times played'
            }
        },
        series: [{
	    showInLegend: false,
            data: [""" + maps_played_list + """]
        }]
    });
});
</script>
""")

f.write(footer)
f.close()

end_time = time.time()

print "Finished in " + (str)(end_time - start_time) + " seconds."
print "Reading: " + (str)(start_crunch_time - start_time) + " seconds."
print "Crunching: " + (str)(start_generate_time - start_crunch_time) + " seconds."
print "Generating: " + (str)(end_time - start_generate_time) + " seconds."
