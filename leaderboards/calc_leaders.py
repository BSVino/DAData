#!/usr/bin/python

import argparse

import leaderboards

parser = argparse.ArgumentParser(description="Calculate new leaders and output HTML.")

parser.add_argument('-d', '--database', nargs=1, metavar='database_directory', help='The directory containing the lmdb database to store the results', required=True)
parser.add_argument('-l', '--leaderboards', nargs=1, metavar='leaderboards_binary', help='The location of the leaderboards binary', required=True)
parser.add_argument('-o', '--output', nargs=1, metavar='output_directory', help='The directory to output the result html', required=True)

args = parser.parse_args()

leaderboards.calc_leaders(args.database[0], args.leaderboards[0], args.output[0])

