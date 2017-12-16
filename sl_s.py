# -*- coding: UTF-8 -*-

import pandas as pd

# following function has been created specifically for the population file
def sl_pop(df_distribution, value_to_distribute):

    list_distribution = df_distribution["zweitstimmen"].astype(int)

    # calculate total population
    sum_distribution = list_distribution.sum()

    # calculate required population for 1 seat
    pop_per_seat = sum_distribution / value_to_distribute

    # run while loop until sum of rounds is equal to number of seats
    while (list_distribution / pop_per_seat).round().sum() != value_to_distribute:
        if (list_distribution / pop_per_seat).round().sum() > value_to_distribute:
            pop_per_seat += 1

        elif (list_distribution / pop_per_seat).round().sum() < value_to_distribute:
            pop_per_seat -= 1

    # create return data frame
    df_result = pd.DataFrame(columns=["body","seats"])

    # assign population table to return data frame and run calculation with previously calculated divident
    df_result["body"] = df_distribution["body"]
    df_result["seats"] = (list_distribution / pop_per_seat).round()

    return df_result

def sl_votes(df_distribution, value_to_distribute):


    list_distribution = df_distribution["zweitstimmen"].astype(int)

    # calculate total population
    sum_distribution = list_distribution.sum()

    # calculate required population for 1 seat
    pop_per_seat = sum_distribution / value_to_distribute

    # run while loop until sum of rounds is equal to number of seats
    while (list_distribution / pop_per_seat).round().sum() != value_to_distribute:
        if (list_distribution / pop_per_seat).round().sum() > value_to_distribute:
            pop_per_seat += 10

        elif (list_distribution / pop_per_seat).round().sum() < value_to_distribute:
            pop_per_seat -= 10

    # create return data frame
    df_result = pd.DataFrame(columns=["land","gruppe","seats"])
    # assign population table to return data frame and run calculation with previously calculated divident
    df_result["gruppe"] = df_distribution["gruppe"]
    df_result["seats"] = (list_distribution / pop_per_seat).round()
    df_result["land"] = df_distribution["land"]

    return df_result

def sl_nation(df_distribution, value_to_distribute):


    list_distribution = df_distribution["zweitstimmen"].astype(int)

    # calculate total population
    sum_distribution = list_distribution.sum()

    # calculate required population for 1 seat
    pop_per_seat = sum_distribution / value_to_distribute

    # run while loop until sum of rounds is equal to number of seats
    while (list_distribution / pop_per_seat).round().sum() != value_to_distribute:
        if (list_distribution / pop_per_seat).round().sum() > value_to_distribute:
            pop_per_seat += 1

        elif (list_distribution / pop_per_seat).round().sum() < value_to_distribute:
            pop_per_seat -= 1

    # create return data frame
    df_result = pd.DataFrame(columns=["gruppe","seats"])
    # assign population table to return data frame and run calculation with previously calculated divident
    df_result["gruppe"] = df_distribution["gruppe"]
    df_result["seats"] = (list_distribution / pop_per_seat).round()

    return df_result