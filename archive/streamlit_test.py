from numpy import empty
import streamlit as st
from Utils.request import Request
import pandas as pd


request = Request()

year = pd.Series([2017,2018,2019])
restaurants = pd.Series(request.get_list_restaurant())
my_head_choice = pd.Series([5,8,10,20,50,100])
my_head_choice = my_head_choice.astype(int)

part_one = st.container()
part_two = st.container()


with part_one:

    st.title("Group 7 : Project Accenture")
    
    st.header("Revenue by restaurant by year")

    selection = st.selectbox("What year do you need ? ",year,key="selection_restaurant_1")

    head_choice = st.selectbox("How much do you want to see ? ",my_head_choice,key="selection_head_choice_1")

    result = request.revenue_restaurants_year(selection).head(head_choice)

    st.write(result)


with part_two:
    
    st.header("Revenue by restaurant by year")

    s_restaurant = st.selectbox("Wich restaurant ? ",restaurants,key="selection_restaurant_2")

    s_year = st.selectbox("What year do you need ? ",year,key="selection_year_2")

    result = request.revenue_restaurant_year_by_month(s_restaurant,s_year)

    st.table(result)
    
    st.write(type(result))