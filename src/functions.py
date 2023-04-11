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

df_TripAdvisor_total = pd.read_csv("../data/df_TripAdvisor_total_boroughs.csv")


# Manipulate the data
restaurant_types = ["European", "Mediterranean", "Asian", "Bar", "Cafe",
                     "International", "Latin", "South American", "Contemporary",
                     "Healthy", "Diner", "Wine bar", "Dining bars",
                     "Beer restaurants", "Fusion", "Eastern European", "Central Asian", "Central American",
                     "Pub", "Brew Pub", "Deli", "Gastropub", "Irish", "Central European", "Soups"]

df_TypeFiltered1 = df_TripAdvisor_total
for elem in ["Southern-Italian", "Pizza", "Neapolitan", "Welsh", "Tuscan", "Romana", "Campania"]:
    df_TypeFiltered1 = df_TypeFiltered1.replace({'Restaurant type 1': elem}, "Italian")
for elem in ["Catalan"]:
    df_TypeFiltered1 = df_TypeFiltered1.replace({'Restaurant type 1': elem}, "Spanish")
for elem in ["Sushi", "Japanese Fusion"]:
    df_TypeFiltered1 = df_TypeFiltered1.replace({'Restaurant type 1': elem}, "Japanese")
for elem in ["Pakistani"]:
    df_TypeFiltered1 = df_TypeFiltered1.replace({'Restaurant type 1': elem}, "Indian")
df_TypeFiltered1 = df_TypeFiltered1[~df_TypeFiltered1["Restaurant type 1"].isin(restaurant_types)]

df_TypeFiltered2 = df_TripAdvisor_total
for elem in ["Southern-Italian", "Pizza", "Neapolitan", "Welsh", "Tuscan", "Romana", "Campania"]:
    df_TypeFiltered2 = df_TypeFiltered2.replace({'Restaurant type 2': elem}, "Italian")
for elem in ["Catalan"]:
    df_TypeFiltered2 = df_TypeFiltered2.replace({'Restaurant type 2': elem}, "Spanish")
for elem in ["Sushi", "Japanese Fusion"]:
    df_TypeFiltered2 = df_TypeFiltered2.replace({'Restaurant type 2': elem}, "Japanese")
for elem in ["Pakistani"]:
    df_TypeFiltered2 = df_TypeFiltered2.replace({'Restaurant type 1': elem}, "Indian")
df_TypeFiltered2 = df_TypeFiltered2[~df_TypeFiltered2["Restaurant type 2"].isin(restaurant_types)]

df1 = df_TypeFiltered1.drop("Restaurant type 2", axis=1).rename({"Restaurant type 1" : "Restaurant type"}, axis=1)
df2 = df_TypeFiltered2.drop("Restaurant type 1", axis=1).rename({"Restaurant type 2" : "Restaurant type"}, axis=1)
df_final=pd.concat([df1,df2])


# dataframe with boroughs and coordinates:

list_boroughs = list(df_TripAdvisor_total["Boroughs"].dropna().unique()) 
list_coords = [(39.46516885263047, -0.37417109685013045), 
               (39.4728399547363, -0.37644089581541273), 
               (39.47811833162089, -0.3435258650105859), 
               (39.45300223498394, -0.3328957281348358), 
               (39.475690593048455, -0.36167987957402464), 
               (39.473092350983244, -0.3867381257508482), 
               (39.493497063678646, -0.3909488123046656), 
               (39.4873503529693, -0.35569593602803773), 
               (39.483508261889384, -0.37131711992897537), 
               (39.472248364286706, -0.39516055338001754), 
               (39.46310451105254, -0.34927758763390543), 
               (39.49572989507793, -0.366404999577168), 
               (39.449915688458624, -0.36035553099481404), 
               (39.48330952726673, -0.4032461331770456), 
               (39.447194222046264, -0.39090006698740554), 
               (39.43918900044102, -0.376327382847183), 
               (39.4958798850356, -0.4175568180556274), 
               (39.457207597088015, -0.4001000138795662)] 
coords =pd.DataFrame( {"Boroughs" : list_boroughs, "lat" : [list_coords[i][0] for i in range(len(list_coords))], 
                       "lon" : [list_coords[i][1] for i in range(len(list_coords))] }) 
 
