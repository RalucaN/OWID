# COPD Death Rate Analysis

This project calculates the crude death rate and the age-standardized death rate for Chronic Obstructive Pulmonary Disease (COPD) for all ages in both the United States and Uganda for 2019. The rates represent the whole population of each country and are given as deaths per 100,000 people, rounded to one decimal place.

## Prerequisites

The project requires `python 3` and the following libraries: `pandas`, `numpy`, and `requests`. You can install these using pip:

```bash
pip install -r requirements.txt
```

## Installing

Clone the repository to your local machine:

```bash
git clone https://github.com/RalucaN/OWID.git
```

## Data Collection

```bash
python population-data-collection.py
```

Data for populations of the United States and Uganda for 2019 (both total number and age-groups levels) was collected from the UN World Population website using their API. The API allows us to send a GET request and receive the data in JSON format.

An automated data ingestion pipeline was created using API get requests.

The API request is constructed using both required and optional parameters. 
- The required parameters include the indicator ID, location, and version. 
- The optional parameters include the start year, end year, and sex (additional optional parameter can be added). These parameters are read from a configuration file, `config.ini`.

 The collected data is stored in JSON file in the `data` folder.


## Data Analysis

```bash
python main.py 
```

The main script (`main-script.py`) is responsible for executing the entire data analysis process. Here's an overview of its functionality:

1. **Loading Data:** The script starts by loading the population and death rate data from the JSON and CSV files in the `data` folder.

2. **Data Preprocessing:** The loaded data is then preprocessed. This involves exploring and transforming the data, by creating new features (such as population percentage by age group, total number of deaths, and expected deaths).

3. **Calculating Death Rates:** After preprocessing the data, the script calculates the crude death rate and the age-standardized death rate for each country. These calculations are performed using the `crude_death_rate` and `age_standardized_death_rate` functions.

4. **Printing Results:** Finally, the script prints the calculated death rates to the console. To save the output from the console to a text file, `output.txt`, run the command below:

```bash
python main.py > output.txt
```


## Project Diagram
```
project_directory/               # Root directory of the project
│
├── data/                       # Directory for storing data files
│   ├── population_data.json    # JSON file with population data
│   └── deathrate_data.csv      # CSV file with death rate data
│
├── config.ini                  # Configuration file for data collection script
│
├── main-script.py                     # Main Python script
│
├── population-data-collection.py      # Python script for data collection
│
├── requirements.txt            # File listing project dependencies
│
└── README.md                   # Project description and instructions
```


