import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx
from streamlit_javascript import st_javascript
import time
import random
import requests
import threading
import uuid

Games = ['Riding Extreme 3D','My Clone Army','Chain Cube 2048','Train Miner','Merge Away','Twerk Race 3D','Polysphere','Mud Racing','Mow and Trim']
hide_streamlit_style = """<script src="https://telegram.org/js/telegram-web-app.js"></script><style>div[data-testid="stToolbar"] {visibility: hidden;height: 0%;position: fixed;}div[data-testid="stDecoration"] {visibility: hidden;height: 0%;position: fixed;}div[data-testid="stStatusWidget"] {visibility: hidden;height: 0%;position: fixed;}#MainMenu {visibility: hidden;height: 0%;}header {visibility: hidden;height: 0%;}footer {visibility: hidden;height: 0%;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def generate_code():
    client_id = str(uuid.uuid4())

    return_value = st_javascript("""await fetch('https://fullstackpython.com').then(function() {
      return 'Wyoming';
    });""")

    time.sleep(2)
    st.markdown(f"Return value was: {return_value}")
    #return return_value

generate_code()
c = st.container(border=True)
game_ids = {'Riding Extreme 3D': 1,'My Clone Army': 2,'Chain Cube 2048': 3,'Train Miner': 4,'Merge Away': 5,'Twerk Race 3D': 6,'Polysphere': 7,'Mud Racing': 8,'Mow and Trim': 9}
option = c.selectbox('label',Games, label_visibility='hidden')

key_code = c.empty()
key_code.info("Click [GENERATE] to generate a new code.")

progress_text = "Operation in progress. Please wait."
progress_bar = c.empty()
button = c.empty()
time_to_code = 10
codes = []

def parse_keys(game_id, number):
    time.sleep(time_to_code)
    codes.append('SUCK-MY-MIDDLEFINGER')

def generate_keys():
    button.button('GENERATE ANOTHER ONE', key=random.getrandbits(128), disabled=True)
    progress_bar.progress(0, text='')
    response = requests.get('https://api.gamepromo.io')
    parsekeys = threading.Thread(target=parse_keys,args=(game_ids[option],1))
    add_script_run_ctx(parsekeys)
    parsekeys.start()
    for percent_complete in range(100):
        time.sleep(time_to_code/100)
        progress_bar.progress(percent_complete + 1, text=f'{percent_complete + 1}%')
        key_code.warning(f"Generating codes {'.'*((percent_complete+1)%4)}")
    key_code.success(f"Finished generating codes!")
    for code in codes:
        progress_bar.code(code, language="python")
    regenerate = button.button('GENERATE ANOTHER ONE', key=random.getrandbits(128), disabled=False, on_click=generate_keys)
    time.sleep(60)

button.button(f'GENERATE', key=random.getrandbits(128), on_click=generate_keys)
