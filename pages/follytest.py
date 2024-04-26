import folium
import streamlit as st
import reverse_geocode
from streamlit_folium import st_folium

st.set_page_config(page_title="PLANT MAP | THE WEBFARM", page_icon="images/icon.png")
st.sidebar.page_link("main.py", label="HOME", icon="🏠")
st.sidebar.page_link("pages/scanPlant.py", label="SCAN A PLANT", icon="🌱")
st.sidebar.page_link("pages/follytest.py", label="PICK A LOCATION", icon="🗺️")
st.sidebar.page_link("pages/rippleEffects.py", label="PREDICT EFFECTS", icon="🌎")

file = open("plntNM.txt", "r")
plantName = file.read()
st.header("Predict the environmental effects of "+plantName+"!", divider='green')
st.write("Before introducing a plant to an area, it is important to consider the environmental effects it could have; especially if it a non-native species!")
st.write("Use the map below to see what effect the plant you've captured would have on the location you thought of planting it. **Tap on a location on the map and hit 'Locate!' to retrieve data about the place once you've found the perfect spot to place your plant!**")
st.divider()

left, right = st.columns([0.7, 0.3])

m = folium.Map(location=[9.492408153765544, 38.84765625000001], zoom_start=9)
folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
    ).add_to(m)

        # call to render Folium map in Streamlit
st_data = st_folium(m, width=725)
st.divider()
left, right = st.columns(2)

with left:
    st.subheader("The location selected is:")
    c = st.empty()
    if st.button("Locate!"):
        coordinates = (st_data['last_clicked']['lat'], st_data['last_clicked']['lng']), (st_data['last_clicked']['lat'], st_data['last_clicked']['lng'])
        with open ('coordinates.txt','w') as file:
            file.write(str(st_data['last_clicked']['lat']))
            file.write(" ")
            file.write(str(st_data['last_clicked']['lng']))
        
        location = reverse_geocode.search(coordinates)
    
        place = "**"+location[0]['city']+", "+location[0]['country']+"**"
        c.subheader("🌍 "+place)
    

    
    
with right:
    st_data['last_clicked']
    if st_data['last_clicked']:
        st.write(st_data['last_clicked']['lat'], st_data['last_clicked']['lng'])
    st.write("**(Hint: Go to the sidebar and tap PREDICT ENVIRONMENTAL EFFECTS after you select a location.)**")
    
st.divider()
l, r = st.columns(2)
with r:
    st.caption("made with 💚 by Estifanos Tolemariam")
