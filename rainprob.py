#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pandas as pd

precipdict = {
	"Climate_ID": "XXXXX",
	"Station_Name": "YYYYY",
	"rainy_weekdays": 0,
	"snowy_weekdays": 0,
	
	"rainy_weekend_days": 0,
	"snowy_weekend_days": 0,
	
	"total_weekdays": 0,
	"total_weekend_days": 0,
	
	"first_year": 0,
	"last_year": 0
	}


# Imports historical Environment Canada-formatted weather data from a CSV
# and tallies the number of days with rain and snow, and whether the
# precipitation happened on a weekday or weekend.
def importdata(csv_filename):
	
	with open(csv_filename, 'r') as csv_file:
		df = csv.DictReader(csv_file)
		
		firstrow = next(df)
		
		precipdict['climate_ID'] = firstrow['Climate ID']
		precipdict['station_name'] = firstrow['Station Name']
		
		first_year = int(firstrow['Year'])
		
	
		last_year = 0
		
	
		for row in df:
			date = pd.to_datetime(row['Date/Time'], format='%Y-%m-%d')
			
			if date.year < first_year:
				first_year = date.year
			if date.year > last_year:
				last_year = date.year
	
				
			if date.weekday() < 5:
				# Day is a weekday			
				precipdict['total_weekdays'] += 1
				
				# Tally up rainy and snowy days
				if row['Total Rain (mm)'] and row['Total Rain (mm)'] != '0.0':
					precipdict['rainy_weekdays'] +=1
	
				if row['Total Snow (cm)'] and row['Total Snow (cm)'] != '0.0':
					precipdict['snowy_weekdays'] +=1
	
			else:
				# Day is on a weekend	
				precipdict['total_weekend_days'] +=1
				
				# Tally up rainy and snowy days
				if row['Total Rain (mm)'] and row['Total Rain (mm)'] != '0.0':
					precipdict['rainy_weekend_days'] +=1
	
				if row['Total Snow (cm)'] and row['Total Snow (cm)'] != '0.0':
					precipdict['snowy_weekend_days'] +=1
	
	precipdict['first_year'] = first_year
	precipdict['last_year'] = last_year
	
	return df

def precipreport(csvfile):
	
	weekday_por = round((precipdict['rainy_weekdays'] / precipdict['total_weekdays']) * 100,3)
	
	weekend_por = round((precipdict['rainy_weekend_days'] / precipdict['total_weekend_days']) * 100,3)
	
	rainy_weekdays = precipdict['rainy_weekdays']
	total_weekdays = precipdict['total_weekdays']
	
	rainy_weekend_days = precipdict['rainy_weekend_days']
	total_weekend_days = precipdict['total_weekend_days']
	
	print("The probability of rain at " + precipdict['station_name'] + " is:")
	
	print(str(weekday_por) + "% on a weekday (\u2119 = " + str(rainy_weekdays) + "/" + str(total_weekdays) + ")")
	print(str(weekend_por) + "% on a weekend day (\u2119 = " + str(rainy_weekend_days) + "/" + str(total_weekend_days) + ")")


#weatherdata = importdata('out/station888_1925-2020.csv')
#precipreport(weatherdata)