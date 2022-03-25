import dash
from dash import Dash,dcc,html
import pandas
from Utils.request import Request
import plotly.express as px
from dash.dependencies import Input,Output


request = Request()
app = Dash()

opts = request.get_list_city()
my_options = []

for elem in opts:
    my_options.append({"label":elem,"value":elem})

year = 2019

city = "San Francisco"

new_data = request.get_number_order_by_city_by_year2(year,city)

fig6 = px.bar(new_data, x="restaurant_name", y="count", color="restaurant_name")

fig6.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

fig6.update_xaxes(visible=False, showticklabels=False)


app.layout = html.Div([
    html.Div(
        html.H1("Accenture Project")
    ),
    html.Div(
        dcc.Dropdown(id="mydropdown",options=my_options,placeholder="Select a city")
    ),
    html.Div(
        dcc.Graph(id="myfig1", figure=fig6)
    )
])



@app.callback(Output("myfig1","figure"),Input("mydropdown","value"))
def update_graph(city):

    new_data = request.get_number_order_by_city_by_year2(2017,city)
    print("CITY: ",city)
    print(new_data)
    fig6 = px.bar(new_data, x="restaurant_name", y="count", color="restaurant_name")

    fig6.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    fig6.update_xaxes(visible=False, showticklabels=False)

    return fig6               
        


app.run_server(debug=True)
