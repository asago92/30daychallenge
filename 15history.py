import streamlit as st
import altair as alt
import pandas as pd
import openpyxl
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import streamlit_highcharts as hg 

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
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/96c0bd/sunburst-coffee-flavors-complete.csv')

    fig = go.Figure(go.Treemap(
        ids = df.ids,
        labels = df.labels,
        parents = df.parents,
        pathbar_textfont_size=15,
        root_color="lightgrey"
    ))
    fig.update_layout(
        uniformtext=dict(minsize=10, mode='hide'),
        margin = dict(t=50, l=25, r=25, b=25)
    )
    st.plotly_chart(fig, theme="streamlit")

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
    st.write("The chart shows the average maximum temperature for each month on Mars in an attempt to identify the Martian solstice and equinox cycles.")
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
        alt.X('bin_min:Q', bin='binned', title='Maximum Daily Temperature (C)',
          scale=alt.Scale(domain=[-30, 0])),  
        alt.Y(
            'value:Q',
            scale=alt.Scale(range=[step, -step * overlap]),
            axis=None
        ),
        alt.Fill(
            'mean_temp:Q',
            legend=None,
            scale=alt.Scale(domain=[-15, 0], scheme='lighttealblue')
        )
    ).facet(
        row=alt.Row(
            'Month:T',
            title=None,
            header=alt.Header(labelAngle=0, labelAlign='right', format='%B')
        )
    ).properties(
        title='2012 - 2018',
        bounds='flush'
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    ).configure_title(
        anchor='end'
    )
   
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
    st.markdown("---")
    
    #day17:connections
    
    st.header("Day 17: Connections")
    st.subheader("Gross trade flows within BRICS countries")
    st.write("In the 2022 economic partnership between Brazil, Russia, India, China, and South Africa (BRICS), China took up the majority of overall trade.")

    chartDef={ 'accessibility': { 'point': { 'valueDescriptionFormat': '{index}. '
                                                              'From '
                                                              '{point.from} '
                                                              'to '
                                                              '{point.to}: '
                                                              '{point.weight}.'}},
      'series': [ { 'data': [ [ 'Brazil',
                                'Russia',
                                10.6],
                              [ 'Brazil',
                                'India',
                                15.9],
                              [ 'Brazil',
                                'China',
                                157.5],
                              [ 'Brazil',
                                'South Africa',
                                2.7],
                              [ 'Russia',
                                'Brazil',
                                10.6],
                              [ 'Russia',
                                'India',
                                43.6],
                              [ 'Russia',
                                'China',
                                190.3],
                              [ 'Russia',
                                'South Africa',
                                0.8],
                              [ 'India',
                                'Brazil',
                                15.9],
                              [ 'India',
                                'Russia',
                                43.6],
                              [ 'India',
                                'China',
                                117.43],
                              [ 'India',
                                'South Africa',
                                19.4],
                              [ 'China',
                                'Brazil',
                                157.5],
                              [ 'China',
                                'Russia',
                                190.3],
                              [ 'China',
                                'India',
                                117.3],
                              [ 'China',
                                'South Africa',
                                56.7],
                              [ 'South Africa',
                                'Brazil',
                                2.7],
                              [ 'South Africa',
                                'Russia',
                                0.8],
                              [ 'South Africa',
                                'India',
                                19.4],
                              [ 'South Africa',
                                'China',
                                56.7]],
                    'dataLabels': { 'color': '#333',
                                    'distance': 10,
                                    'style': { 'textOutline': 'none'},
                                    'textPath': { 'attributes': { 'dy': 5},
                                                  'enabled': True}},
                    'keys': [ 'from',
                              'to',
                              'weight'],
                    'name': 'Dependency '
                            'wheel series',
                    'size': '95%',
                    'type': 'dependencywheel'}],
      'title': { 'text': 'BRICS '
                         'Trade '
                         'Turnover 2022'}}
    
    
    hg.streamlit_highcharts(chartDef,640)
    
    st.markdown("---")
    
    #day18 Asian Development Bank
    st.header("Day 18: Asian Development Bank Data")
    st.subheader("ADB's commitment to financing Climate Change ")
    st.write("In 2023, ADB committed $10,747 million in climate finance. This chart shows how the commited funds have been distributed across Asian Sub Regions.")
           
    #bubblechart
    chartDef={ 'chart': { 'height': '50%',
                 'type': 'packedbubble'},
      'plotOptions': { 'packedbubble': { 'dataLabels': { 'enabled': True,
                                                         'filter': { 'operator': '>',
                                                                     'property': 'y',
                                                                     'value': 1000},
                                                         'format': '{point.name}',
                                                         'style': { 'color': 'black',
                                                                    'fontWeight': 'normal',
                                                                    'textOutline': 'none'}},
                                         'layoutAlgorithm': { 'dragBetweenSeries': True,
                                                              'gravitationalConstant': 0.05,
                                                              'parentNodeLimit': True,
                                                              'seriesInteraction': False,
                                                              'splitSeries': True},
                                         'maxSize': '100%',
                                         'minSize': '20%',
                                         'zMax': 1000,
                                         'zMin': 0}},
      'series': [ { 'data': [ { 'name': 'Afghanistan',
                                'value': 400},
                              { 'name': 'Armenia',
                                'value': 138.051},
                              { 'name': 'Georgia',
                                'value': 77.118},
                              { 'name': 'Kazakhstan',
                                'value': 219.933},
                              { 'name': 'Kyrgyz Republic',
                                'value': 80.3},
                              { 'name': 'Pakistan',
                                'value': 1618.674},
                              { 'name': 'Tajikistan',
                                'value': 41},
                              { 'name': 'Uzbekistan',
                                'value': 1252.971}],
                    'name': 'Central and West Asia'},
                  { 'data': [ { 'name': 'Mongolia',
                                'value': 292.887},
                              { 'name': 'China',
                                'value': 1472.433}],
                    'name': 'East Asia'},
                  { 'data': [ { 'name': 'Micronesia',
                                'value': 18},
                             { 'name': 'Fiji',
                                'value': 3},
                             { 'name': 'Kiribati',
                                'value': 40},
                             { 'name': 'Papua New Guinea',
                                'value': 63.6},
                             { 'name': 'Samoa',
                                'value': 10},
                             { 'name': 'Solomon Islands',
                                'value': 56.7},
                              { 'name': 'Tonga',
                                'value': 55.1},
                              { 'name': 'Tonga',
                                'value': 37.8}],
                    'name': 'Pacific'},
                  { 'data': [ { 'name': 'Bangladesh',
                                'value': 4226.90},
                              { 'name': 'Bhutan',
                                'value': 32},
                              { 'name': 'India',
                                'value': 3108.97},
                              { 'name': 'Maldives',
                                'value': 119.2},
                              { 'name': 'Nepal',
                                'value': 554.5},
                              { 'name': 'Sri Lanka',
                                'value': 616.58}],
                    'name': 'South '
                            'Asia'},
                  { 'data': [ { 'name': 'Cambodia',
                                'value': 215},
                              { 'name': 'Indonesia',
                                'value': 2970.356},
                              { 'name': 'Lao',
                                'value': 365.035},
                              { 'name': 'Malaysia',
                                'value': 0.75},
                              { 'name': 'Myanmar',
                                'value': 29.218},
                              { 'name': 'Philippines',
                                'value': 5729.77},
                              { 'name': 'Thailand',
                                'value': 36.986},
                              { 'name': 'Viet Nam',
                                'value': 34.25}],
                    'name': 'South '
                            'East Asia'}],
      'title': { 'text': 'ADB Climate Change Financing '
                         '(2023)'},
      'tooltip': { 'pointFormat': '<b>{point.name}:</b> '
                                  '{point.value}$ million ',
                   'useHTML': True}}
    
    
    hg.streamlit_highcharts(chartDef,1240)




    
