"""
Overview of the Process

The task was to calculate the crude death rate and the age-standardized death rate for Chronic Obstructive Pulmonary Disease (COPD) for all ages in both the United States and Uganda for 2019. 
The rates were to represent the whole population of each country and be given as deaths per 100,000 people, rounded to one decimal place.

Steps Taken:

1. Clarifying Task Requirements: 
The task required understanding the definitions and formulas of crude death rate and the age-standardized death rate, as well as identifying the data that needs to be collected.

2. Data Collection: 
Data for populations of the United States and Uganda for 2019 (both total number and age-groups levels) was collected from the UN World Population website. 
An automated data ingestion pipeline was created using API get requests (see `population-data-collection.py`)

3. Data Exploration and Preprocessing: 
The datasets were explored and any required cleaning or transformation operations were performed on the data, including creating new features.

4. Calculating Death Rates: 
Functions were written to calculate the crude death rate and the age-standardized death rate:
- The crude death rate provides the number of deaths due to COPD per 100,000 people, without considering the age distribution of the population. 
- The age-standardized death rate, on the other hand, takes into account the age distribution of the population, providing a more accurate comparison between different populations.

5. Results and Implications: 
- The age-standardized death rate is generally lower than the crude death rate in countries with a higher proportion of older people, as COPD is more common in older age groups. 
- This is because the age-standardized rate is calculated using a standard age distribution, which allows for fairer comparisons between different populations.

"""


import pandas as pd
import numpy as np

# Loading the data files

population_df = pd.read_json('data/population_data.json')
population_df = pd.json_normalize(population_df['data'])

deathrate_df=pd.read_csv('data/deathrate_data.csv')

# Checking if the files were loaded correcting and exploring the first 5 rows
print('DataFrame showing total population information')    
print(population_df.head())

print('----------------------------------------------------------------------------')

print('DataFrame showing death rates from chronic obstructive pulmonary disease (COPD)')    
print(deathrate_df.head())
print('----------------------------------------------------------------------------')

# Defining variables that will be used more frequestly across the code
countries=['United States','Uganda'] # list with countries of interest
k=100000 # unit of measurement





# Functions: 
# a. For data prepocessing
def preprocess_data(deathrate_df, population_df, country, k):
    # Filtering deathrate data for the given country
    deathrate_country_df = deathrate_df.filter(like=country, axis=1)
    
    # Filtering population data for the given country
    country_pop_df = population_df[
                                    (population_df['location'].str.contains(country)) &
                                    (population_df['indicator'] == 'Total population by sex')
                                ]
    deathrate_country_df_=deathrate_country_df.copy()
    deathrate_country_df_.loc[:, 'Total_population'] = country_pop_df['value'].values[0]
    
    # Filtering the standardized population data
    standardized_pop = population_df[
                                    (population_df['location'].str.contains(country)) &
                                    (population_df['indicator'] == 'Population by 5-year age groups and sex')
                                    ][['ageLabel', 'value']]
    
    # Aggregating 85+ age group
    sum_over_85 = standardized_pop[standardized_pop["ageLabel"].isin(["85-89", "90-94", "95-99", "100+"])].sum()
    new_row = {"ageLabel": "85+", "value": sum_over_85["value"]}
    standardized_pop = standardized_pop._append(new_row, ignore_index=True)
    standardized_pop = standardized_pop[~standardized_pop["ageLabel"].isin(["85-89", "90-94", "95-99", "100+"])].reset_index(drop=True)
    
    # Concatenating the two datasets
    combined_df = pd.concat([deathrate_country_df_, standardized_pop], axis=1)
    combined_df = combined_df.rename(columns={'value': 'Pop_by_age_group'})
    
    # Creating new columns/features: population percentage by age group, total number of deaths and expected deaths
    combined_df['Pop_perc_by_age_group'] = combined_df['Pop_by_age_group'] * 100 / combined_df['Total_population']
    combined_df['Total_deaths_COPD'] = combined_df.iloc[:, 0] / k * combined_df['Total_population']
    combined_df['Expected_death'] = combined_df.iloc[:, 0] * combined_df['Pop_by_age_group'] / k
    print('----------------------------------------------------------------------------')
    return combined_df

#B. For calculations
def crude_death_rate(country,k):
    df=final_dfs[country]
    crude_value=sum(df['Total_deaths_COPD'])/sum(df['Pop_by_age_group'])*k

    return np.around(crude_value, decimals=1)

def age_standardized_death_rate(country,k):
    df=final_dfs[country]
    age_standard=sum(df['Expected_death'])/sum(df['Pop_by_age_group'])*k

    return round(age_standard, 1)




# Applying the functions

final_dfs={} # the 2 dataframes will be stores inside a dictionary for ease of access and dynamic prepocessing

# Looping through the countries and running the preprocess function
for country in countries:
    print(country)
    processed_df = preprocess_data(deathrate_df, population_df, country, k)
    final_dfs[country] = processed_df

    print(f'The Crude Death Rate per 100,000 people for {country} is {crude_death_rate(country,k)}')

    print(f'The Age-standardized death rate per 100,000 people for {country} is {age_standardized_death_rate(country, k)}')
    print('----------------------------------------------------------------------------')