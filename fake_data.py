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
rows = 100000

## Defining values for categorical fields 
channels = ['Online','Direct','App']
products = ['Premier','Quality','Economy']
countries = ["Ireland","USA", "Canada", "UK", "Germany", "France", "Italy","India", "China", "Japan", "Australia", "Brazil"]

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

    # Randomly select the year to be this year or last year
    year = random.choice([current_date.year - 1, current_date.year - 2])

    # Randomly choose the month,date,hour,min
    month = random.choices(
        list(range(1, 13)),
        weights=[0.09, 0.09, 0.095, 0.09, 0.10, 0.105, 0.11, 0.115, 0.11, 0.12, 0.15, 0.13]
    )[0]
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    # Return the generated datetime 
    return datetime(year, month, day, hour, minute)

###################
## Creating a booked timestamp
def booked_timestamp_generate(search_timestamp):
    if random.random() <= 0.4:
        days_to_add = random.randint(1,21)
        booked_date = search_timestamp + timedelta(days_to_add)
        return booked_date
    else:
        return None
                                                

## Generate mock data 
data = {
    "Opportunity ID":  [fake.uuid4() for _ in range(rows)],
    "Channel":random.choices(
        ['Online', 'App', 'Direct'],
        weights= random_weights,  
        k= rows),
    "Search Timestamp": [generate_biased_date() for _ in range(rows)],
    "Booked Timestamp": [booked_timestamp_generate(search_timestamp) for search_timestamp in [generate_biased_date() for _ in range(rows)]]
}

# Create DataFrame
df = pd.DataFrame(data)


df.to_csv("mock_opportunities.csv", index =False)

print("Mock dataset created and saved !")
