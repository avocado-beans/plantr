import streamlit as st
from pages.modules import *
from streamlit_back_camera_input import back_camera_input
import pandas as pd

st.set_page_config(page_title="SCAN A PLANT | THE WEBFARM", page_icon="images/icon.png")
st.sidebar.page_link("main.py", label="HOME", icon="🏠")
st.sidebar.page_link("pages/scanPlant.py", label="SCAN A PLANT", icon="🌱")
st.sidebar.page_link("pages/follytest.py", label="PICK A LOCATION", icon="🗺️")
st.sidebar.page_link("pages/rippleEffects.py", label="PREDICT EFFECTS", icon="🌎")

st.header("Scan That Plant: Tap the Camera!", divider='green')
image = back_camera_input()
d = st.empty()
c = st.empty()
c.subheader("**Snap a pic' of the 🪴 you want to analyze! Get to a decent distance from the plant (ideally 50 to 100cm ) and tap the window below to take the shot! (Try to make sure the plant is isolated from other plants and that you capture a unique part of it to ensure there is no confusion on the AI's end.)**")


if image:
    c.image(image)
    
    d.success("**PROCESSING IMAGE...**")
    with open ('images/img.jpg','wb') as file:
        file.write(image.getbuffer())
    plantName = getPlant('images/img.jpg')
    c.header(f"{plantName[0]}: The {plantName[1]}", divider='green')
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
    
    st.header(f"About {plantName[0]}:")
    pre_apiKey = "iZM0rbUN67u9PmtCMpaS0NyDY8gtXRNsKwK_-OIW-OE"

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

    

