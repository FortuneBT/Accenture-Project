
import dash
from dash import Dash,dcc,html
import pandas
from Utils.request import Request
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input,Output


request = Request()
app = Dash()

opts = request.get_list_city()
my_city_options = []
my_year_options = []
my_restaurant_options = []

total_orders = request.get_number_order()
total_revenue = request.get_total_revenue()
total_restaurant = request.get_total_number_of_restaurant()
total_street = request.get_total_number_of_street()


my_city_options.append({"label":"Every cities","value":0})
for elem in opts:
    my_city_options.append({"label":elem,"value":elem})


my_restaurant_options.append({"label":"Every restaurants","value":0})
opts = request.get_list_restaurant()
for elem in opts:
    my_restaurant_options.append({"label":elem,"value":elem})


my_year_options.append({"label":"Every years","value":0})
opts = request.get_list_year()
for elem in opts:
    my_year_options.append({"label":elem,"value":elem})


df_order_cities = request.get_total_orders_cities()
df_top_10_restaurant = request.get_top_restaurant_order()

fig1 = px.pie(df_order_cities, values='Total orders', names='city',hole=.6)
fig1.update_layout(margin=dict(l=50, r=50, t=50, b=50))
fig1.update_layout({"plot_bgcolor":"rgba(0,0,0,0)","paper_bgcolor":"rgba(0,0,0,0)"})

fig2 = px.bar(df_top_10_restaurant, x="Restaurant", y="Number of order", color="Number of order")
fig2.update_layout(margin=dict(l=30, r=30, t=20, b=20))

fig3 = go.Figure()
#fig3.add_trace(go.Bar(x=years,y="",marker_color='rgb(55, 83, 109)'))
#fig3.add_trace(go.Bar(x=years,y="",marker_color='rgb(26, 118, 255)'))


app.layout = html.Bdo(html.Div([
    html.Div([
        html.Div(),#logo
        html.Div(html.H2("Accenture Project")),#title
        html.Div()#date
    ]),# DIV 1
    html.Div(
        html.Div()
    ),# DIV 2
    html.Div([
        html.Div(
            html.Div([
                html.P("Total order"),
                html.P(f"{total_orders:,}",className="squareNumber")
            ])
        ,id="square1",className="squareDiv3"),#div 31
        html.Div(
            html.Div([
                html.P("Total revenue"),
                html.P(f"{total_revenue:,} $",className="squareNumber")
            ])
        ,id="square2",className="squareDiv3"),#div 32
        html.Div(
            html.Div([
                html.P("number of restaurant"),
                html.P(total_restaurant,className="squareNumber")
            ])
        ,id="square3",className="squareDiv3"),#div 33
        html.Div(
            html.Div([
                html.P("number of street"),
                html.P(total_street,className="squareNumber")
            ])
        ,id="square4",className="squareDiv3")#div 34
    ],className="Div3"),# DIV 3
    html.Div([
        html.Div([  
            html.P("Select your City"),
            dcc.Dropdown(id="MyCitySelection",options=my_city_options,className="selectionChange",style={"color":"red"},value="Every Cities"),
            html.P("Select your restaurant"),
            dcc.Dropdown(id="MyrestaurantSelection",options=my_restaurant_options,className="selectionChange",value="Every restaurants"),
            html.P("Select your year"),
            dcc.Dropdown(id="MystreetSelection",options=my_year_options,className="selectionChange",value="Every years"),
            dcc.Graph(id="myfig1",figure=fig1,style={"width":"500px","margin-top":"5%"})
        ],id="blockleft"),#first block to the left
        html.Div([
            html.Div([
                html.Div(
                    dcc.Graph(id="myfig2",figure=fig2,style={"width":"500px","height":"200px","margin-top":"2%"})
                ),#top left from the part above from the right part
                html.Div()#top right from the part above from the right part 
            ]),
            html.Div()#bottom from the right part 
        ],id="blockright")
    ]
    ,className="Div4")# DIV 4
],id="dash"))



app.run_server(debug=True)