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

st.write("# Mapa de calor faenas mineras")

data_puntos = data[ ["Este","Norte", "NOMBRE EM", "COMUNA F", "TIPO INST", "RECURSO P"]].rename(columns={
  "NOMBRE EM": "Nombre empresa", 
  "COMUNA F": "Comuna", 
  "TIPO INST": "Tipo institucion",
  "RECURSO P": "RECURSO"
})


# Generar listado ordenados
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

 # Multiselector de recurso
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


geo_data = data_puntos.query(" RECURSO==@rec_sel and Comuna==@comuna_sel ")

if geo_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  avg_lat = np.median(geo_data["Norte"])
  avg_lng = np.median(geo_data["Este"])

  puntos_mapa = pdk.Deck(
      map_style=None,
      initial_view_state=pdk.ViewState(
          latitude=avg_lat,
          longitude=avg_lng,
          zoom=5,
          min_zoom=5,
          max_zoom=15,
          pitch=20,
      ),
      layers=[
        pdk.Layer(
          "HeatmapLayer",
          data=geo_data,
          pickable=True,
          auto_highlight=True,
          get_position='[Este, Norte]',
          opacity=0.6,
        
        )      
      ],

  )

  st.write(puntos_mapa)

st.write("#### Tabla de información")
st.write(geo_data)
