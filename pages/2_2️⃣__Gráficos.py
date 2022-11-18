import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt


st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide"
)

@st.cache
def carga_data():
  return pd.read_excel("faenas_chile.xlsx", header=0)

st.write("### Gráficos")
st.write("##### Información de Faenas mineras en Chile y el tipo de recurso explotado.")

# Se lee la información de forma óptima
data = carga_data()

data_puntos = data[ ["Este","Norte", "NOMBRE EM", "COMUNA F", "TIPO INST", "RECURSO P"]].rename(columns={
  "NOMBRE EM": "Nombre empresa", 
  "COMUNA F": "Comuna", 
  "TIPO INST": "Tipo institucion",
  "RECURSO P": "RECURSO"
})


# Generar listado de horarios ordenados
recu_puntos = data_puntos["RECURSO"].sort_values().unique()

# Generar listado de comunas ordenadas
comunas_puntos = data_puntos["Comuna"].sort_values().unique()

with st.sidebar:


  # Multiselector de comunas
  comuna_sel = st.multiselect(
    label="Comunas",
    options=comunas_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not comuna_sel:
    comuna_sel = comunas_puntos.tolist()

 # Multiselector de horarios
  hora_sel = st.multiselect(
    label="Tipo de recurso",
    options=recu_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not hora_sel:
    hora_sel = recu_puntos.tolist()

  # Se establece la lista completa en caso de no seleccionar ninguna
  if not hora_sel:
    hora_sel = recu_puntos.tolist()


col_bar, col_pie, col_line = st.columns(3, gap="small")

group_comuna = data_puntos.groupby(["RECURSO"]).size()
# Se ordenan de mayor a menor, gracias al uso del parámetros "ascending=False"
group_comuna.sort_values(axis="index", ascending=False, inplace=True)

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"


with col_bar:
  st.write("Gráfico de barra")
  bar = plt.figure()
  group_comuna.plot.bar(
    title="Cantidad de faenas por tipo de recurso",
    label="Total de faenas",
    xlabel="Tipo de recurso",
    ylabel="Faenas",
    color="maroon",
    grid=True,
  ).plot()
  st.pyplot(bar)
  

with col_pie:
  st.write("Gráfico de torta")
  pie = plt.figure()
  group_comuna.plot.pie(
    y="index",
    title="Cantidad de faenas por tipo de recurso",
    legend=None,
    autopct=formato_porciento
  ).plot()
  st.pyplot(pie)
  

with col_line:
  st.write("Gráfico de línea")
  line = plt.figure()
  group_comuna.plot.line(
    title="Cantidad de faenas por tipo de recurso",
    label="Faenas",
    xlabel="Tipo de recurso",
    ylabel="Faenas",
    color="blue",
    grid=True
  ).plot()
  st.pyplot(line)
  

geo_data = data_puntos.query(" RECURSO==@hora_sel and Comuna==@comuna_sel ")



st.write("###### Fuente:"" Ministerio de Minería")