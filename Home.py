import streamlit as st 
import geemap


m=geemap.Map()

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