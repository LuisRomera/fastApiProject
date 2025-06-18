import streamlit as st
import pandas as pd

st.header('Hello')
d = {'numeros': [0, 3, 3, 2, 9], 'frutas': ['platano', 'peras', 'manzanas', 'melocotones', 'banana']}
df = pd.DataFrame(data=d)

st.dataframe(df)