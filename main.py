#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from downloader import find_station, download_data
from rainprob import importdata, precipreport

stationinfo = find_station("VANCOUVER HARBOUR CS")

print("Station ID: " + stationinfo['station_id'])
print("First Year: " + stationinfo['first_year'])
print("Last Year: " + stationinfo['last_year'])
print("\n")

csvdownload = download_data(
    stationinfo['station_id'],
    stationinfo['first_year'],
    stationinfo['last_year']
    )

weatherdata = importdata(csvdownload)

print("\n")

precipreport(weatherdata)