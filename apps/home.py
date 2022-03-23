from matplotlib.pyplot import autoscale
import streamlit as st
from Utils.request import Request
import pandas as pd
from Utils.figure import Figure

def app():

    request = Request()

    figure = Figure()



    years = pd.Series([2017,2018,2019])
    restaurants = pd.Series(request.get_list_restaurant())
    my_head_choice = pd.Series([5,8,10,20,50,100])
    my_head_choice = my_head_choice.astype(int)

    labels = request.get_list_city()
    new_york = labels[1]
    san_fransisco = labels[0]
    year = 2017
    orders1 = request.get_number_order_by_city_by_year(san_fransisco,year)
    orders2 = request.get_number_order_by_city_by_year(new_york,year)
    values = [orders1, orders2]
    st.write(san_fransisco)
    

    part_one = st.container()
    part_two = st.container()


    with part_one:

        col_part_one1,col_part_one2,col_part_one3 = st.columns(3)

        fig1 = figure.donut(labels,values)
        fig2 = figure.donut(labels,values)
        fig3 = figure.donut(labels,values)

        """fig1.update_layout(
            annotations=[dict(text='2017', x=0.18, y=0.5, font_size=20, showarrow=False)],
            
        )"""
        
        fig1.add_annotation(
            text="2017",
            showarrow=False,
            font_size=50)


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

        col_part_two1,col_part_two2= st.columns(2)

        x = "year"
        y = "lifeExp"

        fig4 = figure.line(x,y)
        fig4.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        col_part_two1.plotly_chart(fig4,use_container_width=True)

        x='year'
        y='pop'

        fig5 = figure.bar(x,y)
        fig5.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        col_part_two2.plotly_chart(fig5,use_container_width=True)
    

        