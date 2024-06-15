import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import panel as pn

st.set_page_config(
    page_title="Retail Spatial Analysis",
    #page_icon="0xF0 0x9F 0x8F 0xAC",
    layout="wide",
    initial_sidebar_state="expanded")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Retail Spatial Analysis</h1>", unsafe_allow_html=True)

st.divider()

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
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
    with col5:
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

        r1 = pn.pane.DeckGL(r, sizing_mode='stretch_width', tooltips=tooltips, height=600)
        r1.save("map.html")
        path_to_html = "./map.html" 

        with open(path_to_html,'r') as f: 
            html_data = f.read()
        
        st.components.v1.html(html_data, scrolling=True, height=500)
        

with st.sidebar:
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
    
    