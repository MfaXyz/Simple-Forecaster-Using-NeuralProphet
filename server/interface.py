# Import Libraries
import streamlit as st
from PIL import Image
import main
from zipfile import ZipFile


# Set Basic Configs
st.set_page_config(page_title='PAFTA', page_icon=Image.open('favicon-32x32.png'), menu_items={
    'Get Help': 'http://mfaxyz.ir/',
    'Report a bug': 'http://mfaxyz.ir/',
    'About': "Pafta! Time Series Sales/Demand Forecasting For Businesses :)"
})
hide_img_fs = '''<style>
button[title="View fullscreen"]{ visibility: hidden;} 
footer{visibility: hidden;} 
div.stButton > button:first-child{background-color: #2c4a78 ;color:#EEEEEE;font-size:20px;height:3em;width:20em;border-radius:10px 10px 10px 
10px;left: 25%;position: relative;}
</style> '''
st.markdown(hide_img_fs, unsafe_allow_html=True)


# Change Visibility Of Button Function
def change_buttons(status):
    if status:
        hide_buttons = '''<style>
        div.stDownloadButton > button:first-child{display:none;background-color: #00ADB5 ;color:#EEEEEE;font-size:20px;height:3em;width:20em;border-radius:10px 10px 10px 
        10px;left: 25%;position: relative;} 
        </style> '''
        st.markdown(hide_buttons, unsafe_allow_html=True)
    else:
        hide_buttons = '''<style>
        div.stDownloadButton > button:first-child{display:block;background-color: #00ADB5 ;color:#EEEEEE;font-size:20px;height:3em;width:20em;border-radius:10px 10px 10px 
        10px;left: 25%;position: relative;} 
        </style> '''
        st.markdown(hide_buttons, unsafe_allow_html=True)


# Create Basic UI
image = Image.open('paftaLogo.png')
col1, col2, col3 = st.columns([2.5, 5, 2.5])
col2.image(image, caption='Time Series Sales/Demand Forecasting For Businesses', use_column_width=True)
uploaded_file = st.file_uploader("Choose CSV File:", type='csv')
option = st.selectbox(
    'Choose Frequency Type:',
    ('Daily', 'Monthly'))
st.write('Selected Frequency:', option)
freq = ''
if option == 'Daily':
    freq = 'D'
else:
    freq = 'M'
periods = st.number_input('Insert Your Length Of Predict Time:', min_value=1, step=1)
st.write('The Inserted Number:', periods)

# Start Forecasting Button
aContainer = st.empty()
done = False
button_A = aContainer.button('Start Forecasting', key='first')
if button_A:
    if hasattr(uploaded_file, 'name'):
        change_buttons(True)
        aContainer.empty()
        with st.spinner('Waiting...'):
            print(freq)
            main.make_future(filename=uploaded_file, freq=freq, periods=periods)
        st.success('Done!')
        done = True
        showResult = True
        change_buttons(False)
    else:
        st.warning('Please Choose CSV File!')

# After Forecasting, Show Results
if done:
    button_A = aContainer.button('Done!', key='second')
    zipObj = ZipFile("Results.zip", "w")
    zipObj.write('forecast.csv')
    zipObj.write("Output.html")
    zipObj.close()
    with open('Results.zip', 'rb') as f:
        st.download_button('Download Your Results As a Zip File', f, file_name='Results.zip')

