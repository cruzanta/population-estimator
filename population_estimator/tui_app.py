#!/usr/bin/env python


"""
Module for viewing, searching, and exporting the Annual Estimates of the
Resident Population provided by the U.S. Census Bureau, Population Division.
"""

from constants import *
import csv_dicts
import geography
import operator
import curses
import curses_io
import collections
import sys


def get_geographies(csv_dicts):
    # Returns a list of Geography objects.
    geographies = []
    for csv_dict in csv_dicts:
        population_estimates = [int(csv_dict[key]) for key in ANN_POP_EST_KEYS]
        geo = geography.Geography(csv_dict[GEO_KEY], population_estimates)
        geographies.append(geo)

    return geographies


def sort_geographies_by_most_recent_pop(geographies):
    # Returns a list of Geography objects that are sorted by their most recent
    # population estimate attributes in descending order.
    geographies.sort(key=operator.attrgetter('most_recent_pop_est'),
                     reverse=True)


def sort_geographies_by_cagr(geographies):
    # Returns a list of Geography objects that are sorted by their compound
    # annual growth rate attributes in descending order.
    geographies.sort(key=operator.attrgetter('cagr'), reverse=True)


def sort_geographies_by_projected_pop(geographies, year):
    # Returns a list of Geography objects that are sorted by their projected
    # population estimate method return value for a given future year in
    # descending order.
    geographies.sort(key=operator.methodcaller(
        'get_projected_population', LAST_YEAR, year), reverse=True)


def get_geography_dicts(user_selections):
    # Returns a list of dictionaries that contain the name attribute along with
    # a second attribute, or method return value, of each Geography object in a
    # list. The second attribute, or method return value, is determined by the
    # values of the 'user_selections' dict.
    geo_dicts = []
    for geography in user_selections.get(GEOGRAPHIES):
        geo_dict = collections.OrderedDict()
        geo_dict['Geography Name'] = geography.name

        if user_selections.get(SORTED_BY) == MOST_RECENT_POP:
            key = '%s Population Estimate' % (user_selections.get(YEAR))
            geo_dict[key] = geography.most_recent_pop_est
        elif user_selections.get(SORTED_BY) == CAGR:
            key = 'Compound Annual Growth Rate Estimate (%s-%s)' % (FIRST_YEAR,
                                                                    LAST_YEAR)
            geo_dict[key] = '%s%%' % (round(geography.cagr * 100, 2))
        elif user_selections.get(SORTED_BY) == PROJECTED_POP:
            key = '%s Population Estimate' % (user_selections.get(YEAR))
            geo_dict[key] = geography.get_projected_population(
                LAST_YEAR, user_selections.get(YEAR))

        if geography.name == user_selections.get(SEARCH_GEO):
            geo_dicts = [geo_dict]
            break

        else:
            geo_dicts.append(geo_dict)

    return geo_dicts


def get_projected_year_from_user(screen):
    # Returns a future year provided by the user.
    first_line_num = 0
    prompt_heading = ('Please enter a year below. The year must be greater ' +
                      'than %s.' % (LAST_YEAR))
    prompt = 'Year:'

    while True:
        year = curses_io.display_string_with_prompt(screen, first_line_num,
                                                    prompt_heading, prompt)
        try:
            year = int(year)
        except ValueError:
            continue
        if not (year > LAST_YEAR):
            continue
        else:
            break

    return year


def search_for_geography(screen, user_selections):
    # Returns the name of the first geography in a list of geography names that
    # contains all or part of the user-provided search term.
    first_line_num = 0
    prompt_heading = 'Please enter the name of a %s below.' % (
                     user_selections.get(GEO_DIVISION).lower())
    prompt = '%s:' % (user_selections.get(GEO_DIVISION))
    geo_names = [
        geography.name for geography in user_selections.get(GEOGRAPHIES)]

    search_result = ''
    while search_result not in geo_names:
        search_term = curses_io.display_string_with_prompt(screen,
                                                           first_line_num,
                                                           prompt_heading,
                                                           prompt)
        search_result = next(
            (name for name in geo_names if search_term in name), None)

    return search_result


