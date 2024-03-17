"""
Accessing UN population Data via API get requests

Link to the swagger that can be used to create the API get curl:
https://population.un.org/dataportalapi/index.html#/

Example:
curl -X 'GET' \
  'https://population.un.org/dataportalapi/api/v1/data/indicators/{indicator_id}/locations/{location}?startYear={startyear}&endYear={endyear}&sexes={sex}&pagingInHeader=false&format=json' \
  -H 'accept: application/json'

"""

# Importing libraries
import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('config.ini')

# Required indicators
indicator_id = config['REQUIRED']['indicator_id']
location = config['REQUIRED']['location']
version = config['REQUIRED']['version']

# Optional indicators
startyear = config['OPTIONAL']['startyear']
endyear = config['OPTIONAL']['endyear']
sex = config['OPTIONAL']['sex']

# Transforming list into string
location= location.replace(",", "%2C")
indicator_id= indicator_id.replace(",", "%2C")

url = 'https://population.un.org/dataportalapi/api/{version}/data/indicators/{indicator_id}/locations/{location}?startYear={startyear}&endYear={endyear}&sexes={sex}&pagingInHeader=false&format=json'
headers = {'accept': 'application/json'}

# Construct the complete URL
complete_url = url.format(version=version, indicator_id=indicator_id, location=location, startyear=startyear, endyear=endyear, sex=sex)

print(complete_url)

# Make the GET request
response = requests.get(complete_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Save the data to a JSON file
    with open('data/population_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print('Data saved to population_data.json')
else:
    print(f"Error: {response.status_code} - {response.text}")
