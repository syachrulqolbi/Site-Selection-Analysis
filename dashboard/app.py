import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import panel as pn
import streamlit.components.v1 as components

img_url = "https://img.icons8.com/?size=100&id=gD6jY1ZThEJD&format=png&color=000000"

st.set_page_config(
    page_title="Retail Spatial Analysis",
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
    st.markdown("<h1 style='text-align: center;'>Retail Spatial Analysis</h1>", unsafe_allow_html=True)

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
        DATA_URL = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/geojson/vancouver-blocks.json"

        #LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]]
        #LAND_COVER = [(np.random.randn(10, 2) / [50, 50] + [-33, 151]).tolist()]

        INITIAL_VIEW_STATE = pdk.ViewState(
          latitude=-33.891,
          longitude=151.198,
          zoom=15,
          #max_zoom=16,
          pitch=0,
          bearing=0
        )

        polygon = pdk.Layer(
            'PolygonLayer',
            #LAND_COVER,
            stroked=False,
            # processes the data as a flat longitude-latitude pair
            get_polygon='-',
            get_fill_color=[0, 0, 0, 20]
        )

        geojson = pdk.Layer(
            'GeoJsonLayer',
            DATA_URL,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation='properties.valuePerSqm / 20',
            get_fill_color='[255, 255, properties.growth * 255]',
            get_line_color=[255, 255, 255],
            pickable=True
        )

        r = pdk.Deck(
            layers=[polygon, geojson],
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            initial_view_state=INITIAL_VIEW_STATE
        )
        
        geojson_tooltip = {
            "html": """
              <b>Value per Square meter:</b> {properties.valuePerSqm}<br>
              <b>Growth:</b> {properties.growth}
            """,
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }

        tooltips = {geojson.id: geojson_tooltip}

        path_to_html = "./map.html"
        r1 = pn.pane.DeckGL(r, sizing_mode='stretch_width', tooltips=tooltips, height=800)
        r1.save(path_to_html)
         

        with open(path_to_html,'r') as f: 
            html_data = f.read()
        
        components.html(html_data, scrolling=False, height=800)
        
with st.container():
    col1, _, col2 = st.columns([2, 1, 1])
    with col1:
        st.header("About")
        st.markdown("<p>Retail Spatial Analysis is revolutionizing location intelligence, business analytics, mapping, and geo-fencing markets in Sydney, Australia</p>", unsafe_allow_html=True)
        
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
        