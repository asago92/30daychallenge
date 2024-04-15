import streamlit as st
import altair as alt
import pandas as pd

source = pd.read_excel('https://query.data.world/s/tjec4jpzz3kkdw46rdqjggump76iog?dws=00000')

chart = alt.Chart(source).mark_area().encode(
    alt.X('Year',
        axis=alt.Axis(format='%Y', domain=False, tickSize=0)
    ),
    alt.Y('sum(Value (Actual))', stack='center', axis=None),
    alt.Color('Format',
        scale=alt.Scale(scheme='category20b')
    )
).interactive()

st.altair_chart(chart, theme="streamlit", use_container_width=True)
