
## Importing relevant libraries 
import pandas as pd 
import numpy as np 
import random

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


## Generate mock data 

data = {
    "Opportunity ID":  [fake.uuid4() for _ in range(rows)],
    "Channel":random.choices(
        ['Online', 'App', 'Direct'],
        weights= random_weights,  
        k= rows),
    "Search Timestamp": [fake.date_time_between(start_date="-2y", end_date="now") for _ in range(rows)],
    "Booked Timestamp": [
    fake.date_time_between(start_date="-2y", end_date="now") if random.random() > 0.6 else None
    for _ in range(rows)
],
}

# Create DataFrame
df = pd.DataFrame(data)

## Booked timestamp should always be after search timestamp 
df["Booked Timestamp"] = df.apply(
    lambda row: fake.date_time_between(start_date=row["Search Timestamp"], end_date="now"),
    axis=1
)

df.to_csv("mock_opportunities.csv", index =False)

print("Mock dataset created and saved")