df_bors = df_final.groupby("Boroughs")[["Restaurant type"]].count().reset_index() 
df_bors = df_bors.merge(df_final.groupby("Boroughs", as_index=False)["Population"].mean())
df_bors["restaurants per 10k residents"] = df_bors["Restaurant type"]/ df_bors["Population"]*10000
df_bors = df_bors.drop(["Restaurant type", "Population"], axis=1)
df_bors_coords = df_bors.merge(coords, how = "inner")

#coordinates of Moroccan, Polish and Korean restaurants

coords_myrests = [(39.47859464995849, -0.38602487151089016),
                  (39.47243222641176, -0.371598415844762),
                  (39.47680845183803, -0.35006117166723877),
                  (39.46964086510725, -0.35625845817387614),
                  (39.47218205467545, -0.3716162735157179),
                  (39.46155107745301, -0.3758514888579189),
                  (39.47346826486452, -0.37049794145974096),
                  (39.471058357083315, -0.34717207536410144),
                  (39.47314526858856, -0.3710351296228373),
                  (39.45903836755602, -0.36851057351608635),
                  (39.47267230791354, -0.3503377158447549),
                  (39.464957184286014, -0.3644474716675471),
                  (39.480878127654, -0.40325528975873987),
                  (39.46959973113276, -0.3580731041996127),
                  (39.469897937505905, -0.3485787012061273),
                  (39.463174972206, -0.3760343102999674),
                  (39.47377814740199, -0.3469219594278099),
                  (39.46279603946376, -0.37376297166761324),
                  (39.46322937570005, -0.394583758174035),
                  (39.467089406989224, -0.39241569157865397),
                  (39.48521160511, -0.3639519330346634),
                  (39.46633208861474, -0.38795586002229293) 
                  ]
df_coords_myrests = pd.DataFrame({"lat" : [coords_myrests[i][0] for i in range(len(coords_myrests))],
                                 "lon" : [coords_myrests[i][1] for i in range(len(coords_myrests))]}, 
                                 index= df_final[df_final["Restaurant type"].isin(["Polish", "Korean", "Moroccan"])].index)

df_myrests_coords = df_final[df_final["Restaurant type"].isin(["Polish", "Korean", "Moroccan"])][["Restaurant type"]].merge(df_coords_myrests, left_index=True, right_index=True)



def map_boroughs(df_bors_coords):
    map = folium.Map(location=[39.46, -0.36], zoom_start=13, tiles='CartoDB Positron')

    for i in range(0,len(df_bors_coords)):
        folium.CircleMarker(
            location=[df_bors_coords["lat"].iloc[i], df_bors_coords["lon"].iloc[i]],
            tooltip=(df_bors_coords.iloc[i]['Boroughs'], float(df_bors_coords.iloc[i]["restaurants per 10k residents"])),
            radius=float(df_bors_coords.iloc[i]["restaurants per 10k residents"]/5),
            color='rgba(0,100,240,0.7)',
            fill=True,
            fill_color='#69b3a2'
        ).add_to(map)
    legend_html = '''
        <div style=" position: fixed;
                    bottom: 250px; left: 50px; width: 170px; height: 320px;
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color:white;
                    "> <br>
                    &nbsp; <b> 200 </b> &nbsp; <svg height="110" width="110">
                                        <circle cx="55" cy="55" r="40" stroke='rgba(0,100,240,0.7)' stroke-width="2" fill="#69b3a2" /></svg><br>
                    &nbsp; <b> 100 </b> &nbsp; <svg height="100" width="110">
                                        <circle cx="50" cy="50" r="20" stroke='rgba(0,100,240,0.7)' stroke-width="2" fill="#69b3a2" /></svg><br>
                    &nbsp; <b> 50 </b> &nbsp; <svg height="30" width="110">
                                        <circle cx="55" cy="15" r="10"stroke='rgba(0,100,240,0.7)' stroke-width="2" fill="#69b3a2" /></svg><br><br>
                    &nbsp; <b> 25 </b> &nbsp; &nbsp; <svg height="30" width="110">
                                        <circle cx="45" cy="15" r="5"stroke='rgba(0,100,240,0.7)' stroke-width="2" fill="#69b3a2" /></svg>

        </div>
        '''
    map.get_root().html.add_child(folium.Element(legend_html))
    st_map = st_folium(map, width=900, height=600)

