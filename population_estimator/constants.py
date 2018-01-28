#!/usr/bin/env python

"""
Constants used in the population_estimator.py module.
"""

import os

# First and last years in the data set.
FIRST_YEAR = 2010  # Modify if a previous year of data is added.
LAST_YEAR = 2016  # Modify if a future year of data is added.

# Path to CSV files
CSV_PATH = '%s/data/' % (os.path.dirname(__file__))

# Names of the CSV files.
NATION_POP_CSV = (
    '%snation_PEP_%s_PEPANNRES_with_ann.csv' % (CSV_PATH, LAST_YEAR))
REGION_POP_CSV = (
    '%sregion_PEP_%s_PEPANNRES_with_ann.csv' % (CSV_PATH, LAST_YEAR))
DIVISION_POP_CSV = (
    '%sdivision_PEP_%s_PEPANNRES_with_ann.csv' % (CSV_PATH, LAST_YEAR))
STATE_POP_CSV = (
    '%sstate_PEP_%s_PEPANNRES_with_ann.csv' % (CSV_PATH, LAST_YEAR))
COUNTY_POP_CSV = (
    '%scounty_PEP_%s_PEPANNRES_with_ann.csv' % (CSV_PATH, LAST_YEAR))
METRO_POP_CSV = (
    '%smetro_PEP_%s_PEPANNRES_with_ann.csv' % (CSV_PATH, LAST_YEAR))
MICRO_POP_CSV = (
    '%smicro_PEP_%s_PEPANNRES_with_ann.csv' % (CSV_PATH, LAST_YEAR))

# Row number of the header row in the CSV files.
HEADER_ROW_NUM = 2

# Name of the column that contains the geography names in the CSV files.
GEO_KEY = 'Geography'

# Names of the columns that contain the annual population estimates in the CSV
# files.
ANN_POP_EST_KEYS = ['Population Estimate (as of July 1) - %s' %
                    year for year in range(FIRST_YEAR, LAST_YEAR + 1)]

# Main Menu options.
START = 'Start'
QUIT = 'Quit'

# Geographic Divisions Menu options.
NATION = 'Nation'
REGION = 'Region'
DIVISION = 'Division'
STATE = 'State'
COUNTY = 'County'
METRO = 'Metropolitan'
MICRO = 'Micropolitan'

# Population Estimates Menu options.
MOST_RECENT_POP = 'Most Recent Population Estimates'
CAGR = 'Compound Annual Growth Rate Estimates (%s-%s)' % (
       FIRST_YEAR, LAST_YEAR)
PROJECTED_POP = 'Projected Population Estimates for a Given Year'

# Access Data Menu options.
SEARCH = 'Search'
VIEW = 'View'
EXPORT = 'Export'

# Name of the folder that contains the exported files.
EXPORT_FOLDER = '%s/export' % (os.path.dirname(__file__))

# Names of the keys in the dictionary that store thes user's selections.
GEOGRAPHIES = 'Geographies'
GEO_DIVISION = 'Geographic Division'
SORTED_BY = 'Sorted By'
YEAR = 'Year'
SEARCH_GEO = 'Search Geography'
