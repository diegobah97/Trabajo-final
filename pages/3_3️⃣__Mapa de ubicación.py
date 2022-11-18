import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide"
)

@st.cache
def carga_data():
  return pd.read_excel("faenas_chile.xlsx", header=0)

# Se lee la información de forma óptima
data = carga_data()

st.write("# Mapa de ubicación faenas mineras en Chile")

data_puntos = data[ ["Este","Norte", "NOMBRE EM", "COMUNA F", "TIPO INST", "RECURSO P"]].rename(columns={
  "NOMBRE EM": "Nombre empresa", 
  "COMUNA F": "Comuna", 
  "TIPO INST": "Tipo institucion",
  "RECURSO P": "RECURSO"
})


# Generar listado  ordenado
recu_puntos = data_puntos["RECURSO"].sort_values().unique()

# Generar listado de comunas ordenadas
comunas_puntos = data_puntos["Comuna"].sort_values().unique()

with st.sidebar:
  st.write("##### Filtros de Información")
  st.write("---")

  # Multiselector de comunas
  comuna_sel = st.multiselect(
    label="Comunas",
    options=comunas_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not comuna_sel:
    comuna_sel = comunas_puntos.tolist()

 # Multiselector de recursos
  rec_sel = st.multiselect(
    label="Tipo de recurso",
    options=recu_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not rec_sel:
    rec_sel = recu_puntos.tolist()

  # Se establece la lista completa en caso de no seleccionar ninguna
  if not rec_sel:
    rec_sel = recu_puntos.tolist()

geo_datas = data_puntos

geo_data = data_puntos.query(" RECURSO==@rec_sel and Comuna==@comuna_sel ")

# Obtener el punto promedio entre todas las georeferencias
avg_lat = np.average(geo_data["Norte"])
avg_lng = np.average(geo_data["Este"])

puntos_mapa = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lng,
        zoom=3,
        pitch=20,
    ),
    layers=[
      pdk.Layer(
        "ScatterplotLayer",
        data = geo_data,
        pickable=True,
        get_position='[Este, Norte]',
        opacity=0.8,
        filled=True,
        radius_scale=2,
        radius_min_pixels=5,
        radius_max_pixels=50,
        line_width_min_pixels=0.01,
      )      
    ],
    tooltip={
      "html": "<b>Nombre empresa: </b> {Nombre empresa} <br /> "
              "<b>Tipo: </b> {Tipo institucion} <br /> "
              "<b>Comuna: </b> {Comuna} <br /> "
              "<b>Recurso: </b> {RECURSO} <br /> "
              "<b>Georeferencia (Lat, Lng): </b>[{Norte}, {Este}] <br /> ",
      "style": {
         "backgroundColor": "maroon",
         "color": "white"
        }
    }
)

st.write(puntos_mapa)