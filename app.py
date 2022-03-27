import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from multiapp import MultiApp
from apps import home, description,team,revenue,slides # import your app modules here


st.set_page_config(layout="wide")

app = MultiApp()


header = st.container()
part_one = st.container()


# Add all your application here
app.add_app("Orders", home.app)
app.add_app("Revenue", revenue.app)
app.add_app("Description", description.app)
app.add_app("Team", team.app)
app.add_app("Slides", slides.app)

with header:

    col_header1,col_header2,col_header3,col_header4 = st.columns(4)

    col_header1.title("Project Accenture")

    # The main app
    app.run()

    




hide_st_style = """
            <style>
            .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
            
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style,unsafe_allow_html=True)


