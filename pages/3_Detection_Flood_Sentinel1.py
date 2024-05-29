##App Delimitação de manchas de inundação 

import geemap
import geemap.foliumap as geemap
import ee
import streamlit as st 
import folium
import streamlit_folium
from streamlit_folium import folium_static
import plotly.express as px
import geopandas as gpd
import pandas as pd
# import mapclassify
import json 
import matplotlib.pyplot as plt 

# from palette_biome import paleta_cores
# from palette_biome import paleta_nomes
# from palette_biome import dicionario_classes
# from palette_biome import dicionario_cores
import os 

##Titulo da aplicação 
# Configuração da página
st.set_page_config(layout="wide")

st.title('Detecção de Cheias - FLOOD SELECT')
st.divider()

st.sidebar.markdown("""Esta aplicação desenvolvida para visualização dos dados do Sentinel 1 utilizada na delimitação da cheia por meio de limiar e segmentação.""")


@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

# Função para converter em valores naturais
def toNatural(image):
    return ee.Image(10.0).pow(image.divide(10.0)).copyProperties(image, image.propertyNames()).set('date', image.date().format('YYYY-MM-dd'))

def process_flood_detection(point, start_date, end_date):
    # Cria o mapa
    Map = geemap.Map()
    Map.add_basemap('HYBRID')

    # Filtra as imagens do Sentinel-1
    s1Collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
        .filterBounds(point) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        .map(toNatural)

    # Pega a primeira imagem da coleção
    s1Image = s1Collection.first()
    date_img = s1Image.get('date').getInfo()
    id_img = s1Image.get('system:id').getInfo()
    st.sidebar.markdown(f'A data da imagem é {date_img} e o id é {id_img}')

    # Cria a máscara de inundação
    flood_mask = s1Image.select('VH').lte(0.06).And(s1Image.select('VV').lte(0.06)).selfMask().rename('water')
    Map.addLayer(s1Image, {'min': 0, 'max': 0.2, 'bands': 'VV'}, 'Sentinel-1 VV', False)
    Map.addLayer(s1Image, {'min': 0, 'max': 0.2, 'bands': 'VH'}, 'Sentinel-1 VH', False)
    Map.addLayer(flood_mask, {'palette': ['blue'], 'opacity': 0.5}, 'flood', False)

    # Unindo pixels isolados usando morfologia matemática
    dilated = flood_mask.focal_max(1.25, 'square', 'pixels')
    flood_fill = dilated.focal_min(1.25, 'square', 'pixels')
    Map.addLayer(flood_fill, {'palette': ['cyan'], 'opacity': 0.5}, 'flood fill', False)

    # Obtém o conjunto de dados anual histórico do JRC
    jrc = ee.ImageCollection('JRC/GSW1_3/YearlyHistory') \
        .filterDate('1985-01-01', '2024-01-01') \
        .limit(5, 'system:time_start', False)

    permanentWater = jrc.map(lambda image: image.select('waterClass').eq(3)) \
        .sum() \
        .unmask(0) \
        .gt(0) \
        .updateMask(flood_mask.mask())

    Map.addLayer(permanentWater.selfMask(), {'palette': 'royalblue'}, 'JRC permanent water')

    # Encontre áreas onde não há água permanente, mas a água é observada
    floodImage = permanentWater.Not().And(flood_fill)
    Map.addLayer(floodImage.selfMask(), {'palette': 'firebrick'}, 'Flood areas')

    # Centraliza o mapa no ponto
    Map.centerObject(point, 10)

    # Exibe o mapa
    Map.to_streamlit()

    # # Visualizar as propriedades da imagem
    # st.write(floodImage.getInfo())
    # Calcula a área de floodImage e permanentWater
    # Calcula a área de floodImage e permanentWater

    area_floodImage = ee.Number(flood_mask.multiply(ee.Image.pixelArea()).reduceRegion(reducer=ee.Reducer.sum(), geometry=st.session_state.point.buffer(100000), maxPixels=1e13,scale=100).get("water")).getInfo()
    area_permanentWater = ee.Number(permanentWater.multiply(ee.Image.pixelArea()).reduceRegion(reducer=ee.Reducer.sum(), geometry=st.session_state.point.buffer(100000),maxPixels=1e13, scale=100).get("waterClass")).getInfo()

    # Arredonda os valores para duas casas decimais
    area_floodImage = round(area_floodImage / 1e6, 2)  # Convertendo de metros quadrados para quilômetros quadrados
    area_permanentWater = round(area_permanentWater / 1e6, 2)    # Convertendo de metros quadrados para quilômetros quadrados
   # Divide a tela em duas colunas
    col1, col2 = st.columns([0.6,0.4])

    # Gráfico de barras
    with col1:
        st.subheader('Área das Inundações')
        df = pd.DataFrame({
            'Categoria': ['Flood Image', 'Permanent Water'],
            'Área (km²)': [area_floodImage, area_permanentWater]
        })
        fig = px.bar(df, x='Categoria', y='Área (km²)', color='Categoria', title='Área das Inundações')
        st.plotly_chart(fig, use_container_width=True)

    # DataFrame
    with col2:
        st.subheader('Dados da Área')
        st.dataframe(df)

    return floodImage, flood_fill


# Primeira execução para desenhar o ponto
if 'point' not in st.session_state:
    st.session_state.point = None
if 'start_date' not in st.session_state:
    st.session_state.start_date = '2024-05-11'
if 'end_date' not in st.session_state:
    st.session_state.end_date = '2024-05-15'

# Inputs de latitude e longitude como texto
lat = st.sidebar.text_input('Latitude', value='-30.040714573694625')
lon = st.sidebar.text_input('Longitude', value='-51.21888918281439')

# Inputs para as datas
start_date = st.sidebar.text_input('Data de Início (YYYY-MM-DD)', value=st.session_state.start_date)
end_date = st.sidebar.text_input('Data de Fim (YYYY-MM-DD)', value=st.session_state.end_date)

if st.sidebar.button('Atualizar Localização e Datas'):
    try:
        lat = float(lat)
        lon = float(lon)
        st.session_state.point = ee.Geometry.Point([lon, lat])
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
    except ValueError:
        st.sidebar.error("Por favor, insira valores válidos para latitude e longitude.")

if st.session_state.point:
    floodImage, flood_mask = process_flood_detection(st.session_state.point, st.session_state.start_date, st.session_state.end_date)

    # Adicionar botão de download
    if st.sidebar.button("Download das Imagens"):
        out_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        # Exportar imagens
        download_path_floodImage = os.path.join(out_dir, 'floodImage.tif')
        download_path_flood_fill = os.path.join(out_dir, 'flood_fill.tif')
        
        geemap.ee_export_image(floodImage, filename=download_path_floodImage, scale=10, region=st.session_state.point.buffer(10000).bounds()) 
        geemap.ee_export_image(flood_mask, filename=download_path_flood_fill, scale=10, region=st.session_state.point.buffer(10000).bounds())

        # Verificar se os arquivos existem antes de adicionar os links de download
        if os.path.exists(download_path_floodImage) and os.path.exists(download_path_flood_fill):
            st.sidebar.success("Download realizado com sucesso.")
        else:
            st.sidebar.error("Erro durante a exportação. Os arquivos não foram criados.")
else:
    st.write("Insira a latitude, a longitude e as datas, depois clique em 'Atualizar Localização e Datas'.")


st.sidebar.markdown('Desenvolvido por [AmbGEO](https://ambgeo.com/)')
st.sidebar.image('asset/logo_ambgeo.png')