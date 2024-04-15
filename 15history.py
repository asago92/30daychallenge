import streamlit as st
import altair as alt
import pandas as pd
import openpyxl

source = pd.read_excel('MusicData.xlsx')

chart = alt.Chart(source).mark_area().encode(
    alt.X('Year:T',
        axis=alt.Axis(format='%Y', domain=False, tickSize=0)
    ),
    alt.Y('Value (Actual):Q', aggregate='sum', stack='center', axis=None),
    alt.Color('Format:N',
        scale=alt.Scale(scheme='category20b')
    )
).interactive()

st.title("Visualizing 40 Years of Music Industry Sales")
st.altair_chart(chart, theme="None", use_container_width=True)
