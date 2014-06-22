#!/usr/bin/python

import struct
import argparse
import os
import time
import sys
import re
import operator
import datetime

import data_pb2     #Protocol buffer

parser = argparse.ArgumentParser(description="Crunch Double Action data, generate a static webpage.")

parser.add_argument('-d', '--database', nargs=1, metavar='file', help = 'The database file', required=True)
parser.add_argument('-ht', '--html', nargs=1, metavar='directory', help='The html template files location', required=True)
parser.add_argument('-o', '--output', nargs=1, metavar='directory', help='The output directory to place the results', required=True)

args = parser.parse_args()

start_time = time.time()

print "Crunching database..."

f = open(args.database[0], "rb")
database = f.read()
f.close()

read = 0
skipped = 0
location = 0

one_week = 60 * 60 * 24 * 7
one_month = 60 * 60 * 24 * 30

maps_days = 365
one_month_ago = time.time() - 60 * 60 * 24 * maps_days

top_ten = 10

fifty = 40 # Yeah I know
fifty_weeks_ago = time.time() - one_week * fifty

recent_maps = {}
past_maps = {}

while location < len(database):
  read = read + 1

  # First we packed a four byte length of the next buffer
  length = struct.unpack('L', database[location:location+struct.calcsize('L')])[0]

  # Advance the location four bytes, now location points to the buffer itself
  location = location + struct.calcsize('L')

  buffer = data_pb2.GameData()

  # Advance to the next location now in case there's a bad buffer
  location = location + length

  try:
    buffer.ParseFromString(database[location-length:location])
  except:
    skipped = skipped + 1
    continue

  if buffer.debug or buffer.cheats:
    continue

  if len(buffer.map_name) == 0:
    continue

  if re.match('^[\w_]+$', buffer.map_name) is None:
    continue

  if buffer.map_name == "dablogomenu":
    continue

  player_minutes = len(buffer.positions.position) * 10

  weeks_ago = int((time.time() - buffer.timestamp)/one_week)

  if weeks_ago < fifty:
    if not buffer.map_name in past_maps:
      past_maps[buffer.map_name] = {}

      # Make sure we have all past 50 weeks initialized so there are no gaps.
      for i in range(0, fifty):
	past_maps[buffer.map_name][i] = 0

    past_maps[buffer.map_name][weeks_ago] += player_minutes

  if buffer.timestamp > one_month_ago:
    if not buffer.map_name in recent_maps:
      recent_maps[buffer.map_name] = 0

    recent_maps[buffer.map_name] += player_minutes


print "Crunched " + str(read) + " buffers. There were " + str(skipped) + " bad buffers."

sorted_recent_maps = sorted(recent_maps.iteritems(), key=operator.itemgetter(1))

if len(sorted_recent_maps) > top_ten:
  sorted_recent_maps = sorted_recent_maps[-top_ten:]

past_maps['Other'] = {}
for i in range(0, fifty):
  past_maps['Other'][i] = 0

for map in past_maps:
  found = False

  for entry in sorted_recent_maps:
    if entry[0] == map:
      found = True
      break

  if not found:
    for i in range(0, fifty):
      past_maps['Other'][i] += past_maps[map][i]

    past_maps[map]['ignore'] = 1

del past_maps['Other']['ignore']

start_generate_time = time.time()

print "Generating html..."

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

f.write('<div class="chart" id="recent_maps"></div>')
f.write("""
<script>
$(function () {
   $('#recent_maps').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Top """ + str(top_ten) + """ most popular maps last """ + str(maps_days) + """ days'
        },
        xAxis: {
            categories: [""" + maps_list + """]
        },
        yAxis: {
            title: {
                text: 'Player minutes'
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

past_weeks = range(0, fifty)
past_weeks.reverse()

weeks = ""
for i in past_weeks:
  weeks = weeks + "'" + datetime.datetime.fromtimestamp(time.time() - i * one_week).strftime('%d %b') + "', "

weeks = weeks[:-2]

series = ""
for map_name in past_maps.keys():
  if 'ignore' in past_maps[map_name]:
    continue

  series = series + "{ name: '" + map_name + "', data: ["
  for n in past_maps[map_name]:
    series = series + str(past_maps[map_name][fifty-n-1]) + ', '

  series = series[:-2] + ']}, '

series = series[:-2]

f.write('<div class="chart" id="maps_over_time""></div>')
f.write("""
<script>
$(function () {
        $('#maps_over_time').highcharts({
            chart: {
                type: 'area'
            },
            title: {
                text: 'Map Popularity Over Time'
            },
            xAxis: {
                categories: [""" + weeks + """],
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'Percent'
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.percentage:.1f}%</b> ({point.y:,.0f} player minutes)<br/>',
                shared: true
            },
            plotOptions: {
                area: {
                    stacking: 'percent',
                    lineColor: '#ffffff',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#ffffff'
                    }
                }
            },
            series: [""" + series + """]
        });
    });
</script>
""")

f.write(footer)
f.close()

end_time = time.time()

print "Finished in " + (str)(end_time - start_time) + " seconds."
print "Crunching: " + (str)(start_generate_time - start_time) + " seconds."
print "Generating: " + (str)(end_time - start_generate_time) + " seconds."
