#!/usr/bin/python

import argparse
import os
import time
import sys
import re
import operator
import datetime

import dadb
import da

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

map_popularity_periods = 20
weekday_players_periods = 105
timeofday_players_periods = 90
characters_chosen_periods = 90
weapons_chosen_periods = 90
skills_chosen_periods = 90
maps_voted_for_periods = 90
votekicked_players_periods = 365

latest_timestamp = 0

recent_maps = {}
past_maps = {}
character_choices = {}
character_choices_recent = {}
weapon_choices = {}
weapon_choices_recent = {}
skill_choices = {}
skill_choices_recent = {}
maps_voted_for = {}
maps_voted_away_from = {}
players_votekicked = {}
da_versions = {}

total_seconds = []
teamplay_seconds = []
thirdperson_seconds = []
hours_of_the_day = []

for i in range(0, 24):
  hours_of_the_day.append(0)

while location[0] < len(database):
  read = read + 1

  buffer = dadb.db_read_next(database, location)

  if buffer == None:
    skipped += 1
    continue

  # If the timestamp is before July 2013 it must be bad because we didn't collect data before then.
  if buffer.timestamp < 1372636800: # July 1 2013
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

  while days_ago >= len(teamplay_seconds):
    teamplay_seconds.append(0)

  while days_ago >= len(thirdperson_seconds):
    thirdperson_seconds.append(0)

  if buffer.debug or buffer.cheats:
    continue

  if len(buffer.map_name) == 0:
    continue

  if re.match('^[\w_]+$', buffer.map_name) is None:
    continue

  if buffer.map_name == "dablogomenu":
    continue

  player_seconds = 0

  da_version = 0
  if buffer.HasField("da_version"):
    da_version = buffer.da_version

  if buffer.HasField("thirdperson_active"):
    if da_version >= 3:
      player_seconds = buffer.thirdperson_active + buffer.thirdperson_inactive
      thirdperson_seconds[days_ago] += buffer.thirdperson_active
    else:
      player_seconds = (buffer.thirdperson_active + buffer.thirdperson_inactive) * 10
      thirdperson_seconds[days_ago] += buffer.thirdperson_active * 10
  else:
    player_seconds = len(buffer.positions.position) * 10

  total_seconds[days_ago] += player_seconds

  if buffer.teamplay:
    teamplay_seconds[days_ago] += player_seconds

  if not da_version in da_versions:
    da_versions[da_version] = []

  while days_ago >= len(da_versions[da_version]):
    da_versions[da_version].append(0)

  da_versions[da_version][days_ago] += player_seconds

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

  # Characters are available in version 1 but they include choices by bots.
  if da_version > 1:
    for character in buffer.characters_chosen:
      # These are the only valid characters, for now.
      if character != 'wish' and character != 'bomber' and character != 'eightball' and character != 'frank':
        continue

      # In version 3, bomber wore the eightball skin
      if da_version == 3 and character == 'bomber':
        character = 'eightball'

      if days_ago < characters_chosen_periods:
        if not character in character_choices_recent:
          character_choices_recent[character] = 0

        character_choices_recent[character] += 1

      if not character in character_choices:
        character_choices[character] = []

      while days_ago >= len(character_choices[character]):
        character_choices[character].append(0)

      character_choices[character][days_ago] += 1

  if da_version >= 1:
    for weapon_name in buffer.weapons_chosen_s:
      if days_ago < weapons_chosen_periods:
        if not weapon_name in weapon_choices_recent:
          weapon_choices_recent[weapon_name] = 0

        weapon_choices_recent[weapon_name] += 1

      if not weapon_name in weapon_choices:
        weapon_choices[weapon_name] = []

      while days_ago >= len(weapon_choices[weapon_name]):
        weapon_choices[weapon_name].append(0)

      weapon_choices[weapon_name][days_ago] += 1

    for weapon in buffer.weapons_chosen:
      weapon_name = da.get_weapon_name(weapon, da_version)

      if days_ago < weapons_chosen_periods:
        if not weapon_name in weapon_choices_recent:
          weapon_choices_recent[weapon_name] = 0

        weapon_choices_recent[weapon_name] += 1

      if not weapon_name in weapon_choices:
        weapon_choices[weapon_name] = []

      while days_ago >= len(weapon_choices[weapon_name]):
        weapon_choices[weapon_name].append(0)

      weapon_choices[weapon_name][days_ago] += 1

  if da_version >= 1:
    for skill_name in buffer.skills_chosen_s:
      if days_ago < skills_chosen_periods:
        if not skill_name in skill_choices_recent:
          skill_choices_recent[skill_name] = 0

        skill_choices_recent[skill_name] += 1

      if not skill_name in skill_choices:
        skill_choices[skill_name] = []

      while days_ago >= len(skill_choices[skill_name]):
        skill_choices[skill_name].append(0)

      skill_choices[skill_name][days_ago] += 1

    for skill in buffer.skills_chosen:
      skill_name = da.get_skill_name(skill, da_version)

      if days_ago < skills_chosen_periods:
        if not skill_name in skill_choices_recent:
          skill_choices_recent[skill_name] = 0

        skill_choices_recent[skill_name] += 1

      if not skill_name in skill_choices:
        skill_choices[skill_name] = []

      while days_ago >= len(skill_choices[skill_name]):
        skill_choices[skill_name].append(0)

      skill_choices[skill_name][days_ago] += 1

  if da_version >= 1:
    for vote in buffer.votes:
      if days_ago < maps_voted_for_periods:
        if (vote.issue == 'changelevel' or vote.issue == 'nextlevel') and vote.result == True:
          if not vote.details in maps_voted_for:
            maps_voted_for[vote.details] = 0

          maps_voted_for[vote.details] += 1

          if vote.issue == 'changelevel':
            if not buffer.map_name in maps_voted_away_from:
              maps_voted_away_from[buffer.map_name] = 0

            maps_voted_away_from[buffer.map_name] += 1

      if days_ago < votekicked_players_periods:
        if vote.issue == 'kick' and vote.result == True:
          # Ignore bot kicks
          if re.match('^.*\(BOT\)$', vote.details) != None:
            continue

          match = re.match('^(.*) \(Account id: ([0-9]+)\)$', vote.details)
          player_name = match.groups()[0]
          player_id = match.groups()[1]
          if not player_id in players_votekicked:
            players_votekicked[player_id] = {}

          if not player_name in players_votekicked[player_id]:
            players_votekicked[player_id][player_name] = 0

          if not 0 in players_votekicked[player_id]:
            players_votekicked[player_id][0] = 0 # Stands for the total times kicked. Not a string so that players can't name themselves that to mess with this code

          players_votekicked[player_id][player_name] += 1
          players_votekicked[player_id][0] += 1

