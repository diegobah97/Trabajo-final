import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide"
)

@st.cache
def carga_data():
  return pd.read_excel("faenas_chile.xlsx", header=0)

# Se lee la información de forma óptima
faenas = carga_data()



st.write("# Mapa de ubicación faenas mineras en Chile")



# Obtener parte de la información
geo_puntos_comuna = faenas[ ["Este","Norte", "NOMBRE EM", "COMUNA F", "TIPO INST", "RECURSO P"]].rename(columns={
  "NOMBRE EM": "Nombre empresa", 
  "COMUNA F": "Comuna", 
  "TIPO INST": "Tipo institucion",
  "RECURSO P":"Recurso",
})
geo_puntos_comuna.dropna(subset=["Comuna"], inplace=True)

with st.sidebar:
  # Obtener los nombres unicos de comunas
  comunas = geo_puntos_comuna["Comuna"].sort_values().unique()

  comunas_seleccionadas = st.multiselect(
    label="Filtrar por Comuna", 
    options=comunas,
    help="Selecciona las comunas a mostrar",
    default=[] # También se puede indicar la variable "comunas", para llenar el listado
  )

with st.sidebar:
  # Obtener los nombres unicos de recurso
  recursos = geo_puntos_comuna["Recurso"].sort_values().unique()

  recursos_seleccionados = st.multiselect(
    label="Filtrar por Recurso", 
    options=recursos,
    help="Seleccionar recurso",
    default=[] # También se puede indicar la variable "comunas", para llenar el listado
  )

geo_data = geo_puntos_comuna


# Aplicar filtro de Comuna
if comunas_seleccionadas:
  geo_data = geo_puntos_comuna.query("Comuna == @comunas_seleccionadas")

if recursos_seleccionados:
  geo_data = geo_puntos_comuna.query("Recurso == @recursos_seleccionados")


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
              "<b>Recurso: </b> {Recurso} <br /> "
              "<b>Georeferencia (Lat, Lng): </b>[{Norte}, {Este}] <br /> "
    }
)

st.write(puntos_mapa)

