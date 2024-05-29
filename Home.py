import geemap
import geemap.foliumap as geemap
import ee
import streamlit as st
import streamlit_folium
from streamlit_folium import st_folium
import os
import json


@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

m=geemap.Map(height=800)
m

st.sidebar.markdown('Desenvolvido por [AmbGEO]("https://ambgeo.com/")')
st.sidebar.image('asset/logo_ambgeo.png')

##Introdução
st.image('asset/logo_ambgeo.png')
st.markdown('# Aplicações para análise e interpretação das Cheias ocorridas em maio de 2024 no Rio Grande do Sul')
st.divider()

##Contexto
st.markdown("""
    Este Dashboard tem como objetivo permitir que os usuário consigam visualizar, interpretar e analisar os impactos das cheias ocorridas em maio de 2024 no Rio Grande do Sul, Brasil, a partir imagens de diferentes sistemas sensores.
    O processamento das informações foi realizado via Google Earth Engine e a partir da integração com bibliotecas Python.
            """)