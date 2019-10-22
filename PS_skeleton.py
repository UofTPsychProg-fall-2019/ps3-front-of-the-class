#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pandorable problem set 3 for PSY 1210 - Fall 2019

@author: katherineduncan

In this problem set, you'll practice your new pandas data management skills, 
continuing to work with the 2018 IAT data used in class

Note that this is a group assignment. Please work in groups of ~4. You can divvy
up the questions between you, or better yet, work together on the questions to 
overcome potential hurdles 
"""

#%% import packages 
import os
import numpy as np
import pandas as pd

#%%
# Question 1: reading and cleaning

# read in the included IAT_2018.csv file
data_path = r'C:\MA Year 1 2019\PSY1210H3 Graduate Computer Programming\Lec3_Files-master\IAT_2018.csv'
IAT = pd.read_csv(data_path)

# rename and reorder the variables to the following (original name->new name):
# session_id->id
# genderidentity->gender
# raceomb_002->race
# edu->edu
# politicalid_7->politic
# STATE -> state
# att_7->attitude 
# tblacks_0to10-> tblack
# twhites_0to10-> twhite
# labels->labels
# D_biep.White_Good_all->D_white_bias
# Mn_RT_all_3467->rt

# Here, we have renamed each column to the desired name
IAT = IAT.rename(columns={'session_id': 'id',
                          'genderidentity': 'gender',
                          'raceomb_002':'race',
                          'edu':'edu',
                          'politicalid_7':'politic',
                          'STATE':'state',
                          'att_7':'attitude',
                          'tblacks_0to10':'tblack',
                          'twhites_0to10':'twhite',
                          'labels':'labels',
                          'D_biep.White_Good_all':'D_white_bias',
                          'Mn_RT_all_3467':'rt'
                          })


# remove all participants that have at least one missing value
IAT_clean = IAT.dropna(axis=0,how='any')
IAT_clean.isnull().mean()

# check out the replace method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
# use this to recode gender so that 1=men and 2=women (instead of '[1]' and '[2]')
IAT_clean = IAT_clean.replace({'gender':{'[1]': 1, '[2]': 2}})

# use this cleaned dataframe to answer the following questions

#%%
# Question 2: sorting and indexing

# use sorting and indexing to print out the following information:

# the ids of the 5 participants with the fastest reaction times
RT_sorted = IAT_clean.sort_values(by= 'rt')
RT_top_five = RT_sorted.head().loc[:, 'id']

# the ids of the 5 men with the strongest white-good bias
# we sorted first by gender and then by bias, and sorted from least
# to greatest for gender (1 and then 2) and greatest to least
# for bias.
men_bias_sorted = IAT_clean.sort_values(by=['gender','D_white_bias'], ascending = [True,False])
men_top_five = men_bias_sorted.head().loc[:, 'id']

# the ids of the 5 women in new york with the strongest white-good bias
# similar method to above
IAT_NY = IAT_clean[(IAT_clean.state == 'NY')]
IAT_NY_women = IAT_NY.sort_values(by=['gender', 'D_white_bias'], ascending = [False,False])
NY_women_top_five = IAT_NY_women.head().loc[:,'id']

#%%
# Question 3: loops and pivots

# check out the unique method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.unique.html
# use it to get a list of states
states = pd.Series(pd.Categorical(IAT_clean.state)).unique()

# write a loop that iterates over states to calculate the median white-good
# bias per state
# store the results in a dataframe with 2 columns: state & bias

# We found the median for each state in the list of states above
# by indexing each state in a loop.
# We wrote in the state and its corresponding median
# into our dataframe we created.
state_bias = pd.DataFrame(columns=['state', 'bias'])
for state in states:
    specific_state = IAT_clean[IAT_clean.state == state]
    median = specific_state.D_white_bias.median()
    state_bias = state_bias.append({'state': state, 
                                    'bias': median}, ignore_index=True)
    
# now use the pivot_table function to calculate the same statistics
state_bias = pd.pivot_table(IAT, values = 'D_white_bias', index = ['state'], aggfunc=np.median)

# make another pivot_table that calculates median bias per state, separately 
# for each race (organized by columns)
state_race_bias= pd.pivot_table(IAT,values = 'D_white_bias',
                                index = ['state'],
                                columns = ['race'],
                                aggfunc=np.median)

#%%
# Question 4: merging and more merging

# add a new variable that codes for whether or not a participant identifies as 
# black/African American

IAT_clean['is_black'] = (1*(IAT_clean.race == 5)
# use your new variable along with the crosstab function to calculate the 
# proportion of each state's population that is black 
# *hint check out the normalization options
proportion_black = pd.crosstab(IAT_clean.state, IAT_clean.is_black, normalize=
                         'index')
proportion_black = proportion_black.loc[:, 1]

# state_pop.xlsx contains census data from 2000 taken from http://www.censusscope.org/us/rank_race_blackafricanamerican.html
# the last column contains the proportion of residents who identify as 
# black/African American 
# read in this file and merge its contents with your prop_black table
path = r'C:\MA Year 1 2019\PSY1210H3 Graduate Computer Programming\ps3-front-of-the-class-master\state_pop.xlsx'
census = pd.read_excel(path)

merged = pd.merge(census, proportion_black, left_on='State', right_on='state')

# use the corr method to correlate the census proportions to the sample proportions

census_corr = merged.corr().loc['per_black', 1]

# now merge the census data with your state_race_bias pivot table
merge_consens_race = pd.merge(census, state_race_bias, left_on='State', right_on='state')

# use the corr method again to determine whether white_good biases is correlated 
# with the proportion of the population which is black across states
# calculate and print this correlation for white and black participants

census_race_correlation = merge_consens_race.corr().loc['per_black', [5.0, 6.0]]

print('The correlation for white participants is ' + str(census_race_correlation.loc[5.0]) +
      '. The correlation for black participants is ' + str(census_race_correlation.loc[6.0]) + '.')






