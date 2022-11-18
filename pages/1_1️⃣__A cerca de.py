import streamlit as st
import streamlit.components.v1 as components

st.write("## A cerca de:")
st.write("### Autor: Diego Bahamondes, Geógrafo.")
st.write("##### Email: dabm1603@gmail.com")


components.html("""
 <iframe width="560" height="315" src="https://www.youtube.com/embed/osdoLjUNFnA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
""", height=520)