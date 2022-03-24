import streamlit as st
from Utils.request import Request
import pandas as pd
from Utils.figure import Figure

def app():

    request = Request()

    figure = Figure()



    year = pd.Series([2017,2018,2019])
    restaurants = pd.Series(request.get_list_restaurant())
    my_head_choice = pd.Series([5,8,10,20,50,100])
    my_head_choice = my_head_choice.astype(int)

    labels = ['New York','San Fransisco']
    values = [4500, 2500]
    
    

    part_one = st.container()
    part_two = st.container()


    with part_one:


        col_part_one1,col_part_one2,col_part_one3 = st.columns(3)

        fig1 = figure.donut(labels,values)
        fig2 = figure.donut(labels,values)
        fig3 = figure.donut(labels,values)

        col_part_one1.plotly_chart(fig1,use_container_width=True)
        col_part_one2.plotly_chart(fig2,use_container_width=True)
        col_part_one3.plotly_chart(fig3,use_container_width=True)


    with part_two:

        col_part_two1,col_part_two2= st.columns(2)

        x = "year"
        y = "lifeExp"

        fig4 = figure.line(x,y)
        
        col_part_two1.plotly_chart(fig4,use_container_width=True)

        x='year'
        y='pop'

        fig5 = figure.bar(x,y)

        col_part_two2.plotly_chart(fig5,use_container_width=True)
    

        