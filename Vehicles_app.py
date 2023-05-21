import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('VEHICLES DATA FROM EXPAT-DAKAR SCRAPER')

st.markdown("""
This app performs simple webscraping of vehicles data from expat-dakar!
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Vehicles-expat-dakar.com](https://www.expat-dakar.com/voitures/dakar?condition=used-abroad).
""")

st.sidebar.header('User Input Features')
selected_page = st.sidebar.selectbox('Page', list(range(1,307)))

# Web scraping of Vehicles data on expat-dakar
@st.cache
def load_data(page):
    Url = "https://www.expat-dakar.com/voitures/dakar?condition=used-abroad&page="+str(page) 
    res = get(Url)
    soup = BeautifulSoup(res.text)
    conteneurs = soup.find_all('div', class_ ='listings-cards__list-item')
    data = []
    for conteneur in conteneurs : 
      try :
        Gen = conteneur.find('div', class_ ='listing-card__header__tags').find_all('span')
        Ven_Occ = Gen[0].text
        Marque= Gen[1].text 
        Année = Gen[2].text
        Aut_Man = Gen[3].text
        Adresse = conteneur.find('div', class_ = 'listing-card__header__location').text.replace('\n', '')
        Prix = conteneur.find('span', class_ = 'listing-card__price__value 1').text.replace('\n', '').replace('\u202f', '').replace(' F Cfa', '')
    
        obj = {
           'Ven_Occ': Ven_Occ,
           'Marque': Marque, 
           'Année': int(Année), # convertir en Integer
           'Aut_Man': Aut_Man, 
           'Adresse': Adresse,
           'Prix': int(Prix) # convertir en Integer
        }
        data.append(obj)
      except:
        pass
    df = pd.DataFrame(data)
    return df
Vehicles_data = load_data(selected_page)




st.header('Display Data dimension')
st.write('Data Dimension: ' + str(Vehicles_data.shape[0]) + ' rows and ' + str(Vehicles_data.shape[1]) + ' columns.')
st.dataframe(Vehicles_data)

# Download Vehicles data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(Vehicles_data), unsafe_allow_html=True)

