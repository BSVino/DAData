#!/usr/bin/python

import argparse
import os
import time
import sys
import re
import operator
import datetime

import dadb

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
location = [0]

one_hour = 60 * 60
one_day = one_hour * 24
one_week = one_day * 7
one_month = one_day * 30

maps_days = 90
maps_days_ago = time.time() - one_day * maps_days

top_ten = 10

map_popularity_periods = 25
weekday_players_periods = 105
timeofday_players_periods = 90

latest_timestamp = 0

recent_maps = {}
past_maps = {}

total_seconds = []
hours_of_the_day = []

for i in range(0, 24):
  hours_of_the_day.append(0)

while location[0] < len(database):
  read = read + 1

  buffer = dadb.db_read_next(database, location)

  if buffer == None:
    skipped += 1
    continue

  if buffer.timestamp == 0:
    continue

  if buffer.timestamp > latest_timestamp:
    latest_timestamp = buffer.timestamp

  days_ago = int((time.time() - buffer.timestamp)/one_day)
  weeks_ago = int((time.time() - buffer.timestamp)/one_week)

  while days_ago >= len(total_seconds):
    total_seconds.append(-1) # -1 means no data for that day.

  # Do this before the continue's below. We collected data from this day even if nobody showed up.
  if total_seconds[days_ago] == -1:
    total_seconds[days_ago] = 0

  if buffer.debug or buffer.cheats:
    continue

  if len(buffer.map_name) == 0:
    continue

  if re.match('^[\w_]+$', buffer.map_name) is None:
    continue

  if buffer.map_name == "dablogomenu":
    continue

  player_seconds = 0

  if buffer.HasField("thirdperson_active"):
    if buffer.HasField("da_version") and buffer.da_version >= 3:
      player_seconds = buffer.thirdperson_active + buffer.thirdperson_inactive
    else:
      player_seconds = (buffer.thirdperson_active + buffer.thirdperson_inactive) * 10
  else:
    player_seconds = len(buffer.positions.position) * 10

  total_seconds[days_ago] += player_seconds

  if weeks_ago < map_popularity_periods:
    if not buffer.map_name in past_maps:
      past_maps[buffer.map_name] = {}

      # Make sure we have all past 50 weeks initialized so there are no gaps.
      for i in range(0, map_popularity_periods):
        past_maps[buffer.map_name][i] = 0

    past_maps[buffer.map_name][weeks_ago] += player_seconds

  if buffer.timestamp > maps_days_ago:
    if not buffer.map_name in recent_maps:
      recent_maps[buffer.map_name] = 0

    recent_maps[buffer.map_name] += player_seconds

  if buffer.timestamp > time.time() - timeofday_players_periods * one_day:
    # What hour is it now?
    day = buffer.timestamp - buffer.timestamp % one_day;
    single_day = buffer.timestamp - day;
    hour = int(single_day / one_hour);

    hours_of_the_day[hour] += player_seconds

print "Crunched " + str(read) + " buffers. There were " + str(skipped) + " bad buffers."
print 
print "Doing post processing..."

# Sort the list of recent maps by popularity
sorted_recent_maps = sorted(recent_maps.iteritems(), key=operator.itemgetter(1))

# We only want the top ten most played maps, truncate the list if there are more
if len(sorted_recent_maps) > top_ten:
  sorted_recent_maps = sorted_recent_maps[-top_ten:]

past_maps['Other'] = {}
for i in range(0, map_popularity_periods):
  past_maps['Other'][i] = 0

total_map_seconds = []
for i in range(0, map_popularity_periods):
  total_map_seconds.append(0)

for map in past_maps:
  found = False

  for entry in sorted_recent_maps:
    if entry[0] == map:
      found = True
      break

  if map != 'Other':
    # total_map_seconds is used to null out weeks where there is no data to make the graph look nicer
    for i in range(0, map_popularity_periods):
      total_map_seconds[i] += past_maps[map][i]

  # If this map is not in the top 10 most popular maps, move it into the "Other" category
  if not found:
    for i in range(0, map_popularity_periods):
      past_maps['Other'][i] += past_maps[map][i]

    past_maps[map]['ignore'] = 1

del past_maps['Other']['ignore']

#Calculate players by day of the week.
weekly_players = []
for i in range(0, 7):
  weekly_players.append(0)

for i in range(0, min(len(total_seconds), weekday_players_periods)):
  today_timestamp = int(time.time() - i * one_day)

  day = int(datetime.datetime.fromtimestamp(today_timestamp).strftime('%w'))

  if day < 0 or day >= 7:
    print "Invalid day of the week: " + day

  # It can be -1 if we have no data!
  if total_seconds[i] > 0:
    weekly_players[day] += total_seconds[i]

