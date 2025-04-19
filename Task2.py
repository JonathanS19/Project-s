# Importing required packages 
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Reading dataset
with open('/content/Dataset .csv',encoding='utf-8',errors='replace') as f:
  data = pd.read_csv(f)
data_cpy = data.copy()

# Remove the null values
print("Before removing the null values : ",len(data_cpy))
data_cpy = data_cpy.dropna()
print("After removing the null values : ",len(data_cpy),"\n")

# Dropping unecessary columns
dropped = ['Restaurant ID','Country Code','Address','Locality','Locality Verbose','Currency','Longitude','Latitude','Rating color','Rating text'	]
data_cpy.drop(dropped,axis=1,inplace=True)

#Encoding binary values
bin_encode = ['Has Table booking','Has Online delivery','Is delivering now','Switch to order menu']
for val in bin_encode:
  data_cpy[val] = data_cpy[val].map({'Yes':1,'No':0})

# Using Apply to remove values

cols_corr = ['Restaurant Name','City','Cuisines']

def remove_elem(text):
  text = re.sub(r'[^\x00-\x7F]','',text)
  return text

for val in cols_corr:
  data_cpy[val] = data_cpy[val].apply(remove_elem)


