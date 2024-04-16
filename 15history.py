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
    #treemaps plotly
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
    #update with interactive legend
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

    #day16:weather 
    #ridgelineplot
    st.header("Day 16: Weather")
    st.subheader("Observing Mars Weather")
    st.write("The data reflects the evolution in music consumption, shifting from physical media like CDs and cassettes to digital downloads and streaming services. This transition highlights the music industry's adaptation to technological advancements and changing consumer preferences.")
    df = pd.read_excel('mars-weather.xlsx')
    df['terrestrial_date'] = pd.to_datetime(df['terrestrial_date'])
    df_sorted = df.sort_values(by='terrestrial_date')

    step = 20
    overlap = 1

    chart = alt.Chart(df_sorted, height=step).transform_timeunit(
        Month='month(terrestrial_date)'
    ).transform_joinaggregate(
        mean_temp='mean(max_temp)', groupby=['Month']
    ).transform_bin(
        ['bin_max', 'bin_min'], 'max_temp'
    ).transform_aggregate(
        value='count()', groupby=['Month', 'mean_temp', 'bin_min', 'bin_max']
    ).transform_impute(
        impute='value', groupby=['Month', 'mean_temp'], key='bin_min', value=0
    ).mark_area(
        interpolate='monotone',
        fillOpacity=0.8,
        stroke='lightgray',
        strokeWidth=0.5
    ).encode(
        alt.X('bin_min:Q', bin='binned', title='Maximum Daily Temperature (C)'),
        alt.Y(
            'value:Q',
            scale=alt.Scale(range=[step, -step * overlap]),
            axis=None
        ),
        alt.Fill(
            'mean_temp:Q',
            legend=None,
            scale=alt.Scale(domain=[-30, 15], scheme='redyellowblue')
        )
    ).facet(
        row=alt.Row(
            'Month:T',
            title=None,
            header=alt.Header(labelAngle=0, labelAlign='right', format='%B')
        )
    ).properties(
        title='Mars Weather',
        bounds='flush'
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    ).configure_title(
        anchor='end'
    )
   
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
