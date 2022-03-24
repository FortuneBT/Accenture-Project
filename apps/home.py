from matplotlib.pyplot import autoscale
import streamlit as st
from Utils.request import Request
import pandas as pd
from Utils.figure import Figure
import plotly.express as px

def app():

    @st.cache
    def create_class():
        request = Request()
        return request


    request = create_class()
    figure = Figure()

    years = pd.Series([2017,2018,2019])
    restaurants = pd.Series(request.get_list_restaurant())
    my_head_choice = pd.Series([5,8,10,20,50,100])
    my_head_choice = my_head_choice.astype(int)

    labels = request.get_list_city()
    new_york = labels[1]
    san_francisco = labels[0]

    values_list = []

    for year in years:
        
        orders1 = request.get_number_order_by_city_by_year1("San Francisco",year)
        orders2 = request.get_number_order_by_city_by_year1(new_york,year)
        values_list.append([orders1, orders2])

    

    part_one = st.container()
    part_two = st.container()
    part_three = st.container()


    with part_one:

        st.markdown("### Number of order per year")
        
        col_part_one1,col_part_one2,col_part_one3 = st.columns(3)

        fig1 = figure.donut(labels,values_list[0])
        fig2 = figure.donut(labels,values_list[1])
        fig3 = figure.donut(labels,values_list[2])

        fig1.add_annotation(
            text="2017",
            showarrow=False,
            font_size=50)

        padding = 0     

        st.markdown(f""" <style>
            .reportview-container .main .block-container{{
                padding-top: {padding}rem;
                padding-right: {padding}rem;
                padding-left: {padding}rem;
                padding-bottom: {padding}rem;
            }} </style> """, unsafe_allow_html=True)

        fig2.add_annotation(
            
            text="2018",
            showarrow=False,
            font_size=50)

        fig3.add_annotation(
            text="2019",
            showarrow=False,
            font_size=50)

        col_part_one1.plotly_chart(fig1,use_container_width=True)

        

        col_part_one2.plotly_chart(fig2,use_container_width=True)
        col_part_one3.plotly_chart(fig3,use_container_width=True)
       

    with part_two:

        x='year'
        y='pop'

        restaurants = request.get_top_restaurant_order()
        fig5 = px.bar(restaurants, x="Restaurant", y="Number of order")
       
        fig5.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        st.plotly_chart(fig5,use_container_width=True)

    with part_three:

        col_part_three1,col_part_three2= st.columns(2)

        year = 2017

        city = "New York"

        col_part_three1.markdown("## New York")

        new_data = request.get_number_order_by_city_by_year2(year,city)

        fig4 = px.bar(new_data, x="restaurant_name", y="count",color="restaurant_name")

        fig4.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        fig4.update_xaxes(visible=False, showticklabels=False)

        col_part_three1.plotly_chart(fig4,use_container_width=True)


        year = 2017

        city = "San Francisco"

        col_part_three2.markdown("## San Francisco")

        new_data = request.get_number_order_by_city_by_year2(year,city)

        fig6 = px.bar(new_data, x="restaurant_name", y="count", color="restaurant_name")

        fig6.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        fig6.update_xaxes(visible=False, showticklabels=False)

        col_part_three2.plotly_chart(fig6,use_container_width=True)
        