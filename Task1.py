# Importing
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Open data and check for null values

data = pd.read_csv("/content/Dataset .csv")#When you read values using pandas its automatically converted into a dataframe

data_cpy = data.copy()

# data_cpy.isnull().sum()

# Dropping unwanted columns
data_cpy = data.drop(['Restaurant ID','Restaurant Name','Address','Locality','Locality Verbose','Longitude','Latitude','Switch to order menu','Currency','Is delivering now','Rating color','Rating text'],axis=1)

# Replacing flawed values
for i,val in enumerate(data_cpy['City']):
  data_cpy.at[i,'City'] = re.sub(r'[^a-zA-Z\d, ]','',val)
# Binary Encoding
for val in ['Has Table booking',	'Has Online delivery']:
  data_cpy[val] = data_cpy[val].map({"Yes":1,"No":0})

# Has Potential since it takes the no of cuisines available
data_cpy["Cuisines"] = data_cpy["Cuisines"].fillna("")
for i,val in enumerate(data_cpy['Cuisines']):
  data_cpy.at[i,'Cuisines'] = int(len(val.split(',')))

# Most influential Features
data_cpy = data_cpy.drop(['City'],axis=1)
data_cpy.corr()


# Creating a map to visvualize the important features

import seaborn as sns
import matplotlib.pyplot as plt

# Select relevant features and the target
features = [
    'Average Cost for two',
    'Price range',
    'Country Code',
    'Has Table booking',
    'Has Online delivery',
    'Cuisines',
    'Aggregate rating'
]

# Filter and melt the dataframe for plotting
plot_data = data_cpy[features].dropna()
melted = plot_data.melt(id_vars='Aggregate rating', var_name='Feature', value_name='Value')

# Scatter plot using seaborn
plt.figure(figsize=(12, 6))
sns.scatterplot(data=melted, x='Aggregate rating', y='Value', hue='Feature', alpha=0.6)
plt.title('Scatter Plot of Features vs Aggregate Rating')
plt.grid(True)
plt.show()

# Importing the ML models requirements
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

# Creating testing and training data 
features = ['Average Cost for two', 'Price range', 'Country Code', 'Cuisines',
            'Has Table booking', 'Has Online delivery', 'Votes']
target = 'Aggregate rating'

X = data_cpy[features]
Y = data_cpy[target]

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

# Linear regression
lr_model = LinearRegression()

lr_model.fit(x_train,y_train)
y_pred = lr_model.predict(x_test)

mse_test = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse_test)
r2 = r2_score(y_test,y_pred)

print(f"Linear Regression MSE: {mse_test:.4f}")
print(f"Linear Regression R² : {r2:.4f}")

# Decision Tree model
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(x_train,y_train)

y_pred = dt_model.predict(x_test)

mse_test = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse_test)
r2 = r2_score(y_test,y_pred)

print(f"Decision Tree Regression MSE: {mse_test:.4f}")
print(f"Decision Tree Regression R² : {r2:.4f}")

# Random forest model
rf_model = RandomForestRegressor(n_estimators=100,random_state=42)
rf_model.fit(x_train,y_train)

y_pred = rf_model.predict(x_test)

mse_test = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse_test)
r2 = r2_score(y_test,y_pred)

print(f"Random Forest Regression MSE: {mse_test:.4f}")
print(f"Random Forest Regression R² : {r2:.4f}")
