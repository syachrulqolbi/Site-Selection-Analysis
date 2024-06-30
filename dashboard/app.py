import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import panel as pn
import streamlit.components.v1 as components
import geohashlite
import json
import math
import os
from supabase import create_client, Client

os.environ["SUPABASE_URL"] = "https://uukvdqiqgagwvzvqkoaw.supabase.co"
os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1a3ZkcWlxZ2Fnd3Z6dnFrb2F3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg1MDE1NzgsImV4cCI6MjAzNDA3NzU3OH0.CMFtfu5KdlCYaq8_si0khmKap0ydcDTIE_m_bTfhoak"
os.environ["SUPABASE_KEY_MASTER"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1a3ZkcWlxZ2Fnd3Z6dnFrb2F3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxODUwMTU3OCwiZXhwIjoyMDM0MDc3NTc4fQ.hDba_swUBO5mfoqFZkzL1MNDdKCKXDZ2oiKGCL_EhZM"

supabase: Client = create_client(os.environ.get("SUPABASE_URL"), 
                                 #os.environ.get("SUPABASE_KEY"),
                                 os.environ.get("SUPABASE_KEY_MASTER"),)

url = os.getcwd()

img_url = "https://img.icons8.com/?size=100&id=gD6jY1ZThEJD&format=png&color=000000"

st.set_page_config(
    page_title="Site Selection Analysis",
    page_icon=img_url,
    layout="wide",
    initial_sidebar_state="expanded")

with st.sidebar:
    st.markdown("<img src={} width='150' style='display: block; margin: 0 auto;'>".format(img_url), unsafe_allow_html=True)
    st.header("Filters")
    with st.container():
        option = st.selectbox(label = "Filter 1",
                              options = ('Email', 'Home phone', 'Mobile phone'), 
                              index = None,
                              placeholder="Filter 1",
                              key="filter_1")
    with st.container():
        option = st.selectbox(label = "Filter 2",
                              options = ('Email', 'Home phone', 'Mobile phone'), 
                              index = None,
                              placeholder="Filter 2",
                              key="filter_2")
    with st.container():
        option = st.selectbox(label = "Filter 3",
                              options = ('Email', 'Home phone', 'Mobile phone'), 
                              index = None,
                              placeholder="Filter 3",
                              key="filter_3")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Site Selection Analysis</h1>", unsafe_allow_html=True)

st.divider()

with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        option = st.selectbox(label = "",
                              options = ('Email', 'Home phone', 'Mobile phone'), 
                              index = None,
                              placeholder="District 1",
                              key="district_1")
    with col2:
        option = st.selectbox(label = "",
                              options = ('Email', 'Home phone', 'Mobile phone'), 
                              index = None,
                              placeholder="District 2",
                              key="district_2")
    with col3:
        option = st.selectbox(label = "",
                              options = ('Email', 'Home phone', 'Mobile phone'), 
                              index = None,
                              placeholder="District 3",
                              key="district_3")
    with col4:
        st.text_input(label = "", 
                      placeholder = "Search...")
    
    with st.container():
        INITIAL_VIEW_STATE = pdk.ViewState(
          latitude=-33.891,
          longitude=151.198,
          zoom=15,
          #max_zoom=16,
          pitch=0,
          bearing=0
        )
        
        df_poi = pd.DataFrame(data = supabase.table("list_poi_sydney").select("*").execute().data)
        df_poi["weight"] = 1
        
        converter = geohashlite.GeoJsonHasher()
        df = pd.DataFrame(data = supabase.table("list_geohash_sydney").select("*").execute().data)
        converter.geohash_codes = df["geohash"].values.tolist()
        converter.decode_geohash(multipolygon=False)
        with open('data.json', 'w') as filepath:
            json.dump(converter.geojson, filepath)
        data = json.load(open('data.json'))
        
        COLOR_BREWER_BLUE_SCALE = [
            [240, 249, 232],
            [204, 235, 197],
            [168, 221, 181],
            [123, 204, 196],
            [67, 162, 202],
            [8, 104, 172],
        ]

        poi_layer = pdk.Layer(
            "HeatmapLayer",
            data=df_poi,
            opacity=0.5,
            get_position=["lon", "lat"],
            aggregation=pdk.types.String("SUM"),
            #color_range=COLOR_BREWER_BLUE_SCALE,
            threshold=0.1,
            get_weight="weight",
            pickable=True,
        )
        
        polygon_layer = pdk.Layer(
            'GeoJsonLayer',
            #polygon_geo,
            data,
            opacity=0.1,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            #get_elevation='properties.valuePerSqm / 20',
            get_elevation='0',
            get_fill_color='[255, 255, 255]',
            get_line_color=[255, 255, 255],
            pickable=True
        )
        
        tooltip = {"html": "<b>Weight:</b> {properties.geohash}"}
        
        r = pdk.Deck(
            layers=[poi_layer, polygon_layer],
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            initial_view_state=INITIAL_VIEW_STATE,
            tooltip=tooltip
        )
        
        path_to_html = "./map.html"
        r1 = pn.pane.DeckGL(r, sizing_mode='stretch_width', height=800)
        r1.save(path_to_html)
         

        with open(path_to_html,'r') as f: 
            html_data = f.read()
        
        components.html(html_data, scrolling=False, height=800)
        
with st.container():
    col1, _, col2 = st.columns([2, 1, 1])
    with col1:
        st.header("About")
        st.markdown("<p>Site Selection Analysis is revolutionizing location intelligence, business analytics, mapping, and geo-fencing markets in Sydney, Australia</p>", unsafe_allow_html=True)
        
    with col2:
        st.header("Contact Info")
        st.markdown("<p style='margin-top: 0px;'><strong>Syachrul Qolbi Nur Septi</strong></p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: -20px;'>Data Scientist</p>", unsafe_allow_html=True)
        st.markdown("""
        <div>
        <a href='https://mail.google.com/mail/u/0/?to=syachrulqolbinursepti@gmail.com&fs=1&tf=cm'>
        <img src='https://img.icons8.com/?size=100&id=OVhNF7HVOQGe&format=png&color=000000' width='40'>
        </a>
        <a href='https://www.linkedin.com/in/syachrulqolbi/'>
        <img src='https://img.icons8.com/?size=100&id=13930&format=png&color=000000' width='40'>
        </a>
        <a href='https://www.instagram.com/syahrulqolbi/'>
        <img src='https://img.icons8.com/?size=100&id=32323&format=png&color=000000' width='40'>
        </a>
        </div?""", unsafe_allow_html=True)
        