def mean_median_nRevies(df_TripAdvisor_total):

    df_reviews_borough = df_TripAdvisor_total.groupby("Boroughs")["Number of reviews"].describe().reset_index().sort_values(by="mean")
    layout = go.Layout( width=700, height=700,
        title='Mean and median number of reviews by neighbourhood',
        xaxis=dict(title='Number of reviews'),
        yaxis=dict(title='Neighbourhood'),
    )
    fig = go.Figure(layout=layout)
    fig.add_trace( go.Bar(
                y=df_reviews_borough["Boroughs"],
                x=df_reviews_borough["mean"],
                name="Mean",
                marker = dict(
                            line = dict(color='rgb(0,0,0)', width = 1.5)),
                            orientation = "h"
                #text = data.keys()
                )
    )
    fig.add_trace( go.Bar(
                y=df_reviews_borough["Boroughs"],
                x=df_reviews_borough["50%"],
                name="Median",
                marker = dict(
                            line = dict(color='rgb(0,0,0)', width = 1.5)),
                            orientation = "h"
                #text = data.keys()
                )
    )
    st.plotly_chart(fig)

def map_myrests(df_myrests_coords):
    icon_polish = "https://cdn-icons-png.flaticon.com/512/6914/6914647.png"
    icon_moroccan = "https://cdn-icons-png.flaticon.com/512/2714/2714078.png"
    icon_korean = "https://cdn-icons-png.flaticon.com/512/8887/8887136.png"
    map_myrests = folium.Map(location=[39.47, -0.37], zoom_start=14, tiles='CartoDB Positron')

    for i in range(0,len(df_myrests_coords)):
        if df_myrests_coords["Restaurant type"].iloc[i] == "Moroccan":
            icon = folium.features.CustomIcon(icon_moroccan, icon_size=(35,35))
        elif df_myrests_coords["Restaurant type"].iloc[i] == "Polish":
            icon = folium.features.CustomIcon(icon_polish, icon_size=(35,35))
        elif df_myrests_coords["Restaurant type"].iloc[i] == "Korean":
            icon = folium.features.CustomIcon(icon_korean, icon_size=(35,35))

        folium.Marker(location=[df_myrests_coords["lat"].iloc[i], df_myrests_coords["lon"].iloc[i]],
                    tooltip = df_myrests_coords["Restaurant type"].iloc[i],
                    icon=icon).add_to(map_myrests)
    # add legend to the map
    legend_html = f'''
        <div style=" position: fixed;
                    bottom: 50px; left: 50px; width: 120px; height: 90px;
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color:#ABBAEA;;
                    ">&nbsp; <b> Polish  </b> &nbsp; &nbsp; &nbsp; &nbsp; <img src="{icon_polish}" width="25" height="25"><br>
                    &nbsp; <b> Moroccan </b> &nbsp; <img src="{icon_moroccan}" width="25" height="25"><br>
                    &nbsp; <b> Korean  </b> &nbsp; &nbsp; &nbsp;  <img src="{icon_korean}" width="25" height="25">
        </div>
        '''
    map_myrests.get_root().html.add_child(folium.Element(legend_html))
    st_map = st_folium(map_myrests, width=900, height=600)

def sankey_myrests(df_final):
    my_rests = ["Polish", "Moroccan", "Korean"]
    df_myrests = df_final[df_final["Restaurant type"].isin(my_rests)]
    df_myrests = df_myrests.groupby(["Restaurant type", "Boroughs"])[["Restaurant name"]].count().reset_index()
    df_myrests = df_myrests.rename({"Restaurant name" : "Count", "Restaurant type" : "Source", "Boroughs" : "Dest"}, axis=1)
    plot = hv.Sankey(df_myrests)
    colors = ["rgba(255, 105, 97,0.7)",
    "rgba(255, 180, 128,0.7)",
    "rgba(248, 243, 141,0.7)",
    "rgba(66, 214, 164,0.7)",
    "rgba(8, 202, 209,0.7)",
    "rgba(89, 173, 246,0.7)",
    "rgba(157, 148, 255,0.7)",
    "rgba(199, 128, 232,0.7)"]
    plot.opts(edge_color='Source', node_color='Dest',cmap='Set1', node_sort = True,
                edge_hover_fill_color="rgba(0, 0, 0,0.3)", label_text_font_size = "10pt")
    st.bokeh_chart(hv.render(plot, backend='bokeh'))
