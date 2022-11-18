import streamlit as st
import streamlit.components.v1 as components

# Se configura la página
st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide",)


st.sidebar.write("## Curso visualización de datos en internet")

st.write("## Faena mineras en Chile")
st.write("La minería es una de las principales actividades de la economía chilena. Actualmente aporta el 11 % del PIB nacional, ​ y es el área con mayor inversión extranjera con un 33,3 % del total.​ El país es el principal productor a nivel mundial de cobre, renio, nitratos naturales, litio y yodo.")

components.html("""
  <iframe width="560" height="315" src="https://www.youtube.com/embed/r2u4Pc3qS2U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>""", height=520)


