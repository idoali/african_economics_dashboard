import streamlit as st 
import pickle
import plotly.express as px
import pandas as pd
import numpy as np

data = pd.read_csv("data/african_economic.csv")

def get_data(df, x, y):
    dx = df[(df["Country and Regions Name"].isin(x)) & (df["Indicators Name"] == y)]
    return dx

def get_barplot(dx, y, year):
    d_tab = dx[["Country and Regions Name", str(year)]].sort_values(str(year), ascending = False)
    fig = px.bar(d_tab, x = "Country and Regions Name", y = str(year), labels = {str(year):y + " in " + str(year)})
    return fig

def get_lineplot(df, y):
    new_ds = df[df.columns[7:]].T
    new_ds.columns = df["Country and Regions Name"].values
    new_ds.reset_index(inplace = True)
    new_ds["index"] = np.int32(new_ds["index"])
    new_ds.rename(columns = {"index":"Year"}, inplace = True)
    new_ds = pd.melt(new_ds, id_vars = ["Year"], var_name = "Country", value_name = y)

    fig = px.line(new_ds, x = "Year", y = y, color = "Country")
    return fig

with open("data/text.p", "rb") as f:
    text = pickle.load(f)
    
explanation = text["explanation"]
countries = text["country"]
indicators = text["indicators"]

input_indicator = st.selectbox("Choose Parameter", indicators)
st.markdown(explanation)

col_1, col_2 = st.columns(2)

with col_1:
    input_country = st.multiselect("Choose Country", countries)
    
with col_2:
    input_year = st.number_input("Choose Year", 1980, 2020)
    
df = get_data(data, input_country, input_indicator)
fig_bar = get_barplot(df, input_indicator, input_year)
fig_line = get_lineplot(df, input_indicator)

st.plotly_chart(fig_bar)
st.plotly_chart(fig_line)
