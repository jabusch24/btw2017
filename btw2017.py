# -*- coding: UTF-8 -*-

#I wasn't able to finish until Sunday evening. Will have it done by next class Wednesday for sure.

#from sl_s import sl_pop,sl_votes,sl_nation
import pandas as pd

# check whether each party gets their minimum # of seats
def compareTables(targetDF, inputDF):

    #check whether both tables have the same size
    if len(targetDF) != len(inputDF):
        print("table sizes don't match. Try again!")

    #elif targetDF[2].names == "mn_seats":
    #    print("name is min_seats")
    #iterate through the tables and compare sizes.
    else:
        for i in range(len(targetDF)):
            if targetDF.iloc[:,1].at[i] > inputDF.iloc[:,1].at[i]:
                #print("at least one value is still too small")
                return False

            else:
                i += 1
    return True


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



# load csv into dataframe
df_btw = pd.read_csv("/home/jannis/DS/PDDS/CSV/ergebnisse.csv", sep=";")

# delete aggregated rows and turn non-ints to 0s
df_btw = df_btw.loc[~df_btw["gruppe"].isin(["Wähler","Wahlberechtigte","Gültige","Ungültige"])]
df_btw["erststimmen"] = df_btw["erststimmen"].replace("-",0).astype(int)
df_btw["zweitstimmen"] = df_btw["zweitstimmen"].replace("-",0).astype(int)

# correct false party names
df_btw["gruppe"] = df_btw["gruppe"].replace("GRÜNE/B 90", "GRÜNE").replace("DIE LINKE.","DIE LINKE").replace("ÖDP / Familie ..","ÖDP")
df_btw = df_btw.sort_values(by=["land"])

# filter for the directmandate winner in every constituency
df_btw_directmandate = df_btw.sort_values(by=["erststimmen"],ascending=False).groupby(["land","wahlkreis"]).first()


# filter for directmandates per party per state
df_btw_directmandate_count = df_btw_directmandate.groupby(["land","gruppe"]).agg(['count']).reset_index()
df_btw_directmandate_count.columns = ["land","gruppe","erststimmen","zweitstimmen"]
df_btw_directmandate_count = df_btw_directmandate_count.sort_values(by=["land"])

# filter for party zweitstimmen per state
df_btw_state = df_btw.groupby(["land","gruppe",])["zweitstimmen"].sum().reset_index()

# calculate zweitstimmen distribution on country level
df_btw_country_shares = df_btw.groupby(["gruppe"]).sum()/df_btw["zweitstimmen"].sum()*100
df_btw_country_shares = df_btw_country_shares.loc[df_btw_country_shares["zweitstimmen"]>=5].reset_index()
winning_parties = df_btw_country_shares["gruppe"]

# filter for winning parties only to calculate in list_seats distribution
df_btw_state = df_btw_state.loc[df_btw_state["gruppe"].isin(winning_parties)]

# prepare data frame for Sainte-Laguë/Schepers computation
df_population = pd.DataFrame(columns=["body","zweitstimmen"])
df_population1 = pd.read_csv("/home/jannis/DS/PDDS/CSV/population.csv", sep=";")
df_population["body"] = df_population1["state"]
df_population["zweitstimmen"] = df_population1["population"]
df_population = df_population.sort_values(by=["body"]).reset_index()

# calculate the seat distribution among stataes via Sainte-Laguë/Schepers
df_seats = pd.DataFrame(columns=["body","seats"])
df_seats = sl_pop(df_population, 598)

# iterate through states and apply sl_votes to identify list_seats
i = 1
df_btw_state_winners = pd.DataFrame()

for i in range(1,17):
    # filter for winning parties only
    df_carrier = sl_votes(df_btw_state.groupby(["land"]).get_group(i),df_seats["seats"].at[i-1])
    frames = [df_btw_state_winners, df_carrier]
    # append data frame to winner data frame during each iteration
    df_btw_state_winners= pd.concat(frames)

