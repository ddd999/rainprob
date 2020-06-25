#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pandas as pd
import datetime
import time
import os.path

STATIONLIST = 'data/stationlist.csv'

def find_station(searchkey):
    with open(STATIONLIST, 'r') as csv_file:
        station_list = csv.DictReader(csv_file)
       
        station_info = dict()
        
        for row in station_list:
            if row['Name'] == searchkey:
                station_info['station_id'] = row['Station ID']
                station_info['first_year'] = row['First Year']
                station_info['last_year'] = row['Last Year']
        
    return station_info

def download_data(station_id,first_year,last_year):
    number_of_years = (int(last_year) - int(first_year)) + 1
    url_list = []
    
    for i in range(number_of_years):
    
        year = int(first_year) + i
        
        # Build a URL for each year
        url = "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=" + station_id + "&Year=" + str(year) + "&Month=1&Day=14&timeframe=2&submit=Download+Data"
        
        # Create a list of all the URLs we want to download
        url_list.append(url)
        
    # Use Pandas to download the data into a list of DataFrames (one DataFrame for each year)
    print("Downloading data from server...")
    t0 = time.time()
    dfs = [pd.read_csv(url) for url in url_list]
    t1 = time.time()
    print("Downloaded in " + str(round(t1-t0,2)) + " s.")
    
    # Combine all of the DataFrames into a single DataFrame containing every year of data
    df = pd.concat(dfs, ignore_index=True)
    
    # Save the complete dataset to a file, mostly for debugging purposes
    
    out_filename = "out/station" + station_id + "_" + first_year + "-" + last_year
    
    if os.path.isfile(out_filename + ".csv"):
        print("File already exists, making a timestamped copy")
        out_filename = out_filename + "_" + str(datetime.datetime.now())
    
    print("Saving file " + out_filename + ".csv...")
    t0 = time.time()
    df.to_csv(out_filename + ".csv", index = False)
    t1 = time.time()
    print("Saved in " + str(round(t1-t0,2)) + " s.")
    print("Finished!")
    
    out_filename = out_filename + ".csv"
    
    return out_filename
 
    
