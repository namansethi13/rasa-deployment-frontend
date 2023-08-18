
import streamlit as st

col1 , col2 , col3 , col4 = st.columns(4)

with col1:
    st.header("this is first")
    st.write("here is some text")
with col2:
    st.header("this is second")
    st.write("here is some text")
with col3:
    st.header("this is third")
    st.write("here is some text")
with col4:
    st.header("this is fourth")
    st.write("here is some text")
