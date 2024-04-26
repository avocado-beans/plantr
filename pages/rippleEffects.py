import streamlit as st
import folium
from pages.modules import *
from streamlit_folium import st_folium
import reverse_geocode
import pandas as pd
from datetime import datetime
from meteostat import Point, Monthly
import numpy as np
import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="RIPPLE EFFECTS | THE WEBFARM", page_icon="images/icon.png")
st.sidebar.page_link("main.py", label="HOME", icon="🏠")
st.sidebar.page_link("pages/scanPlant.py", label="SCAN A PLANT", icon="🌱")
st.sidebar.page_link("pages/follytest.py", label="PICK A LOCATION", icon="🗺️")
st.sidebar.page_link("pages/rippleEffects.py", label="PREDICT EFFECTS", icon="🌎")

file = open("plntNM.txt", "r")
plantName = file.read()
file = open("cmnNM.txt", "r")
commonName = file.read()
response = "weed"
response = gemini("Tell me about the plant species known as "+plantName+".")

st.header(plantName.lower()+": "+commonName.lower(), divider='green')
st.subheader("_a little Introduction:_")
intro = "**"+response+"**"
st.write(intro)

st.divider()
st.image("images/img.jpg")
st.divider()

file = open("coordinates.txt", "r")
lines = file.read()
coordinates = (float(lines.split(" ")[0]), float(lines.split(" ")[1]))
coordinates = (coordinates, coordinates)
location = reverse_geocode.search(coordinates)

st.header(location[0]['city']+", "+location[0]['country'], divider='green')
st.write(coordinates[0])
left, right = st.columns(2)
with left:
    answer = "weed"
    question = "What is the ecosystem of "+location[0]['city']+", "+location[0]['country']+" like?"
    st.subheader(question)
    answer = gemini(question)
    st.write(str(answer))
    question = "Give a list of some of the species that live in "+location[0]['city']+", "+location[0]['country']+"."
    answer = gemini(question)
    st.write(str(answer))
    
with right:
    
    m = folium.Map(location=[coordinates[0][0], coordinates[0][1]], zoom_start=6)
    folium.Marker(
            [coordinates[0][0], coordinates[0][1]], popup=location[0]['city'], tooltip=location[0]['city']).add_to(m)
    st_data = st_folium(m, width=400)
st.divider()
pre_apiKey = "iZM0rbUN67u9PmtCMpaS0NyDY8gtXRNsKwK_-OIW-OE"

file = open("plntNM.txt", "r")
plantName = file.read()

url = f"https://trefle.io/api/v1/plants/search?token={pre_apiKey}&q={plantName}"

response = requests.get(url)
plantSpecies = json.loads(response.text)['data'][0]['slug']
plantDataURL = f"https://trefle.io/api/v1/species/{plantSpecies}?token={pre_apiKey}"
response = requests.get(plantDataURL)
plantData = json.loads(response.text)

question = "How would introducing the plant species "+plantName+" to "+location[0]['city']+", "+location[0]['country']+" affect the region's ecosystem?"
st.header(question)

question = "Does "+plantName+" have natural predators that live in "+location[0]['city']+", "+location[0]['country']+"?"
st.subheader("Does the plant have natural predators in the area?")
answer = gemini(question)
st.write(answer)

question = "Could a new population of "+plantName+" compete too much with the native flora of the region of "+location[0]['city']+", "+location[0]['country']+"?"
st.subheader("Will it compete too much with the region's native flora?")
answer = gemini(question)
st.write(answer)

question = "Will "+plantName+" get sufficient nutrition from the area if it were planted in "+location[0]['city']+", "+location[0]['country']+"?"
st.subheader("Will it get sufficient nutrition from the area?")
answer = gemini(question)
st.write(answer)

question = "Will "+plantName+" be comfortable with the climate of "+location[0]['city']+", "+location[0]['country']+"?"
st.subheader("Will it be comfortable with the region's climate")
answer = gemini(question)
st.write(answer)

st.divider()
l, r = st.columns(2)
with r:
    st.caption("made with 💚 by Estifanos Tolemariam")
