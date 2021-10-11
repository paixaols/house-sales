# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

plt.style.use('bmh')

def load_data(fname):
    df1 = pd.read_csv(fname)
    new_cols = ['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living', 
                'sqft_lot', 'floors', 'water_front', 'view', 'condition', 
                'grade', 'sqft_above', 'sqft_basement', 'yr_built', 
                'yr_renovated', 'zipcode', 'lat', 'long', 'sqft_living15', 
                'sqft_lot15']
    df1.columns = new_cols
    df1['date'] = pd.to_datetime(df1['date'])
    return df1

def feature_engineering(df2):
    df2['month'] = df2['date'].apply(lambda x: x.month)
    df2['renovated'] = df2['yr_renovated'].apply(lambda x: 1 if x > 0 else 0)
    df2['price_per_living_sqft'] = df2['price']/df2['sqft_living']
    df2['price_per_lot_sqft'] = df2['price']/df2['sqft_lot']
    return df2

def data_filtering(df3):
    drop_cols = ['sqft_living15', 'sqft_lot15']
    df3.drop(drop_cols, axis = 1, inplace = True)
    return df3

def data_manipulation(df5):
    aux = df5[['zipcode', 'price']].groupby('zipcode').median().reset_index()
    aux.rename(columns = {'price': 'median_price'}, inplace = True)
    df5 = df5.merge(aux, how = 'left', on = 'zipcode')
    df5 = df5[['id', 'date', 'month', 'price', 'price_per_living_sqft', 
               'price_per_lot_sqft','zipcode','median_price', 
               'condition', 'grade','bedrooms', 'bathrooms', 
               'sqft_living','sqft_lot', 'sqft_above', 'sqft_basement', 
               'floors', 'water_front', 'view', 'yr_built', 
               'yr_renovated', 'lat', 'long']]
    # What to buy?
    df5['buy'] = df5.apply(lambda x: 1 if (x['price'] < x['median_price']) and 
                                          (x['condition'] > 3) and 
                                          (x['grade'] > 7) 
                                       else 0, 
                           axis = 1)
    # When to sell?
    aux1 = df5[['month', 'zipcode', 'price']].groupby(['zipcode', 'month']).median().reset_index()
    aux2 = aux1.groupby('zipcode').max().reset_index()
    aux2['month'] = aux2.apply(lambda x: aux1.loc[(aux1['zipcode'] == x['zipcode']) & 
                                                  (aux1['price'] == x['price']), 'month'].iloc[0], 
                               axis = 1)
    aux2.rename(columns = {'month': 'high_month', 'price': 'high_median_price'}, 
                inplace = True)
    df5 = df5.merge(aux2, how = 'left', on = 'zipcode')
    # For how much?
    df5['sell_price'] = df5.apply(lambda x: -1 if x['buy'] == 0 
                                  else x['price']*1.1 
                                  if x['price'] > x['high_median_price'] 
                                  else x['price']*1.3, axis = 1)
    df5['profit'] = df5.apply(lambda x: x['sell_price']-x['price'], axis = 1)
    return df5

# =============================================================================
# Load and prepare data
# =============================================================================
df1 = load_data('kc_house_data.csv')
df2 = feature_engineering(df1)
df3 = data_filtering(df2)
df5 = data_manipulation(df3)
cols = ['id', 
        'date', 
        # 'month', 
        'price', 
        'sell_price', 
        'profit', 
        'high_month', 
        # 'price_per_living_sqft', 
        # 'price_per_lot_sqft', 
        'zipcode', 
        # 'median_price', 
        'condition', 
        'grade', 
        'bedrooms', 
        'bathrooms', 
        'sqft_living', 
        'sqft_lot', 
        'sqft_above', 
        'sqft_basement', 
        'floors', 
        'water_front', 
        'view', 
        'yr_built', 
        'yr_renovated', 
        'lat', 
        'long']
        # 'buy', 
        # 'high_median_price']
# Further tweaks
buy_recom = df5.loc[df5['buy'] == 1, cols]
buy_recom['date'] = buy_recom['date'].apply(lambda x: x.date())
buy_recom.rename(columns = {'high_median_price': 'high_month_median_price', 
                            'sell_price': 'recom sell price', 
                            'profit': 'expected return', 
                            'high_month': 'recom sell month'}, 
                 inplace = True)

st.title('Houses recomendation')

# =============================================================================
# Map
# =============================================================================
st.header('Map')
min_price = int(buy_recom['price'].min()/1000)
max_price = int(buy_recom['price'].max()/1000)+1
low_price, high_price = st.slider('Price range (x 1000)', 
                                  min_value = min_price, 
                                  max_value = max_price, 
                                  value = (min_price, max_price))
low_price *= 1000
high_price *= 1000
st.write('View prices between ${:,.2f} and $ {:,.2f}'.format(low_price, high_price))

filtered_houses = buy_recom[(buy_recom['price'] >= low_price) & (buy_recom['price'] <= high_price)]

fig = px.scatter_mapbox(filtered_houses, 
                        lat = 'lat', lon = 'long', 
                        hover_name = 'id', 
                        hover_data = ['price', 'grade', 'condition'], 
                        color = 'price', 
                        zoom = 9, 
                        height = 300)
fig.update_layout(mapbox_style = 'open-street-map', 
                  height = 600, 
                  margin = {'r': 0, 't': 0, 'l': 0, 'b': 0})
st.plotly_chart(fig)

# =============================================================================
# Show dataset
# =============================================================================
st.header('Recomended houses')
investment = filtered_houses['price'].sum()
st.write('Investment $ {:,.2f}'.format(investment))

profit = filtered_houses['expected return'].sum()
st.write('Expected return $ {:,.2f} ({:.1f}%)'.format(profit, 100*profit/investment))

st.write(filtered_houses)

# =============================================================================
# Analytics
# =============================================================================
st.header('Analytics')
zipcode = st.selectbox('Zipcode', sorted(df5['zipcode'].unique()))
aux = df5[df5['zipcode'] == zipcode]
aux['price'] = aux['price']/1000

st.write('Average price $ {:,.2f} k'.format(aux['price'].mean()))

# Price
fig, axs = plt.subplots(ncols = 2)
sns.histplot(data = aux, x = 'price', ax = axs[0])
sns.histplot(data = aux, x = 'price_per_living_sqft', ax = axs[1])

axs[0].set_xlabel('Price ($ thousand)')
axs[0].set_ylabel('Count')
axs[1].set_xlabel('Price / living sqft ($)')
axs[1].set_ylabel('Count')
fig.tight_layout()
st.pyplot(fig)

# Bedrooms & floors
aux1 = df5[df5['zipcode'] == zipcode]
aux1['price'] = aux1['price']/1000

fig, axs = plt.subplots(ncols = 2)

aux2 = aux1[['bedrooms', 'price']].groupby('bedrooms').mean().reset_index()
sns.barplot(data = aux2, x = 'bedrooms', y = 'price', 
            ax = axs[0], palette = 'winter')

aux2 = aux1[['floors', 'price']].groupby('floors').mean().reset_index()
sns.barplot(data = aux2, x = 'floors', y = 'price', 
            ax = axs[1], palette = 'winter')

axs[0].set_xlabel('Bedrooms')
axs[0].set_ylabel('Average price ($ thousand)')
axs[1].set_xlabel('Floors')
axs[1].set_ylabel('Average price ($ thousand)')
fig.tight_layout()
st.pyplot(fig)
