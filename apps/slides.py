import streamlit as st


def app():



    slides = ["slides 1","slide 2","slide 3", "slide 4","slide 5"]

    option = st.sidebar.selectbox("Select your slide ", slides,key="my_side_slide_1")
    

    if option == slides[0]:
        st.image("./images/accenture-slide1.png")
    if option == slides[1]:
        st.image("./images/accenture-slide4.png")
    if option == slides[2]:
        st.image("./images/accenture-slide2.png")
    if option == slides[3]:
        st.image("./images/accenture-slide3.png")
    if option == slides[4]:
        st.image("./images/accenture-slide5.png")