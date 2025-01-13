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
# import geemap.foliumap as geemap
from palette_biome import paleta_cores 
from palette_biome import paleta_nomes
from palette_biome import dicionario_classes
from palette_biome import dicionario_cores
import os 

##linha de código para autenticação
service_account = 'my-service-account@...gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'ee-scriptsremoteambgeo-040e397e0cc0.json')
ee.Initialize(credentials)

m=geemap.Map(height=800)
##Titulo da aplicação 
# Configuração da página
st.set_page_config(layout="wide")

st.title('Delimitação das Cheias - FLOOD POA')
st.divider()

st.sidebar.markdown("""Esta aplicação desenvolvida para visualização dos dados do Sentinel 2 utilizada na delimitação da cheia por meio de índices de água. 
                    Nesta mesma aplicação é possível analisar a sobreposição dos dados de uso e cobertura do solo de áreas agrículas oriundos do MapBiomas (coleção 8).""")



#load assets
df= pd.read_parquet('asset/lulc_water.parquet')

##merge database
df['cores'] = df['classe'].map(paleta_cores)
lista_nomes = sorted(list(df.NM_MUN.unique()))

# Adicionar um seletor de município
municipio_selecionado = st.selectbox("Selecione o município:", lista_nomes)

# Filtrar dados pelo município selecionado
dados_filtrados = df[df.NM_MUN == municipio_selecionado]
# Título da aplicação
st.title("Gráfico de Barras por Município")

# Criar o gráfico de barras
figura = px.bar(
    dados_filtrados,
    x='Nome_Class',
    y='area_ha_ov',
    color='Nome_Class',
    color_discrete_map=dicionario_cores,
    title=f'Área por Classe no Município de {municipio_selecionado}'
)

# Atualizar os títulos dos eixos
figura.update_layout(
    xaxis_title='Classes',
    yaxis_title='Área hectares'
)

# Criar duas colunas
col1, col2 = st.columns([0.6,0.4])

# Exibir o gráfico na primeira coluna
with col1:
    st.plotly_chart(figura)

# Exibir o dataframe na segunda coluna
with col2:
    st.dataframe(dados_filtrados)

##Login
Map = geemap.Map(height=800)

#define roi and collection
polygon = ee.Geometry.Polygon(
        [[[-54.64769751406591, -28.4028733286771],
          [-54.64769751406591, -30.66803438221671],
          [-50.41796118594091, -30.66803438221671],
          [-50.41796118594091, -28.4028733286771]]])


# define roi
roi = ee.FeatureCollection('users/scriptsremoteambgeo/Bacias_RS_SEMA').filter(ee.Filter.eq('reg_hid','Guaiba'))
Map.centerObject(roi,6)

# Define functions
def maskCloudAndShadowsSR(image):
  cloudProb = image.select('MSK_CLDPRB');
  snowProb = image.select('MSK_SNWPRB');
  cloud = cloudProb.lt(5)
  snow = snowProb.lt(5)
  scl = image.select('SCL')
  shadow = scl.eq(3) # 3 = cloud shadow
  cirrus = scl.eq(10) #10 = cirrus
  #Probabilidade de nuvem inferior a 5% ou classificação de sombra de nuvem
  mask = (cloud.And(snow)).And(cirrus.neq(1)).And(shadow.neq(1));
  return image.updateMask(mask).select('B.*').multiply(0.0001).set('data', image.date().format('YYYY-MM-dd')) \
        .copyProperties(image, image.propertyNames())


def index(image):
    mndwi = image.normalizedDifference(['B3', 'B11']).rename('mndwi')
    mask = mndwi.gt(0)
    water_mask = mndwi.updateMask(mask).rename('water')

    return image.addBands([water_mask]).clip(roi).copyProperties(image, image.propertyNames())



# Selection dataset mapbiomas 
mapbiomas = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1')
palettes = list(paleta_cores.values())

# Define palette visualition
vis = {
  'palette':palettes,
  'min':0,
  'max':62
}
# Selection year 2022
lucl_2022= mapbiomas.select('classification_2023').clip(roi)


