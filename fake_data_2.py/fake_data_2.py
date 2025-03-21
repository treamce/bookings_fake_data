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
rows = 310  # You can change this to the desired number of rows

## Read company names from a file
def load_company_names(filename="company_names.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Load company names from file
company_names = load_company_names()   

# Ensure the number of company names is at least equal to 'rows'
if len(company_names) < rows:
    raise ValueError(f"Insufficient company names in the file. Need at least {rows} names.")

channels = ['Online','Direct','App']

##################
## Creating variable weighting for channels 
def generate_random_weights(base_weights, variation=0.10):
    varied_weights = [
        max(0, w + np.random.uniform(-variation, variation)) for w in base_weights
    ]
    total = sum(varied_weights)
    return [w / total for w in varied_weights]

## Defining the base weights
base_weights = [0.7, 0.30, 0.10] 

## Random weights
random_weights = generate_random_weights(base_weights)
###################

# Create data dictionary with 'rows' length
data = {
    "Company_Name": random.choices(company_names, k=rows),  # Ensure 'k=rows' to generate the correct number of entries
    "Channel": random.choices(
        channels,
        weights=random_weights,  
        k=rows)  # 'k=rows' ensures that the length matches
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("companies.csv", index=False)

print("Mock dataset created and saved!")