weekly_players_total = 0
for i in weekly_players:
  weekly_players_total += i

hourly_players_total = 0
for i in hours_of_the_day:
  hourly_players_total += i

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



## PLAYER MINUTES OVER TIME ##
data = ""
for i in range(0, len(total_seconds)):
  today_index = len(total_seconds) - i - 1
  today_timestamp = int(time.time() - (len(total_seconds) - i) * one_day) * 1000

  if total_seconds[today_index] == -1:
    data = data + '\n[' + str(today_timestamp) + ', null], '
  else:
    data = data + '\n[' + str(today_timestamp) + ', ' + str(float(total_seconds[today_index])/60/60) + '], '

data = data[:-2]

f.write('<div class="chart" id="player_hours"></div>')
f.write("""
<script>
$(function() {

    // Create the chart
    $('#player_hours').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#player_hours').width() > 480
        },

        title : {
            text : 'Player Hours Per Day'
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: ({point.y} player hours)<br/>'
        },

        plotOptions: {
          area: { lineWidth: 1 }
        },

        series : [{
            name : 'Player Hours',
            type: 'area',
            data : [""" + data + """],
            tooltip: {
                valueDecimals: 2
            },
            fillColor : {
              linearGradient : {
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1
               },
               stops : [
                 [0, Highcharts.getOptions().colors[0]],
                 [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
               ]
             },
         }]
    });

});
</script>
""")



## TOP 10 POPULAR MAPS ##

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
            text: 'Top """ + str(top_ten) + """ Most Popular Maps'
        },
        subtitle: {
            text: 'Last """ + str(maps_days) + """ Days'
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



## POPULAR MAPS OVER TIME ##

past_weeks = range(0, map_popularity_periods)
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
    if total_map_seconds[map_popularity_periods-n-1] == 0:
      series = series + 'null, '
    else:
      series = series + str(past_maps[map_name][map_popularity_periods-n-1]/60) + ', '

  series = series[:-2] + ']}, '

series = series[:-2]

f.write('<div class="chart" id="maps_over_time"></div>')
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
                    lineWidth: 0.3,
                    marker: {
                        enabled: false
                    }
                }
            },
            series: [""" + series + """]
        });
    });
</script>
""")



## PLAYERS BY WEEKDAY ##

days_week_list = ""
for day in weekly_players:
  days_week_list = days_week_list + str(float(day)/weekly_players_total) + ", "

days_week_list = days_week_list[:-2]

f.write('<div class="chart" id="players_by_weekday"></div>')
f.write("""
<script>
$(function () {
   $('#players_by_weekday').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Number of Players by Day of the Week'
        },
        subtitle: {
            text: 'Last """ + str(int(weekday_players_periods/7)) + """ Weeks'
        },
        xAxis: {
            categories: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        },
        yAxis: {
            title: {
                text: 'Percentage of Player Minutes'
            }
        },
        series: [{
            showInLegend: false,
            data: [""" + days_week_list + """]
        }]
    });
});
</script>
""")



## PLAYERS BY HOUR ##

hours_day_list = ""
for hour in hours_of_the_day:
  hours_day_list = hours_day_list + str(float(hour)/hourly_players_total) + ", "

hours_day_list = hours_day_list[:-2]

hours_day_labels = ""

f.write('<div class="chart" id="players_by_hour"></div>')
f.write("""
<script>
$(function () {
        $('#players_by_hour').highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Players by Hour of the Day'
            },
            subtitle: {
                text: 'Last """ + str(timeofday_players_periods) + """ Days'
            },
            xAxis: {
                categories: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'Percentage of Player Minutes'
                }
            },
            plotOptions: {
                area: {
                    stacking: 'percent',
                    lineColor: '#ffffff',
                    lineWidth: 0.3,
                    marker: {
                        enabled: false
                    }
                }
            },
            series: [{
              showInLegend: false,
              data: [""" + hours_day_list + """]
            }]
        });
    });
</script>
""")



f.write("<div id='lastupdated'>Last updated " + datetime.datetime.fromtimestamp(time.time()).strftime('%d %B %Y at %H:%M') + ", latest data " + datetime.datetime.fromtimestamp(latest_timestamp).strftime('%d %B %Y at %H:%M') + "</div>\n")

f.write(footer)
f.close()

end_time = time.time()

print "Finished in " + (str)(end_time - start_time) + " seconds."
print "Crunching: " + (str)(start_generate_time - start_time) + " seconds."
print "Generating: " + (str)(end_time - start_generate_time) + " seconds."