# Select agriculture areas 
# https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Legenda-Colecao-8-LEGEND-CODE.pdf
values_farming = ee.List([14, 15, 18, 19, 39, 20, 40, 62, 41, 36, 46, 47, 35, 48,9,21])
# function to create mask to all value
def createMask(value):
    # Converter o valor para uma imagem constante
    value_image = ee.Image.constant(value)
    # Criar a máscara usando a operação eq()
    return lucl_2022.eq(value_image)

# Mapping a function in all values and combine with operation or 
mask = ee.ImageCollection(values_farming.map(createMask)).reduce(ee.Reducer.anyNonZero())
mask_farming = lucl_2022.updateMask(mask)


# ImagemCollection
collection = ee.ImageCollection("COPERNICUS/S2_SR")\
                .filterBounds(polygon)\
                .filterDate('2024-04-10', '2025-05-11')\
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',35))\
                .map(maskCloudAndShadowsSR)\
                .map(index)
                

# fill clean composite                
fill = collection.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',10)).median()
may = collection.filter(ee.Filter.eq('data','2024-05-06'))


##Convert to vector 
flood = may.median().select('water')

# reduce = flood.reduceRegion(
#                     reducer=ee.Reducer.mean(),
#                     geometry=roi.geometry(),
#                     scale=30,
#                     maxPixels=1e9
# )

flood_fill = flood.gt(0.15).selfMask().rename('water')


# # Convert the zones of the thresholded nightlights to vectors.
# vectors = flood_fill.eq(1).reduceToVectors(**{
#   'geometry':polygon,
#   'scale': 10,
#   'geometryType': 'polygon',
#   'eightConnected': False,
#   'labelProperty': 'zone',
#   'reducer': ee.Reducer.countEvery(),
#   'maxPixels':1e13,
#   'tileScale':4
# })


# mask_farming_clip =  mapbiomas.select('classification_2022').clip(vectors)

# Visualization 
# Map.addLayer(lucl_2022,vis,'Mapbiomas 2022',False)
# Map.addLayer(fill,{'bands':['B4','B3','B2'], 'min':0.10, 'max':0.23},'2023-2023 median')
Map.add_basemap('HYBRID')
# Map.addLayer(may,{'bands':['B4','B3','B2'], 'min':0.10, 'max':0.23},'Maio 06',False)
Map.addLayer(mask_farming,vis,'Farming')
# Map.addLayer(mask_farming_clip,vis,'Farming Clip')
Map.addLayer(flood_fill,{'palette':['blue'], 'min':0.10, 'max':0.54,'opacity':0.5},'Maio 06 2024')
# Map.addLayer(flood,{'palette':['blue'], 'min':0.10, 'max':0.54,'opacity':0.5},'Maio 06 2024_')


Map.to_streamlit()

st.sidebar.markdown('Desenvolvido por [AmbGEO]("https://ambgeo.com/")')
st.sidebar.image('asset/logo_ambgeo.png')


# ##Export
# task = ee.batch.Export.table.toDrive(
#     collection=vectors,
#     description='mask_water_fill',
#     folder='MBA_EX',
#     fileFormat='SHP',
# )

# # Inicie a tarefa de exportação
# task.start()
# task.status()

# ##Classe mapbiomas
# vectors_lulc = mask_farming_clip.reduceToVectors(**{
#   'geometry':polygon,
#   'scale': 250,
#   'geometryType': 'polygon',
#    'bestEffort':True,
#   'eightConnected': False,
#   'labelProperty': 'classe',
#   'reducer': ee.Reducer.countEvery(),
#   'maxPixels':1e13,
#   'tileScale':4
# })

# # geemap.ee_to_shp(vectors_lulc, filename='mapbiomas.shp')
# # geemap.ee_to_shp(vectors, filename='mask_water.shp')


# ##Export
# task_2 = ee.batch.Export.table.toDrive(
#     collection=vectors_lulc,
#     description='lucl_farm',
#     folder='MBA_EX',
#     fileFormat='SHP',
# )

# # Inicie a tarefa de exportação
# task_2.start()
# task_2.status()