def display_geo_dicts_and_return_to_main_menu(screen, geo_dicts,
                                              user_selections):
    # Displays the key, value pairs of dictionaries in a list until the user
    # chooses to return to the Main Menu.
    first_line_num = 0
    prompt_heading = '%s %s' % (user_selections.get(GEO_DIVISION),
                                user_selections.get(SORTED_BY))
    prompt = 'Enter "r" to return to the Main Menu:'
    return_keys = ['r', 'R']

    return_key = ''
    while return_key not in return_keys:
        return_key = curses_io.display_formatted_dicts_with_prompt(
            screen, first_line_num, prompt_heading, geo_dicts, prompt)


def display_export_success_and_return_to_main_menu(screen, file_name):
    # Displays a message that indicates that a export file has been created
    # until the user chooses to return to the Main Menu.
    first_line_num = 0
    message = ('Success! %s.csv has been created in the following directory: %s'
               % (file_name, EXPORT_FOLDER))
    prompt = 'Enter "r" to return to the Main Menu:'
    return_keys = ['r', 'R']

    return_key = ''
    while return_key not in return_keys:
        return_key = curses_io.display_string_with_prompt(screen,
                                                          first_line_num,
                                                          message, prompt)


def main_menu(screen):
    # Returns True if the user chooses to start the application or False if the
    # user chooses to quit the application.
    first_line_num = 0
    menu_heading = ('Welcome to the Population Estimator! Please select an ' +
                    'option from the menu below.')
    menu_items = [START, QUIT]
    prompt = 'Selection:'

    selection = curses_io.get_user_menu_selection(screen, first_line_num,
                                                  menu_heading, menu_items,
                                                  prompt)
    if selection == START:
        return True
    elif selection == QUIT:
        return False


def geographical_divisions_menu(screen, user_selections):
    # Adds a list of Geography objects to a dictionary that contains the user's
    # selections and returns the dictionary.
    first_line_num = 0
    menu_heading = ('Please select a geographical division from the menu ' +
                    'below.')
    menu_items = [NATION, REGION, DIVISION, STATE, COUNTY, METRO, MICRO]
    prompt = 'Selection:'

    selection = curses_io.get_user_menu_selection(screen, first_line_num,
                                                  menu_heading, menu_items,
                                                  prompt)
    if selection == NATION:
        csv_file = NATION_POP_CSV
    elif selection == REGION:
        csv_file = REGION_POP_CSV
    elif selection == DIVISION:
        csv_file = DIVISION_POP_CSV
    elif selection == STATE:
        csv_file = STATE_POP_CSV
    elif selection == COUNTY:
        csv_file = COUNTY_POP_CSV
    elif selection == METRO:
        csv_file = METRO_POP_CSV
    elif selection == MICRO:
        csv_file = MICRO_POP_CSV

    user_selections[GEOGRAPHIES] = get_geographies(
        csv_dicts.csv_rows_to_dicts(csv_file, HEADER_ROW_NUM))
    user_selections[GEO_DIVISION] = selection

    return user_selections