print "Crunched " + str(read) + " buffers. There were " + str(skipped) + " bad buffers."
print 
print "Doing post processing..."

# Sort the list of recent maps by popularity
sorted_recent_maps = sorted(recent_maps.iteritems(), key=operator.itemgetter(1))
sorted_voted_for_maps = sorted(maps_voted_for.iteritems(), key=operator.itemgetter(1))
sorted_voted_away_from_maps = sorted(maps_voted_away_from.iteritems(), key=operator.itemgetter(1))
sorted_votekicked_players = sorted(players_votekicked.iteritems(), key=operator.itemgetter(1)) # This one doesn't actually sort it, it just quickly flattens the dictionary
sorted_votekicked_players.sort(key=lambda e: e[1][0]) # Now it's sorted.

# We only want the top ten most played maps, truncate the list if there are more
if len(sorted_recent_maps) > top_ten:
  sorted_recent_maps = sorted_recent_maps[-top_ten:]

if len(sorted_voted_for_maps) > top_ten:
  sorted_voted_for_maps = sorted_voted_for_maps[-top_ten:]

if len(sorted_voted_away_from_maps) > top_ten:
  sorted_voted_away_from_maps = sorted_voted_away_from_maps[-top_ten:]

if len(sorted_votekicked_players) > top_ten:
  sorted_votekicked_players = sorted_votekicked_players[-top_ten:]

