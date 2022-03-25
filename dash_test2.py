import dash
from dash import Dash,dcc,html
import pandas
from Utils.request import Request
import plotly.express as px
from dash.dependencies import Input,Output


request = Request()
app = Dash()

opts = request.get_list_city()
my_city_options = []
my_year_options = []
my_restaurant_options = []

for elem in opts:
    my_city_options.append({"label":elem,"value":elem})


opts = request.get_list_restaurant()
for elem in opts:
    my_restaurant_options.append({"label":elem,"value":elem})


opts = request.get_list_year()
for elem in opts:
    my_year_options.append({"label":elem,"value":elem})
request.year


app.layout = html.Div([
    html.Div([
        html.Div(),#logo
        html.Div(html.H1("Accenture Project")),#title
        html.Div()#date
    ]),# DIV 1
    html.Div(
        html.Div()
    ),# DIV 2
    html.Div([
        html.Div(
            html.Div([
                html.P("Total order"),
                html.P("1.256.456")
            ])
        ),#div 21
        html.Div(
            html.Div([
                html.P("Total revenue"),
                html.P("80.256.456")
            ])
        ),#div 22
        html.Div(
            html.Div([
                html.P("number of restaurant"),
                html.P("576")
            ])
        ),#div 23
        html.Div(
            html.Div([
                html.P("number of street"),
                html.P("346")
            ])
        )#div 24
    ]),# DIV 3
    html.Div([
        html.Div([
            html.P("Select your City"),
            dcc.Dropdown(id="MyCitySelection",options=my_city_options),
            dcc.Dropdown(id="MyrestaurantSelection",options=my_restaurant_options),
            dcc.Dropdown(id="MystreetSelection",options=my_year_options)
        ]),#first block to the left
        html.Div([
            html.Div([
                html.Div(),
                html.Div()
            ]),
            html.Div()
        ])
    ]
    )# DIV 4
])


app.run_server(debug=True)