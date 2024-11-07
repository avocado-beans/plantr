from pages.modules import *
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="THE WEBFARM | USING AI TO SAVE THE 🌎, ONE 🌱 AT A TIME", page_icon="images/icon.png")

st.sidebar.page_link("main.py", label="HOME", icon="🏠")
st.sidebar.page_link("pages/scanPlant.py", label="SCAN A PLANT", icon="🌱")
st.sidebar.page_link("pages/follytest.py", label="PICK A LOCATION", icon="🗺️")
st.sidebar.page_link("pages/rippleEffects.py", label="PREDICT EFFECTS", icon="🌎")

st.image("images/logo.png")
st.header("", divider='green')
#Using AI to save the 🌎, one 🌱 at a time
st.header("**Drag in a picture of a plant and see how it could affect different ecosystems!**")
st.divider()
uploaded_file = st.file_uploader("Choose a file")

d = st.empty()
if uploaded_file is not None:
    image = uploaded_file.getvalue()
    st.image(image)
    
    d.success("**PROCESSING IMAGE...**")
    with open ('images/img.jpg','wb') as file:
        file.write(image)
    plantName = getPlant('images/img.jpg')
    st.header(f"{plantName[0]}: The {plantName[1]}", divider='green')
    d.success("**DONE!**")
    left, right = st.columns(2)
    with open ('plntNM.txt','w') as file:
        file.write(plantName[0])
    with open ('cmnNM.txt', 'w') as file:
        file.write("The ")
        file.write(plantName[1])
    response = gemini("Tell me about the plant species known as "+plantName[0]+".")
    with left:
        st.write(response)
        st.write("**(Hint: Go to the sidebar and hit PICK LOCATION to pick the area you wanna see this plant placed.)**")
    with right:
        st.image("images/img.jpg")
    st.divider()
    
    st.header(f"About {plantName[0]}:", divider='green')
    pre_apiKey = os.env['PREKEY']

    url = f"https://trefle.io/api/v1/plants/search?token={pre_apiKey}&q={plantName[0]}"

    response = requests.get(url)
    plantSpecies = json.loads(response.text)['data'][0]['slug']
    plantDataURL = f"https://trefle.io/api/v1/species/{plantSpecies}?token={pre_apiKey}"
    response = requests.get(plantDataURL)
    plantData = json.loads(response.text)

    df = pd.DataFrame({
        "Native Locations": plantData['data']['distribution']['native']
        })
    df1 = pd.DataFrame({"Introduced to Locations": plantData['data']['distribution']['introduced']    
        })
    
    question = f"Where does the plant species {plantName[0]} originate?"
    st.subheader("Q: Where does the plant originate?") 
    st.table(df)
    st.table(df1)
    
    question = f"What kind of climate does the plant species {plantName[0]} prefer?"
    st.subheader("Q: What kind of climate does the plant prefer?")
    
    answer = gemini(question)
    st.write(answer)
    
    question = f"What are the space and nutritional requirements of the plant species {plantName[0]}? (State quantitatively.)"
    st.subheader("Q: What are the nutritional requirements of the plant?")
    answer = gemini(question)
    st.write(answer)
    
    
    question = f"How can the plant species {plantName[0]} be used for human benefit?"
    st.subheader("Q: How can I use this plant?")
    
    answer = gemini(question)
    st.write(answer)
    
    
st.divider()
l, r = st.columns(2)
with r:
    st.caption("made with 💚 by Estifanos Tolemariam")
