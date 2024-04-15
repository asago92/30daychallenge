import streamlit as st
import altair as alt
import pandas as pd
import openpyxl
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="vizchallenge",
    page_icon="📊",
    layout="wide"
)
st.title("#30DayChartChallenge April 2024")
st.header("30 Days | 30 Charts | 5 Categories")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Comparisons", "Distributions", "Relationships", "Timeseries", "Uncertainties"])

with tab1:
    df = px.data.gapminder().query("year == 2007")
    fig = px.icicle(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                      color='lifeExp', hover_data=['iso_alpha'],
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, theme=None)
    st.header("Day 1: Part-to-Whole")
    st.subheader("Life Expectancy")
    st.write("Something about this chart")

with tab3:
    source = pd.read_excel('MusicData.xlsx')
    source['Year'] = pd.to_datetime(source['Year'], format='%Y')
    
    chart = alt.Chart(source).mark_area().encode(
        alt.X('Year:T',
            axis=alt.Axis(format='%Y', domain=False, tickSize=0)
        ),
        alt.Y('Value (Actual):Q', aggregate='sum', stack='center', axis=None),
        alt.Color('Format:N',
            scale=alt.Scale(scheme='tableau20')
        )
    ).interactive()
    
    st.header("Day 15: Historical")
    st.subheader("Visualizing 40 Years of Music Industry Sales")
    st.write("The data reflects the evolution in music consumption, shifting from physical media like CDs and cassettes to digital downloads and streaming services. This transition highlights the music industry's adaptation to technological advancements and changing consumer preferences.")
    
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
    st.markdown("---")
