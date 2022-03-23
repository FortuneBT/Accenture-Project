import streamlit as st
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def app():

    st.title('Description')
    
    st.header("Our goal")
    st.markdown("Accenture has been asked to provide an E2E (end-to-end) Data Solution for you")
    st.markdown("Your restaurant chain is spread accros The East coast and the West coast and all the restaurant are in either San Fransisco or New York.")
    st.markdown("Our team found some insights on your Data and we would like to share them with you")
    st.markdown("we hope that those insights would be able to provide you information to help you to make relevant business decisions.")

 
    st.header("Our process")

    st.markdown("Do some research")
    st.markdown("Cleaning of the data provided")
    st.markdown("Preprocess the data")
    st.markdown("Do the exploration of the data")
    st.markdown("Build a Dashboard using a Data Visualization tool")

    


        
