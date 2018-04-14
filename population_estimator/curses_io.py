#!/usr/bin/env python

"""
Module for painting output on and obtaining input from a text-based terminal
window using the curses library.
"""

import curses
import textwrap


def display_string(screen, a_string, output_line):
    # Paints a string on a text-based terminal window.
    _, width = screen.getmaxyx()

    try:
        screen.addstr(output_line, 0, textwrap.fill(a_string, width - 1))
    except curses.error:
        screen.addstr(0, 0, textwrap.fill(
            'Terminal window too small for output! Please resize. ', width - 1))

    return output_line


def display_list_items(screen, a_list, output_line):
    # Paints each item of a list on a text-based terminal window.
    for item in a_list:
        output_line = display_string(screen, '%s' % (item), output_line)
        output_line += 1

    return output_line


def display_formatted_dict(screen, dct, output_line):
    # Paints each key, value pair of a dict on a text-based terminal window.
    for key, value in dct.items():
        formatted_dict = '%s: %s' % (key, value)
        output_line = display_string(screen, formatted_dict, output_line)
        output_line += 1

    return output_line


def display_string_with_prompt(screen, first_line_num, a_string, prompt):
    """Paints two strings and accepts input.

    Paints two strings on a text-based terminal window. The latter of the two
    strings serves as the prompt for the user to enter input.

    Args:
        screen: A window object that represents the text-based terminal window.
        first_line_num: An integer that represents the location along the y-axis
            of the terminal window where the first character of the first string
            is painted.
        a_string: The first string that is painted on the terminal window.
        prompt: A string that serves as a prompt for the user to enter input.

    Returns:
        A string that the user enters in as input.
    """
    screen.clear()

    output_line = first_line_num
    output_line = display_string(screen, a_string, output_line)

    output_line += 3
    output_line = display_string(screen, prompt, output_line)

    screen.refresh()

    return screen.getstr(output_line, len(prompt) + 1)


def display_list_items_with_prompt(screen, first_line_num, a_string, a_list,
                                   prompt):
    """Paints a string, each item of a list, and accepts input.

    Paints a string, each item of a list, and another string on a text-based
    terminal window. Each item of the list is painted on its own line.
    The second string serves as a prompt for the user to enter input.

    Args:
        screen: A window object that represents the text-based terminal window.
        first_line_num: An integer that represents the location along the y-axis
            of the terminal window where the first character of the first string
            is painted.
        a_string: The first string that is painted on the terminal window.
        a_list: A list whose items are painted on each line of the terminal
            window.
        prompt: A string that serves as a prompt for the user to enter input.

    Returns:
        A string that the user enters in as input.
    """
    screen.clear()

    output_line = first_line_num
    output_line = display_string(screen, a_string, output_line)

    output_line += 2
    output_line = display_list_items(screen, a_list, output_line)

    output_line += 1
    output_line = display_string(screen, prompt, output_line)

    screen.refresh()

    return screen.getstr(output_line, len(prompt) + 1)


def display_formatted_dicts_with_prompt(screen, first_line_num, a_string,
                                        list_of_dicts, prompt):
    """Paints a string, each item of each dict in a list, and accepts input.

    Paints a string, each item of each dict in a list, and another string on a
    text-based terminal window. Each key, value pair of each dict is painted on
    its own line with the key and value separated by a colon. The second string
    serves as a prompt for the user to enter input.

    Args:
        screen: A window object that represents the text-based terminal window.
        first_line_num: An integer that represents the location along the y-axis
            of the terminal window where the first character of the first string
            is painted.
        a_string: The first string that is painted on the terminal window.
        list_of_dicts: A list of dictionaries whose key, value pairs are painted
            on their own line of the terminal window.
        prompt: A string that serves as a prompt for the user to enter input.

    Returns:
        A string that the user enters in as input.
    """
    screen.clear()

    output_line = first_line_num
    output_line = display_string(screen, a_string, output_line)

    output_line += 2
    for dct in list_of_dicts:
        output_line = display_formatted_dict(screen, dct, output_line)
        output_line += 1

    output_line += 1
    output_line = display_string(screen, prompt, output_line)

    screen.refresh()

    return screen.getstr(output_line, len(prompt) + 1)


def get_user_menu_selection(screen, first_line_num, a_string, menu_items,
                            prompt):
    """Paints a string, a menu, and accepts input.

    Paints a string, a menu, and another string on a text-based terminal window.
    The menu is composed of the items in a list, and each item is assigned its
    own number that represents the order in which the item appears in the menu.
    The second string serves as a prompt for the user to enter a number from the
    menu.

    Args:
        screen: A window object that represents the text-based terminal window.
        first_line_num: An integer that represents the location along the y-axis
            of the terminal window where the first character of the first string
            is painted.
        a_string: The first string that is painted on the terminal window.
        menu_items: A list whose items are painted on each line of the terminal
            window as menu options.
        prompt: A string that serves as a prompt for the user to enter a number
            from the menu.

    Returns:
        A string representation of the item in 'menu_items' that the user
        selects.
    """
    # Create a dictionary that contains the items in 'menu_items'. Each item
    # is added as a value with an integer key that represents the order in which
    # the item will appear in the menu.
    item_key = 1
    selection_items = {}
    for item in menu_items:
        selection_items['%s' % (item_key)] = item
        item_key += 1
    # Display the menu and prompt the user for a selection.
    while True:
        screen.clear()

        output_line = first_line_num
        output_line = display_string(screen, a_string, output_line)

        output_line += 3
        for menu_num in sorted(selection_items.iterkeys()):
            item_line = '%s) %s' % (menu_num, selection_items[menu_num])
            output_line = display_string(screen, item_line, output_line)
            output_line += 1

        output_line += 1
        output_line = display_string(screen, prompt, output_line)

        screen.refresh()

        input = screen.getstr(output_line, len(prompt) + 1)

        if input not in selection_items.keys():
            continue  # Force the user to enter a valid selection.
        else:
            return selection_items[input]
