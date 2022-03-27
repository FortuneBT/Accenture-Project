from urllib import request
import streamlit as st
from Utils.request import Request
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import altair as alt

def app():

    @st.cache
    def create_class():
        request = Request()
        return request

    request = create_class()

    option = st.sidebar.selectbox('Data exploration', ('Over all revenue','Per year'))

    df_citys = request.revenue_cities()
    df_restaurants = request.revenue_restaurants().head(10)
    df_streets = request.revenue_streets()
    df_dishes = request.least_expensive_dishes()

    if option == 'Over all revenue':

        countries=[df_citys['city'][0] + " $", df_citys['city'][1] + " $"]
        values = [df_citys['real_price'][0], df_citys['real_price'][1]]
        fig1 = go.Figure(go.Pie(labels = countries, values = values, hoverinfo = "label+percent",
        textinfo = "value" ))

        fig1.update_layout( autosize=False, width=700, height=500)
        st.header("Over all revenue per city")
        st.plotly_chart(fig1)

        fig2 = px.bar(df_restaurants, x =df_restaurants['restaurant_name'], y =df_restaurants['real_price'], 
        color=df_restaurants['restaurant_name'])
        fig2.update_layout( autosize=False, width=800, height=600)

        st.header("The top 10 restaurants over all revenue")
        st.plotly_chart(fig2)


        fig3 = px.line(df_streets.head(10), x="street", y="real_price", color="street", text="street")
        fig3.update_layout( autosize=False, width=800, height=600)
        st.header("The top 10 streets over all revenue")
        st.plotly_chart(fig3, use_container_width=False)

        labels = request.restaurant['name'].tail(10).to_list()
        sizes = [5, 10, 15, 3, 5, 10, 15, 3, 15, 3]

        st.header("The 10 most expensive  dishes")
        fig4, ax1 = plt.subplots()
        
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig4)


    if option == 'Per year':

        year = pd.Series([2017,2018,2019])
        restaurant = pd.Series(request.get_list_restaurant())
        st.header("Restaurants revenue per year")
        s_restaurant = st.sidebar.selectbox("Select restaurant name ? ",restaurant,key="selection_restaurant_2")
        s_year = st.sidebar.selectbox("Select year ? ",year,key="selection_year_2")
        df_months = request.revenue_restaurant_year_by_month(s_restaurant,s_year)

        fig = px.bar(df_months, x='Month', y='revenue ($)',
        hover_data=['Month', 'revenue ($)'], color='Month',
        labels={'pop':'population of Canada'}, height=400)
        st.plotly_chart(fig)

        df_streets_revenue = request.revenue_streets_year(s_year)

        fig3 = px.line(df_streets_revenue.head(10), x="street", y="real_price", color="street", text="street")
        fig3.update_layout( autosize=False, width=800, height=600)
        st.header(f"The top 10 streets {s_year} revenue")
        st.plotly_chart(fig3, use_container_width=True)
        
    