sorted_recent_maps.reverse()
sorted_voted_for_maps.reverse()
sorted_voted_away_from_maps.reverse()
sorted_votekicked_players.reverse()

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

if not 'bomber' in character_choices:
  character_choices['bomber'] = []

longest_character = 0

# Make sure all character choices have the same data time points
for character in character_choices:
  longest_character = max(longest_character, len(character_choices[character]))

for character in character_choices:
  while longest_character >= len(character_choices[character]):
    character_choices[character].append(0)

# And weapons
longest_weapon = 0

for weapon in weapon_choices:
  longest_weapon = max(longest_weapon, len(weapon_choices[weapon]))

for weapon in weapon_choices:
  while longest_weapon >= len(weapon_choices[weapon]):
    weapon_choices[weapon].append(0)

# And skills
longest_skill = 0

for skill in skill_choices:
  longest_skill = max(longest_skill, len(skill_choices[skill]))

for skill in skill_choices:
  while longest_skill >= len(skill_choices[skill]):
    skill_choices[skill].append(0)

# And versions
longest_version = 0

for version in da_versions:
  longest_version = max(longest_version, len(da_versions[version]))

for version in da_versions:
  while longest_version >= len(da_versions[version]):
    da_versions[version].append(0)

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
  today_timestamp = int(start_time - (len(total_seconds) - i) * one_day)

  # We don't have any data from before July 2013 because that's when the tracking started, so omit whatever's before that, assume it's bad data
  if today_timestamp < 1372636800: # July 1 2013
    continue

  today_timestamp_millis = today_timestamp * 1000

  if total_seconds[today_index] == -1:
    data = data + '[' + str(today_timestamp_millis) + ', null], '
  else:
    data = data + '[' + str(today_timestamp_millis) + ', ' + str(float(total_seconds[today_index])/60/60) + '], '

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
  maps_played_list = maps_played_list + str(float(map[1])/60/60) + ", "

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
                text: 'Player hours'
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
  weeks = weeks + "'" + datetime.datetime.fromtimestamp(start_time - i * one_week).strftime('%d %b') + "', "

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
      series = series + str(float(past_maps[map_name][map_popularity_periods-n-1])/60/60) + ', '

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
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.percentage:.1f}%</b> ({point.y:,.1f} player hours)<br/>',
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



## POPULAR MAPS VOTED FOR ##

data = ""
categories = ""
for map in sorted_voted_for_maps:
  categories = categories + "'" + map[0] + "', "
  data = data + str(map[1]) + ", "

categories = categories[:-2]
data = data[:-2]

f.write('<div class="chart" id="maps_voted_for"></div>')
f.write("""
<script>
$(function () {
   $('#maps_voted_for').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Top """ + str(top_ten) + """ Successful Map Votes'
        },
        subtitle: {
            text: 'Last """ + str(int(maps_voted_for_periods)) + """ Days'
        },
        xAxis: {
            categories: [""" + categories + """]
        },
        yAxis: {
            title: {
                text: 'Times Chosen'
            }
        },
        series: [{
            showInLegend: false,
            data: [""" + data + """]
        }]
    });
});
</script>
""")



## MAPS VOTED AWAY FROM ##

data = ""
categories = ""
for map in sorted_voted_away_from_maps:
  categories = categories + "'" + map[0] + "', "
  data = data + str(map[1]) + ", "

categories = categories[:-2]
data = data[:-2]