def population_estimates_menu(screen, user_selections):
    # Sorts a list of Geography objects based on which attribute or method value
    # that the user chooses to sort the objects by and returns a dictionary
    # of user selections containing the sorted list of Geography objects.
    first_line_num = 0
    menu_heading = 'Please select a type of estimate from the menu below.'
    menu_items = [MOST_RECENT_POP, CAGR, PROJECTED_POP]
    prompt = 'Selection:'

    selection = curses_io.get_user_menu_selection(screen, first_line_num,
                                                  menu_heading, menu_items,
                                                  prompt)
    if selection == MOST_RECENT_POP:
        sort_geographies_by_most_recent_pop(user_selections.get(GEOGRAPHIES))
        user_selections[SORTED_BY] = selection
        user_selections[YEAR] = LAST_YEAR
    elif selection == CAGR:
        sort_geographies_by_cagr(user_selections.get(GEOGRAPHIES))
        user_selections[SORTED_BY] = selection
        user_selections[YEAR] = LAST_YEAR
    elif selection == PROJECTED_POP:
        user_selections[YEAR] = get_projected_year_from_user(screen)
        sort_geographies_by_projected_pop(user_selections.get(GEOGRAPHIES),
                                          user_selections.get(YEAR))
        user_selections[SORTED_BY] = selection

    return user_selections


def access_data_menu(screen, user_selections):
    # Allows the user to access each geography's population data by searching
    # for a geography name, viewing each geography's population data, or
    # exporting all the population data to a CSV file.
    first_line_num = 0
    menu_heading = ('Please select a method of accessing the %s %s from the' +
                    ' menu below.') % (
        user_selections.get(GEO_DIVISION),
        user_selections.get(SORTED_BY))

    if user_selections.get(GEO_DIVISION) == NATION:
        menu_items = ['View', 'Export to CSV']
    elif user_selections.get(GEO_DIVISION) == REGION:
        menu_items = ['View All', 'Export All to CSV']
    elif user_selections.get(GEO_DIVISION) == DIVISION:
        menu_items = ['View Top 5 Divisions',
                      'Export All Divisions to CSV', 'Search for a Division']
    elif user_selections.get(GEO_DIVISION) == STATE:
        menu_items = ['View Top 5 States',
                      'Export All States to CSV', 'Search for a State']
    elif user_selections.get(GEO_DIVISION) == COUNTY:
        menu_items = ['View Top 5 Counties',
                      'Export All Counties to CSV', 'Search for a County']
    elif user_selections.get(GEO_DIVISION) == METRO:
        menu_items = ['View Top 5 Metropolitan Areas',
                      'Export All Metropolitan Areas to CSV',
                      'Search for a Metropolitan Area']
    elif user_selections.get(GEO_DIVISION) == MICRO:
        menu_items = ['View Top 5 Micropolitan Areas',
                      'Export All Micropolitan Areas to CSV',
                      'Search for a Micropolitan Area']

    prompt = 'Selection:'

    selection = curses_io.get_user_menu_selection(screen, first_line_num,
                                                  menu_heading, menu_items,
                                                  prompt)

    if selection == menu_items[0]:
        geo_dicts = get_geography_dicts(user_selections)
        display_geo_dicts_and_return_to_main_menu(screen, geo_dicts[:5],
                                                  user_selections)
    elif selection == menu_items[1]:
        geo_dicts = get_geography_dicts(user_selections)
        prompt_heading = 'Please enter a name for the CSV file below.'
        prompt = 'File Name:'
        file_name = ''
        while file_name == '':
            file_name = curses_io.display_string_with_prompt(screen,
                                                             first_line_num,
                                                             prompt_heading,
                                                             prompt)
        csv_dicts.dicts_to_csv(geo_dicts, '%s/%s' % (EXPORT_FOLDER, file_name))
        display_export_success_and_return_to_main_menu(screen, file_name)
    elif selection == menu_items[2]:
        user_selections[SEARCH_GEO] = search_for_geography(screen,
                                                           user_selections)
        geo_dicts = get_geography_dicts(user_selections)
        display_geo_dicts_and_return_to_main_menu(screen, geo_dicts,
                                                  user_selections)


def main():
    screen = curses.initscr()
    try:
        while main_menu(screen):
            selections = geographical_divisions_menu(screen, {})
            selections = population_estimates_menu(screen, selections)
            access_data_menu(screen, selections)
    except KeyboardInterrupt:
        curses.endwin()
    finally:
        curses.endwin()


if __name__ == '__main__':
    main()
