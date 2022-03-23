from urllib import request
import streamlit as st
from Utils.request import Request
import plotly.graph_objects as go
import pandas as pd
from Utils.figure import Figure


request = Request()

option = st.sidebar.selectbox('Data Exploration', ('Revenue Per City','List Expensive Dishes'))

df_dishes = request.least_expensive_dishes()
df_citys = request.revenue_cities()

if option == 'Revenue Per City':

    countries=[df_citys['city'][0] + " $", df_citys['city'][1] + " $"]
    values = [df_citys['real_price'][0], df_citys['real_price'][1]]

    fig = go.Figure(go.Pie(labels = countries, values = values, hoverinfo = "label+percent",
        textinfo = "value", ))
    fig.update_layout( autosize=False, width=700, height=600)

    st.header("Pie chart")
    st.plotly_chart(fig)

    request.revenue_cities

if option == 'List Expensive Dishes':

    st.write("pass")
