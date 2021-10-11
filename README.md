# House sales

This project uses [this dataset](https://www.kaggle.com/harlfoxem/housesalesprediction), which contains sale prices of homes sold between May 2014 and May 2015. The goal is to generate insights on the house market. From the analysis it is concluded that selected houses could be bought and sold, with 30% return, while still below the average market price.

# Solution strategy

1. Data collection: download the dataset from kaggle.

2. Data description: explore the raw data using descriptive statistics.

3. Feature engineering: convert and derive new attributes based on the original data to better describe the phenomenon to be modeled.

4. Data filtering: filter data that may not be relevant or available during production.

5. Exploratory data analysis: explore the data to gain insights.

# Top 3 data insights

1. 2 floor houses are 12% more expensive than 3 floor houses.

2. Prices are higher during the first semester.

3. Houses built between the 1940's and the 1960's are less expensive.

# Assumptions

Seasonality of the prices must be taken into account, and to reach the final expected return, it is assumed that the houses are sold at their highest price.

# Data product

The final result is presented as a dashboard (https://house-sales-analytics.herokuapp.com/) answering the questions:

1. Which houses to buy?

2. What is the best moment to sell?

3. What should be the selling price?

The group of houses selected demand an investment of $407,142,664.00, with a return of $122,142,799.20 (30%).

# Further improvements

The suggested selling price considers a 30% return over the buying price. The selling price of several houses are still below the average market price. Therefore, a further analysis could reveal an optimum selling price, maximizing the return.
