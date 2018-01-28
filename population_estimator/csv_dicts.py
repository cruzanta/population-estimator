#!/usr/bin/env python

"""
Module for storing the rows of a CSV file to dictionaries and vice versa.
"""

import csv


def csv_rows_to_dicts(csv_file, header_row_num):
    """Stores the rows of a CSV file in dictionaries.

    Retrieves the rows from a CSV file, stores the content of each row in its
    own dictionary using the column names of the header row as the keys for the
    dictionary, and adds each dictionary to a list.

    Args:
        csv_file: A string that contains the path to a CSV file.
        header_row_num: An integer that represents the row number of the header
            row in the CSV file.

    Returns:
        A list of dictonaries with each dictionary containing the content of a
        row in the CSV file. For example:

        [{'Animal': 'cat', 'Name': 'Frank', 'Age': 8},
         {'Animal': 'dog', 'Name': 'Buddy', 'Age': 2},
         {'Animal': 'bird', 'Name': 'Jim', 'Age': 4}]
    """
    csv_dicts = []

    with open(csv_file) as input_file:
        for i in range(header_row_num - 1):
            input_file.next()  # Skip to the header row.
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            csv_dicts.append(row)

    return csv_dicts


def dicts_to_csv(list_of_dicts, file_name):
    """Stores the content of a list of dictionaries as rows in a CSV file.

    Retrieves the keys and values of each dictionary and adds the values of each
    dictionary to their own row in a CSV file. The keys of each dictionary are
    used as the column names of the CSV file's header row.

    Args:
        list_of_dicts: A list that contains dictionaries whose values will be
            added to a CSV file as rows.
        file_name: A string that contains the name of the CSV file that is
            created.

    Returns:
        A CSV file whose header row is composed of each dictionary's keys and
        whose rows contain the values of each dictionary. For example:

        Animal, Name, Age
        cat, Frank, 8
        dog, Buddy, 2
        bird, Jim, 4
    """
    with open('%s.csv' % (file_name), 'w') as csvfile:
        fieldnames = list_of_dicts[0].keys()  # CSV file header row.
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for dct in list_of_dicts:
            writer.writerow(dct)
