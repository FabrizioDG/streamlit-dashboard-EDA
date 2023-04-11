import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import folium # pip install folium
from folium import plugins
from streamlit_folium import st_folium

import plotly.graph_objects as go

import holoviews as hv
from holoviews import opts, dim
hv.extension('bokeh')

#Add the folder where the functions for gradient descent are implemented
import sys
sys.path.insert(1, 'src')
from functions import *

st.set_page_config(
    page_title = "Restaurants in Valencia",
    page_icon = "🍽️",
    layout = "wide"

)



col1, col2, col3 = st.columns([1,5,1])
with col2:
    st.image("https://i.pinimg.com/originals/bf/65/d5/bf65d51f34b1bf193ec947f3c0c3f3e0.jpg")
    st.markdown("<h1 style='text-align: center; color: black;'>EDA on restaurants in Valencia</h1>", unsafe_allow_html=True)
    #st.title()


option = st.sidebar.selectbox("Select the view", ("Home", "Number of restaurants by boroughs",
                                                 "Mean and median number of reviews by boroughs",
                                                  "Map of my chosen restaurants",
                                                  "Sankey diagram"))
st.sidebar.write(option)


if option=="Home":
    st.subheader("Home")

    with st.expander("App details - click to show"):
        st.write(""" This website shows some of the visualizations for the Exploratory Data Analysis project
                    on restaurants in Valencia.
                    """)
    st.write(df_TripAdvisor_total)


elif option=="Number of restaurants by boroughs":
    st.subheader("Number of restaurants by boroughs")

    # map
    map_boroughs(df_bors_coords)




elif option=="Mean and median number of reviews by boroughs":
    st.subheader("Mean and median number of reviews by boroughs")
    mean_median_nRevies(df_TripAdvisor_total)

elif option=="Map of my chosen restaurants":
    st.subheader("Map of Moroccan, Polish and Korean restaurants")
    map_myrests(df_myrests_coords)


elif option=="Sankey diagram":
    st.subheader("Sankey diagram")
    sankey_myrests(df_final)