# create final data frame
df_ueberhang = pd.DataFrame()
df_ueberhang = df_btw_state_winners
df_ueberhang.columns = ["state","party","list_seats"]
df_ueberhang["direct_seats"] = 0
df_ueberhang["ueberhang"] = 0


# allocate the values of the directmandate winners to the final table
for i in range(0,29):
    df_btw_directmandate_count["gruppe"].at[i]
    # identify index where value should be inserted
    intega = df_ueberhang.loc[(df_ueberhang["state"]==df_btw_directmandate_count["land"].at[i])
                     & (df_ueberhang["party"]==df_btw_directmandate_count["gruppe"].at[i])].index
    # insert value from direktmandat data frame to final ueberhand data frame
    df_ueberhang["direct_seats"].at[int(intega[0])] = df_btw_directmandate_count["erststimmen"].at[i]
    i = i+1

# calculate ueberhandmandate
df_ueberhang["ueberhang"] = df_ueberhang["direct_seats"]-df_ueberhang["list_seats"]
# delete all negative values
df_ueberhang["ueberhang"] = [0 if i<0 else i for i in df_ueberhang["ueberhang"]]

# export data frame as csv
#df_ueberhang.to_csv("/home/jannis/DS/PDDS/CSV/ueberhangmandate.csv", sep=";")

# Exercise 4
df_ueberhang["list_seats"] = df_ueberhang["list_seats"].astype(int)
df_ueberhang = df_ueberhang.reset_index()
df_ueberhang["min_seats"] = df_ueberhang["list_seats"]
i = 0
for i in range(0,len(df_ueberhang["list_seats"])):
    if df_ueberhang["min_seats"].at[i] <= df_ueberhang["direct_seats"].at[i]:
        df_ueberhang["min_seats"].at[i] = df_ueberhang["direct_seats"].at[i]
    i += 1

df_btw_zweitstimmen = df_btw_state.groupby(["gruppe"])["zweitstimmen"].agg('sum').reset_index()

df_min_seats = df_ueberhang.groupby(["party"])["min_seats"].agg('sum').reset_index()

i = 644
df_iterateSeats = sl_nation(df_btw_zweitstimmen,i)
summe = df_iterateSeats["seats"].sum()


df_iterateSeats["seats"] = df_iterateSeats["seats"].astype(int)


# apply sainte lague as long as not ALL parties receive minimum amount of seats
while compareTables(df_min_seats, df_iterateSeats) == False:
    df_iterateSeats = sl_nation(df_btw_zweitstimmen, i)
    i += 1

df_btw_zweitstimmen["seats"] = df_iterateSeats["seats"].astype(int)
df_btw_zweitstimmen["divisor"] = df_btw_zweitstimmen["zweitstimmen"]/df_btw_zweitstimmen["seats"]


df_btw_state["unroundSeats"] = 0.0
df_btw_state = df_btw_state.reset_index()
df_btw_state = df_btw_state.drop("index", 1)

i = 0
for i in range(len(df_btw_state)):
    divisor = df_btw_zweitstimmen.loc[(df_btw_zweitstimmen["gruppe"] == df_btw_state["gruppe"].at[i])].reset_index()

    divisor = divisor["divisor"][0].astype(float)
    df_btw_state["unroundSeats"].at[i] = df_btw_state["zweitstimmen"].at[i]/divisor
    i = i + 1

df_btw_state.groupby(["gruppe"]).sum()
df_btw_state["roundSeats"] = df_btw_state["unroundSeats"].round()

targetDF = pd.DataFrame()
targetDF["party"] = df_btw_zweitstimmen["gruppe"]
targetDF["seats"] = df_btw_zweitstimmen["seats"]

placeholderDF = df_btw_state.groupby(["gruppe"]).sum().reset_index()
inputDF = pd.DataFrame()
inputDF["gruppe"] = placeholderDF["gruppe"]
inputDF["seats"] = placeholderDF["roundSeats"]

while inputDF["seats"] != targetDF["seats"]:
    inputDF = sl_nation(targetDF,inputDF)

print(inputDF)



#print(df_btw_state)

