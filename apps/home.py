from matplotlib.pyplot import autoscale
import streamlit as st
from Utils.request import Request
import pandas as pd
from Utils.figure import Figure
import plotly.express as px



def create_fig1(names,values):
    #values=values_list[0]
    #names=labels
        fig1 = px.pie(names=names,values=values,hole=0.6,height=200)
        fig1.add_annotation(
            text="2017",
            showarrow=False,
            font_size=50)
        fig1.layout.update(showlegend=False)
        fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        return fig1

def create_fig2(names,values):
    #values=values_list[1]
    #names=labels
    fig2 = px.pie(names=names,values=values,hole=0.6,height=200)
    fig2.add_annotation(
        text="2018",
        showarrow=False,
        font_size=50)
    fig2.layout.update(showlegend=False)
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig2


@st.cache
def create_fig3(names,values):
    #values=values_list[2]
    #names=labels
    fig3 = px.pie(names=names,values=values,hole=0.6,height=200)
    fig3.add_annotation(
        text="2019",
        showarrow=False,
        font_size=50)
    fig3.layout.update(showlegend=False)
    fig3.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig3


def app():

    @st.cache
    def create_class():
        request = Request()
        return request

    
    request = create_class()


    years = pd.Series([2017,2018,2019])
    restaurants = pd.Series(request.get_list_restaurant())
    my_head_choice = pd.Series([5,8,10,20,50,100])
    my_head_choice = my_head_choice.astype(int)

    orders_2017 = request.get_total_orders_by_years(2017)
    orders_2018 = request.get_total_orders_by_years(2018)
    orders_2019 = request.get_total_orders_by_years(2019)
    
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
    part_four = st.container()
    part_five = st.container()


    fig1 = create_fig3(labels,values=values_list[0])
    fig2 = create_fig3(labels,values=values_list[1])
    fig3 = create_fig3(labels,values=values_list[2])

    option = st.sidebar.selectbox('Data exploration', ('main','second'))


    if option == "main":
        with part_one:

            st.markdown("### Number of order per year")
            
            col_part_one1,col_part_one2,col_part_one3 = st.columns(3)


            #st.metric("Total Order", value, delta=None, delta_color="normal")
            #fig1 = figure.donut(labels,values_list[0])
            
            
            
        

            col_part_one1.plotly_chart(fig1,use_container_width=True)
            col_part_one2.plotly_chart(fig2,use_container_width=True)
            col_part_one3.plotly_chart(fig3,use_container_width=True)
            

            #col_part_one1.metric("Total 2017", orders_2017, delta=None, delta_color="normal")
            #col_part_one1.markdown(f"## {orders_2017}")
            col_part_one1.markdown(f"<h2 style='text-align: center; color: white;'>Total : {orders_2017:,}</h2>", unsafe_allow_html=True)
            col_part_one2.markdown(f"<h2 style='text-align: center; color: white;'>Total : {orders_2018:,}</h2>", unsafe_allow_html=True)
            col_part_one3.markdown(f"<h2 style='text-align: center; color: white;'>Total : {orders_2019:,}</h2>", unsafe_allow_html=True)


        with part_two:

            x='year'
            y='pop'

            restaurants = request.get_top_restaurant_order()
            fig5 = px.bar(restaurants, x="Restaurant", y="Number of order", color="Number of order")
        
            fig5.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False)),
                title={
                    'xanchor': 'center',
                    "text" : "Top 10 Restaurant"
                    }
            )
            fig5['layout']['title']['font'] = dict(size=20)
            #st.markdown(f"<h2 style='text-align: center; color: yellow;'>Total : Top 10 Restaurant</h2>", unsafe_allow_html=True)
            #part_two.markdown("<h2>Top 10 Restaurant</h2>", unsafe_allow_html=True)
            st.plotly_chart(fig5,use_container_width=True)

    else:

        with part_three:

            col_part_three1,col_part_three2= st.columns(2)

            year = 2017

            city = "New York"

            col_part_three1.markdown("## New York 2017")

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

            col_part_three2.markdown("## San Francisco 2017")

            new_data = request.get_number_order_by_city_by_year2(year,city)

            fig6 = px.bar(new_data, x="restaurant_name", y="count", color="restaurant_name")

            fig6.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )

            fig6.update_xaxes(visible=False, showticklabels=False)

            col_part_three2.plotly_chart(fig6,use_container_width=True)
            

        with part_four:

            col_part_four1,col_part_four2= st.columns(2)

            year = 2018

            city = "New York"

            col_part_four1.markdown("## New York 2018")

            new_data = request.get_number_order_by_city_by_year2(year,city)

            fig4 = px.bar(new_data, x="restaurant_name", y="count",color="restaurant_name")

            fig4.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )

            fig4.update_xaxes(visible=False, showticklabels=False)

            col_part_four1.plotly_chart(fig4,use_container_width=True)


            year = 2018

            city = "San Francisco"

            col_part_four2.markdown("## San Francisco 2018")

            new_data = request.get_number_order_by_city_by_year2(year,city)

            fig6 = px.bar(new_data, x="restaurant_name", y="count", color="restaurant_name")

            fig6.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )

            fig6.update_xaxes(visible=False, showticklabels=False)

            col_part_four2.plotly_chart(fig6,use_container_width=True)
            


        
        with part_five:

            col_part_five1,col_part_five2= st.columns(2)

            year = 2019

            city = "New York"

            col_part_five1.markdown("## New York 2019")

            new_data = request.get_number_order_by_city_by_year2(year,city)

            fig4 = px.bar(new_data, x="restaurant_name", y="count",color="restaurant_name")

            fig4.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )

            fig4.update_xaxes(visible=False, showticklabels=False)

            col_part_five1.plotly_chart(fig4,use_container_width=True)


            year = 2019

            city = "San Francisco"

            col_part_five2.markdown("## San Francisco 2019")

            new_data = request.get_number_order_by_city_by_year2(year,city)

            fig6 = px.bar(new_data, x="restaurant_name", y="count", color="restaurant_name")

            fig6.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )

            fig6.update_xaxes(visible=False, showticklabels=False)

            col_part_five2.plotly_chart(fig6,use_container_width=True)
            

            padding = 0
            st.markdown(f""" <style>
                .reportview-container .main .block-container{{
                    padding-top: {padding}rem;
                    padding-right: {padding}rem;
                    padding-left: {padding}rem;
                    padding-bottom: {padding}rem;
                }} </style> """, unsafe_allow_html=True)