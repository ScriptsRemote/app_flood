##App to visulize NOAA VIRS Night

##Import
import geemap
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
import geemap.foliumap as geemap
import os 

# Configuração da página
st.set_page_config(layout="wide")

##Titulo da aplicação 
st.title('VIIRS Daily Gridded Day Night - FLOOD POA')
st.divider()

st.sidebar.markdown("""Esta aplicação desenvolvida para visualização dos dados da coleção VNP46A1: VIIRS Daily Gridded Day Night Band 500m. A partir de um sensor Day-Night Band (DNB) que fornece medições diárias globais de luz noturna visível e infravermelha próxima (NIR) que são adequadas para o sistema terrestre ciência e aplicações. """)


##Login
m = geemap.Map(heigth=800)

dnbVis = {
  'min': 0,
  'max': 50,
  'palette': ['black', 'red', 'orange', 'white'],
}

roi = ee.Geometry.Point([-51.19636799894206, -29.92277214508047])

#before
noaa_before=  ee.ImageCollection('NOAA/VIIRS/001/VNP46A1')\
                .select('DNB_At_Sensor_Radiance_500m')\
                .filter(ee.Filter.date('2024-03-01', '2024-03-30')).median()
                
zones_before = noaa_before.gt(5).add(noaa_before.gt(10)).add(noaa_before.gt(15)).add(noaa_before.gt(20)).add(noaa_before.gt(30)).add(noaa_before.gt(40))
zones_before = zones_before.updateMask(zones_before.neq(0))

# m.addLayer(noaa_before, dnbVis, 'Before Flood')
##After
noaa_after = ee.ImageCollection('NOAA/VIIRS/001/VNP46A1')\
                .select('DNB_At_Sensor_Radiance_500m')\
                .filter(ee.Filter.date('2024-05-04', '2024-05-09')).median()
                
zones_after = noaa_after.gt(5).add(noaa_after.gt(10)).add(noaa_after.gt(15)).add(noaa_after.gt(20)).add(noaa_after.gt(30)).add(noaa_after.gt(40))
zones_after = zones_after.updateMask(zones_after.neq(0))



#define roi and collection
polygon = ee.Geometry.Polygon(
        [[[-57.37914878740735, -27.001757647128635],
          [-57.37914878740735, -32.21408265395696],
          [-48.77685386553235, -32.21408265395696],
          [-48.77685386553235, -27.001757647128635]]])



# m.addLayer(noaa_after, dnbVis, 'After Flood')
m.centerObject(roi,10)
m.add_basemap('HYBRID')
#join
left_layer = geemap.ee_tile_layer(
    zones_before, dnbVis, 'Before Flood',
)
right_layer = geemap.ee_tile_layer(
    zones_after, dnbVis, 'After Flood'
)

m.split_map(
    left_layer, right_layer, left_label='Before Flood', right_label='After Flood', left_position= "bottomleft",
    right_position = "bottomright"
)

m.to_streamlit()

##statistic
# Função para calcular a área de uma imagem mascarada
def calculate_area(image, region):
    pixel_area = image.multiply(ee.Image.pixelArea())
    area = pixel_area.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=500,
        maxPixels=1e9
    )
    return area.getInfo()['DNB_At_Sensor_Radiance_500m']

# Calcula a área antes e depois da cheia
area_before = calculate_area(zones_before, polygon)
area_after = calculate_area(zones_after, polygon)

# Arredonda os valores para duas casas decimais
area_before = round(area_before / 1e6, 2)  # Convertendo de metros quadrados para quilômetros quadrados
area_after = round(area_after / 1e6, 2)    # Convertendo de metros quadrados para quilômetros quadrados

# Cria um DataFrame com os resultados
data = {'Período': ['Pré', 'Pós'],
        'Área (km²)': [area_before, area_after]}
df = pd.DataFrame(data)

# Exibe os dados de área na barra lateral
st.sidebar.markdown(f'''Área luminosa antes da cheia (km²) era de {area_before}. Após a cheia, a área luminosa foi reduzida a {area_after} km².''')

# Cria um gráfico de barras com Plotly
fig = px.bar(df, x='Período', y='Área (km²)', color='Período',
             color_discrete_map={'Pré': 'gray', 'Pós': 'darkgray'},
             title='Comparação de Área Antes e Depois da Cheia',
             labels={'Área (km²)': 'Área (km²)', 'Período': 'Período'})

fig.update_layout(legend_title_text='Período')
st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown('Desenvolvido por [AmbGEO]("https://ambgeo.com/")')
st.sidebar.image('asset/logo_ambgeo.png')