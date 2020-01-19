# Import SQL Libraries
import pandas as pd

# Database Credentials

engine = ''

# SQL Queries
query_jobs = open(r'./src/get_data.sql').read()
query_zips = open(r'./src/zipcode_by_year.sql').read()

# Get Data
data_jobs = pd.read_sql(query_jobs, engine)
data_zips = pd.read_sql(query_zips, engine)

# Write Data to CSV for the next Step
data_jobs.to_csv('./data/jobs.csv')
data_zips.to_csv('./data/zipyear.csv')