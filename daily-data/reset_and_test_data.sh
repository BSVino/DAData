#!/bin/bash

rm archive/*
rm data -r
cp data_pristine data -r
rm servers.db

./store.py -i data -d servers.db -a archive