f.write('<div class="chart" id="maps_voted_away_from"></div>')
f.write("""
<script>
$(function () {
   $('#maps_voted_away_from').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Top """ + str(top_ten) + """ Maps Voted Away From'
        },
        subtitle: {
            text: 'Last """ + str(int(maps_voted_for_periods)) + """ Days'
        },
        xAxis: {
            categories: [""" + categories + """]
        },
        yAxis: {
            title: {
                text: 'Times Voted Away From'
            }
        },
        series: [{
            showInLegend: false,
            data: [""" + data + """]
        }]
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
                    text: 'Hour (UTC)'
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



## CHARACTERS CHOSEN OVER TIME ##

def build_character_data(character_choices):
  char_data = ""
  for i in range(0, len(character_choices)):
    today_index = len(character_choices) - i - 1
    today_timestamp = int(start_time - (len(character_choices) - i) * one_day)

    today_timestamp_millis = today_timestamp * 1000

    char_data = char_data + '[' + str(today_timestamp_millis) + ', ' + str(float(character_choices[today_index])) + '], '

  char_data = char_data[:-2]

  return char_data

frank_data = ""
wish_data = ""
eightball_data = ""
bomber_data = ""

if 'frank' in character_choices:
  frank_data = build_character_data(character_choices['frank'])

if 'wish' in character_choices:
  wish_data = build_character_data(character_choices['wish'])

if 'eightball' in character_choices:
  eightball_data = build_character_data(character_choices['eightball'])

if 'bomber' in character_choices:
  bomber_data = build_character_data(character_choices['bomber'])

f.write('<div class="chart" id="characters_chosen_history"></div>')
f.write("""
<script>
$(function() {

    // Create the chart
    $('#characters_chosen_history').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#characters_chosen_history').width() > 480
        },

        title : {
            text : 'Characters Chosen'
        },

        legend: {
          enabled: true
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: (Chosen {point.y} times)<br/>'
        },

        plotOptions: {
          area: {
            stacking: 'percent',
            lineWidth: 1
          }
        },

        series : [{
            name : 'Vice',
            color: '#818eb7',
            type: 'area',
            data : [""" + wish_data + """],
            tooltip: {
                valueDecimals: 2
            },
            fillColor : {
              linearGradient : { x1: 0, y1: 0, x2: 0, y2: 1 },
               stops : [
                 [0, '#c4cce5'],
                 [1, '#5c71b7']
               ]
            }
         }, {
            name : 'Diesel',
            color: '#666666',
            type: 'area',
            data : [""" + frank_data + """],
            tooltip: {
                valueDecimals: 2
            },
            fillColor : {
              linearGradient : { x1: 0, y1: 0, x2: 0, y2: 1 },
               stops : [
                 [0, '#202020'],
                 [1, '#59668f']
               ]
            }
         }, {
            name : 'Eightball',
            color: '#94534a',
            type: 'area',
            data : [""" + eightball_data + """],
            tooltip: {
                valueDecimals: 2
            },
            fillColor : {
              linearGradient : { x1: 0, y1: 0, x2: 0, y2: 1 },
               stops : [
                 [0, '#94534a'],
                 [1, '#943629']
               ]
            }
         }, {
            name : 'Bomber',
            color: '#634816',
            type: 'area',
            data : [""" + bomber_data + """],
            tooltip: {
                valueDecimals: 2
            },
            fillColor : {
              linearGradient : { x1: 0, y1: 0, x2: 0, y2: 1 },
               stops : [
                 [0, '#634816'],
                 [1, '#947438']
               ]
            }
         }]
    });

});
</script>
""")



## POPULAR CHARACTERS CHOSEN ##

data = ""
categories = ""
for character in character_choices_recent:
  categories = categories + "'" + da.get_character_print_name(character) + "', "
  data = data + str(character_choices_recent[character]) + ", "

categories = categories[:-2]
data = data[:-2]

f.write('<div class="chart" id="characters_chosen"></div>')
f.write("""
<script>
$(function () {
   $('#characters_chosen').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Total Characters Chosen'
        },
        subtitle: {
            text: 'Last """ + str(int(characters_chosen_periods)) + """ Days'
        },
        xAxis: {
            categories: [""" + categories + """]
        },
        yAxis: {
            title: {
                text: 'Times Chosen'
            }
        },
        series: [{
            showInLegend: false,
            data: [""" + data + """]
        }]
    });
});
</script>
""")



## WEAPONS CHOSEN OVER TIME ##

data = ""

for weapon in weapon_choices:
  data = data + """{
            name : '""" + da.get_weapon_print_name(weapon) + """',
            type: 'area',
            data : ["""

  for i in range(0, len(weapon_choices[weapon])):
    today_index = len(weapon_choices[weapon]) - i - 1
    today_timestamp = int(start_time - (len(weapon_choices[weapon]) - i) * one_day)

    today_timestamp_millis = today_timestamp * 1000

    data = data + '[' + str(today_timestamp_millis) + ', ' + str(float(weapon_choices[weapon][today_index])) + '], '

  data = data + """],
            tooltip: {
                valueDecimals: 2
            }
         }, """

data = data[:-2]

f.write('<div class="tallchart" id="weapons_chosen_history"></div>')
f.write("""
<script>
$(function() {

    // Create the chart
    $('#weapons_chosen_history').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#weapons_chosen_history').width() > 480
        },

        title : {
            text : 'Weapons Chosen'
        },

        legend: {
          enabled: true
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: (Chosen {point.y} times)<br/>'
        },

        plotOptions: {
          area: {
            stacking: 'percent',
            lineWidth: 1
          }
        },

        series : [""" + data + """]
    });

});
</script>
""")



## POPULAR WEAPONS CHOSEN ##

data = ""
categories = ""
for weapon in weapon_choices_recent:
  categories = categories + "'" + da.get_weapon_print_name(weapon) + "', "
  data = data + str(weapon_choices_recent[weapon]) + ", "

categories = categories[:-2]
data = data[:-2]

f.write('<div class="chart" id="weapons_chosen"></div>')
f.write("""
<script>
$(function () {
   $('#weapons_chosen').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Total Weapons Chosen'
        },
        subtitle: {
            text: 'Last """ + str(int(weapons_chosen_periods)) + """ Days'
        },
        xAxis: {
            categories: [""" + categories + """]
        },
        yAxis: {
            title: {
                text: 'Times Chosen'
            }
        },
        series: [{
            showInLegend: false,
            data: [""" + data + """]
        }]
    });
});
</script>
""")



## SKILLS CHOSEN OVER TIME ##

data = ""

for skill in skill_choices:
  data = data + """{
            name : '""" + da.get_skill_print_name(skill) + """',
            type: 'area',
            data : ["""

  for i in range(0, len(skill_choices[skill])):
    today_index = len(skill_choices[skill]) - i - 1
    today_timestamp = int(start_time - (len(skill_choices[skill]) - i) * one_day)

    today_timestamp_millis = today_timestamp * 1000

    data = data + '[' + str(today_timestamp_millis) + ', ' + str(float(skill_choices[skill][today_index])) + '], '

  data = data + """],
            tooltip: {
                valueDecimals: 2
            }
         }, """

data = data[:-2]

f.write('<div class="tallchart" id="skills_chosen_history"></div>')
f.write("""
<script>
$(function() {

    // Create the chart
    $('#skills_chosen_history').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#skills_chosen_history').width() > 480
        },

        title : {
            text : 'Skills Chosen'
        },

        legend: {
          enabled: true
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: (Chosen {point.y} times)<br/>'
        },

        plotOptions: {
          area: {
            stacking: 'percent',
            lineWidth: 1
          }
        },

        series : [""" + data + """]
    });

});
</script>
""")



## POPULAR SKILLS CHOSEN ##

data = ""
categories = ""
for skill in skill_choices_recent:
  categories = categories + "'" + da.get_skill_print_name(skill) + "', "
  data = data + str(skill_choices_recent[skill]) + ", "

categories = categories[:-2]
data = data[:-2]

f.write('<div class="chart" id="skills_chosen"></div>')
f.write("""
<script>
$(function () {
   $('#skills_chosen').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Total Skills Chosen'
        },
        subtitle: {
            text: 'Last """ + str(int(skills_chosen_periods)) + """ Days'
        },
        xAxis: {
            categories: [""" + categories + """]
        },
        yAxis: {
            title: {
                text: 'Times Chosen'
            }
        },
        series: [{
            showInLegend: false,
            data: [""" + data + """]
        }]
    });
});
</script>
""")



## MOST VOTEKICKED PLAYERS ##

data = ""
categories = ""
for player in sorted_votekicked_players:
  data = data + str(player[1][0]) + ", "

  del player[1][0]

  sorted_names = sorted(player[1].iteritems(), key=operator.itemgetter(1), reverse=True)

  clean_name = re.sub(r'\W+', '_', sorted_names[0][0])

  categories = categories + "'" + clean_name + " (ID: " + player[0] + ")', "

categories = categories[:-2]
data = data[:-2]

f.write('<div class="chart" id="votekicked_players"></div>')
f.write("""
<script>
$(function () {
   $('#votekicked_players').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Top """ + str(top_ten) + """ Vote-Kicked Players'
        },
        subtitle: {
            text: 'Last """ + str(int(votekicked_players_periods)) + """ Days'
        },
        xAxis: {
            categories: [""" + categories + """]
        },
        yAxis: {
            title: {
                text: 'Times Vote-Kicked'
            }
        },
        series: [{
            showInLegend: false,
            data: [""" + data + """]
        }]
    });
});
</script>
""")



## TEAMPLAY OVER TIME ##

dm_data = ""
tdm_data = ""
for i in range(0, len(total_seconds)):
  today_index = len(total_seconds) - i - 1
  today_timestamp = int(start_time - (len(total_seconds) - i) * one_day)

  # We didn't track teamplay before Epsilon, so don't bother looking at data older
  if today_timestamp < 1386460800 : # December 8 2013
    continue

  today_timestamp_millis = today_timestamp * 1000

  if total_seconds[today_index] <= 0:
    dm_data = dm_data + '[' + str(today_timestamp_millis) + ', null], '
    tdm_data = tdm_data + '[' + str(today_timestamp_millis) + ', null], '
  else:
    dm_data = dm_data + '[' + str(today_timestamp_millis) + ', ' + str(1-float(teamplay_seconds[today_index])/total_seconds[today_index]) + '], '
    tdm_data = tdm_data + '[' + str(today_timestamp_millis) + ', ' + str(float(teamplay_seconds[today_index])/total_seconds[today_index]) + '], '

dm_data = dm_data[:-2]
tdm_data = tdm_data[:-2]

f.write('<div class="chart" id="teamplay_history"></div>')
f.write("""
<script>
$(function() {

    // Create the chart
    $('#teamplay_history').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#teamplay_history').width() > 480
        },

        title : {
            text : 'Teamplay'
        },

        legend: {
          enabled: true
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: ({point.y})<br/>'
        },

        plotOptions: {
          area: {
            stacking: 'percent',
            lineWidth: 1
          }
        },

        series : [{
            name : 'Deathmatch',
            color: '#94534a',
            type: 'area',
            data : [""" + dm_data + """],
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
                 [0, '#94534a'],
                 [1, '#943629']
               ]
             },
         }, {
            name : 'Team Deathmatch',
            color: '#c4cce5',
            type: 'area',
            data : [""" + tdm_data + """],
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
                 [0, '#c4cce5'],
                 [1, '#5c71b7']
               ]
             },
         }]
    });

});
</script>
""")



## THIRD PERSON OVER TIME ##

tp_data = ""
fp_data = ""
for i in range(0, len(total_seconds)):
  today_index = len(total_seconds) - i - 1
  today_timestamp = int(start_time - (len(total_seconds) - i) * one_day)

  # We didn't track third person before Epsilon, so don't bother looking at data older
  if today_timestamp < 1386460800 : # December 8 2013
    continue

  today_timestamp_millis = today_timestamp * 1000

  if total_seconds[today_index] <= 0:
    tp_data = tp_data + '[' + str(today_timestamp_millis) + ', null], '
    fp_data = fp_data + '[' + str(today_timestamp_millis) + ', null], '
  else:
    tp_data = tp_data + '[' + str(today_timestamp_millis) + ', ' + str(float(thirdperson_seconds[today_index])/total_seconds[today_index]) + '], '
    fp_data = fp_data + '[' + str(today_timestamp_millis) + ', ' + str(1-float(thirdperson_seconds[today_index])/total_seconds[today_index]) + '], '

tp_data = tp_data[:-2]
fp_data = fp_data[:-2]

f.write('<div class="chart" id="thirdperson_history"></div>')
f.write("""
<script>
$(function() {

    // Create the chart
    $('#thirdperson_history').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#thirdperson_history').width() > 480
        },

        title : {
            text : 'Third Person vs First Person'
        },

        legend: {
          enabled: true
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: ({point.y})<br/>'
        },

        plotOptions: {
          area: {
            stacking: 'percent',
            lineWidth: 1
          }
        },

        series : [{
            name : 'Third Person',
            type: 'area',
            data : [""" + tp_data + """],
            tooltip: {
                valueDecimals: 2
            }
         }, {
            name : 'First Person',
            type: 'area',
            data : [""" + fp_data + """],
            tooltip: {
                valueDecimals: 2
            }
         }]
    });

});
</script>
""")



## VERSION ADOPTION ##

data = ""

for version in da_versions:
  data = data + """{
            name : '""" + da.get_da_version_name(version) + """',
            type: 'area',
            data : ["""

  for i in range(0, len(da_versions[version])):
    today_index = len(da_versions[version]) - i - 1
    today_timestamp = int(start_time - (len(da_versions[version]) - i) * one_day)

    today_timestamp_millis = today_timestamp * 1000

    data = data + '[' + str(today_timestamp_millis) + ', ' + str(float(da_versions[version][today_index])/60/60) + '], '

  data = data + """],
            tooltip: {
                valueDecimals: 2
            }
         }, """

data = data[:-2]

f.write('<div class="chart" id="version_adoption"></div>')
f.write("""
<script>
$(function() {

    // Create the chart
    $('#version_adoption').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#version_adoption').width() > 480
        },

        legend: {
          enabled: true
        },

        title : {
            text : 'Version Adoption'
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: ({point.y} player hours)<br/>'
        },

        plotOptions: {
          area: {
            stacking: 'percent',
            lineWidth: 1
          }
        },

        series : [""" + data + """]
    });

});
</script>
""")



## REVENUE IN DOLLARS ##

data = ""
for i in range(0, len(total_seconds)):
  today_index = len(total_seconds) - i - 1
  today_timestamp = int(start_time - (len(total_seconds) - i) * one_day)

  today_timestamp_millis = today_timestamp * 1000

  # We don't have any data from before July 2013 because that's when the tracking started, so omit whatever's before that, assume it's bad data
  if today_timestamp < 1372636800: # July 1 2013
    continue

  data = data + '[' + str(today_timestamp_millis) + ', 0], '

data = data[:-2]

f.write("""<div class="chart" id="revenue_dollars"></div>
<script>
$(function() {

    // Create the chart
    $('#revenue_dollars').highcharts('StockChart', {

        rangeSelector : {
            selected : 1,
            inputEnabled: $('#revenue_dollars').width() > 480
        },

        title : {
            text : 'Daily Revenue'
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: (${point.y})<br/>'
        },

        plotOptions: {
          area: { lineWidth: 1 }
        },

        series : [{
            name : 'Revenue',
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



f.write("<div id='lastupdated'>Last updated " + datetime.datetime.fromtimestamp(start_time).strftime('%d %B %Y at %H:%M') + ", latest data " + datetime.datetime.fromtimestamp(latest_timestamp).strftime('%d %B %Y at %H:%M') + "</div>\n")

f.write(footer)
f.close()

end_time = time.time()

print "Finished in " + (str)(end_time - start_time) + " seconds."
print "Crunching: " + (str)(start_generate_time - start_time) + " seconds."
print "Generating: " + (str)(end_time - start_generate_time) + " seconds."
