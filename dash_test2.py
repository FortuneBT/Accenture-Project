import dash
from dash import Dash,dcc,html
import pandas
from Utils.request import Request
import plotly.express as px
from dash.dependencies import Input,Output


request = Request()
app = Dash()

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
        html.Div(),
        html.Div(),
        html.Div(),
        html.Div()
    ]),# DIV 3
    html.Div([
        html.Div(),
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