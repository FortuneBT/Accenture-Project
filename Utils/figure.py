
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List,Dict
import plotly.express as px


class Figure():
    
    def donut(self, labels:List,values:List):
        
        my_layout = go.Layout({"showlegend": False})

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)],layout=my_layout)

        return fig

    def line(self,x,y):

        df = px.data.gapminder().query("continent=='Oceania'")
        fig = px.line(df, x=x, y=y, color='country')

        return fig


    def bar(self,x,y):
        data_canada = px.data.gapminder().query("country == 'Canada'")
        fig = px.bar(data_canada, x=x, y=y)

        return fig