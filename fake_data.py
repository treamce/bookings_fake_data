## Importing relevant libraries 
import pandas as pd 
import numpy as np 
import random

from datetime import datetime, timedelta

from faker import Faker 
fake = Faker()

## Setting a random seed 
Faker.seed(42)
np.random.seed(42)
random.seed(42)

## Defining number of rows 
rows = 109273

## Defining values for categorical fields 
channels = ['Online','Direct','App']
products = ['Premier','Quality','Economy']
countries = ["Ireland","USA", "Canada", "UK", "Germany", "France", "Italy","India", "China", "Japan", "Australia", "Brazil"]

## Creating a mapping of cities to countries 
country_to_cities_with_airports = {
    "Ireland": ["Dublin", "Cork", "Shannon", "Knock","Belfast"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "UK": ["London", "Manchester", "Birmingham", "Liverpool", "Edinburgh"],
    "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne"],
    "France": ["Paris", "Marseille", "Lyon", "Nice", "Toulouse"],
    "Italy": ["Rome", "Milan", "Venice", "Naples", "Bologna"],
    "India": ["New Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"],
    "China": ["Beijing", "Shanghai", "Hong Kong", "Guangzhou", "Shenzhen"],
    "Japan": ["Tokyo", "Osaka", "Nagoya", "Hiroshima", "Sapporo"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "Brazil": ["Sao Paulo", "Rio de Janeiro", "Brasilia", "Salvador", "Fortaleza"]
}

##################
## Creating variable weighting for channels 
def generate_random_weights(base_weights, variation=0.05):
    varied_weights = [
        max(0, w + np.random.uniform(-variation, variation)) for w in base_weights
    ]
    total = sum(varied_weights)
    return [w / total for w in varied_weights]

## Defining the base weights
base_weights = [0.6, 0.25, 0.15] 

## Random weights
random_weights = generate_random_weights(base_weights)
###################

## Creating seasonality
def generate_biased_date():
    # Get the current date
    current_date = datetime.now()

    # Adjusted month weights to ensure no extreme overrepresentation of any month
    month_weights = [0.08, 0.08, 0.085, 0.085, 0.09, 0.095, 0.1, 0.105, 0.1, 0.1, 0.12, 0.115]

    # Apply weighting for years: 2025 is three times less likely than 2023 or 2024
    years = [current_date.year, current_date.year - 1, current_date.year - 2]  # Current year, last year, and two years ago
    year_weights = [1, 1, 0.33]  # Weight 2025 (current year) as 1, and 2025 as 0.33 to make it 3 times less likely

    # Randomly select a year based on weights
    year = random.choices(years, weights=year_weights, k=1)[0]

    # Define the available months (for all years, from January to December)
    available_months = list(range(1, 13))  # January to December
    available_weights = month_weights  # Use the month weights to adjust the probability of each month

    # Randomly select a month based on the adjusted weights
    month = random.choices(available_months, weights=available_weights, k=1)[0]

    # Now handle the day based on the selected month and year
    if month in {1, 3, 5, 7, 8, 10, 12}:  # Months with 31 days
        max_day = 31
    elif month in {4, 6, 9, 11}:  # Months with 30 days
        max_day = 30
    else:  # February, handle leap years
        max_day = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28

    # Randomly select the day, hour, and minute
    day = random.randint(1, max_day)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    # Return the generated datetime object
    return datetime(year, month, day, hour, minute)

###################
## Creating a booked timestamp - only want 40% of searches to be booked 
def booked_timestamp_generate(search_timestamp):
    if random.random() <= 0.4:
        days_to_add = random.randint(1,21)
        booked_date = search_timestamp + timedelta(days_to_add)
        return booked_date
    else:
        return None
    
## Read company names from a file and map them to channels
df_companies = pd.read_csv('companies.csv')

# Map companies to channels from the CSV (assumes your CSV file has 'Channel' and 'Company_Name' columns)
company_data = df_companies.groupby('Channel')['Company_Name'].apply(list).to_dict()

# Load company data
## Generate mock data 
data = {
    "Opportunity ID":  [fake.uuid4() for _ in range(rows)],
    "Channel": random.choices(
        ['Online', 'App', 'Direct'],
        weights=random_weights,  
        k=rows
    ),
    "Search Timestamp": [generate_biased_date() for _ in range(rows)],
    "Booked Timestamp": [booked_timestamp_generate(search_timestamp) for search_timestamp in [generate_biased_date() for _ in range(rows)]],
    "Weight": np.random.uniform(1, 57.2, rows).round(2),
    "Chargeable Weight":np.random.uniform(2, 70, rows).round(2),
    "Volume": np.random.uniform(0.1, 43.7, rows).round(2),
    "Origin Country": [random.choice(list(country_to_cities_with_airports.keys())) for _ in range(rows)],
    "Origin City": [random.choice(country_to_cities_with_airports[country]) for country in random.choices(list(country_to_cities_with_airports.keys()), k=rows)],
    "Destination Country": [random.choice(list(country_to_cities_with_airports.keys())) for _ in range(rows)],
    "Destination City": [random.choice(country_to_cities_with_airports[country]) for country in random.choices(list(country_to_cities_with_airports.keys()), k=rows)],
    "Product": [random.choice(products) for _ in range(rows)],
    "Price per Kilo": [5 if product == 'Premier' else 2.50 if product == 'Quality' else 0.75 for product in [random.choice(products) for _ in range(rows)]],
    "Row_Number": list(range(1, rows+1)) 
}

# Create DataFrame from mock data
df = pd.DataFrame(data)

# Now, assign a company based on the Channel
def assign_company(channel):
    # Ensure the channel has a list of companies
    if channel in company_data and company_data[channel]:
        return random.choice(company_data[channel])  # Select a company from the matching channel
    return None  # If no company is found for the channel

# Apply the function to add a 'Company_Name' column
df["Company_Name"] = df["Channel"].apply(assign_company)

# Save the DataFrame to CSV
df.to_csv("mock_opportunities.csv", index=False)

print("Mock opportunities dataset with companies created and saved!")