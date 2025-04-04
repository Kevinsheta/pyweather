import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

def convert_to_fahrenheit(celsius):
    return round((celsius * 9/5) + 32, 2)

# Function to display weather card
def weather_card(weather_data):
    # Create individual cards
    cards_html = "".join([
        f"""
        <div class="weather-card1">
            <div class="weather-card-content">
                <p class="weather-time">{hour['time']}</p>
                <img src="data:image/png;base64,{hour['icon_path']}" class="weather-icon2" alt="weather icon">
                <p class="weather-temp">{hour['temperature']}°</p>
            </div>
        </div>
        """ for hour in weather_data
    ])
    
    # Style and display the entire container
    st.markdown(
        f"""
        <style>
            .weather-container2 {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: black;
                padding: 20px;
                border-radius: 10px;
                max-width: 900px;
                margin: 0px auto;
                overflow-x: auto;
            }}
            .weather-card1 {{
                display: inline-block;
                width: 100px;
                padding: 10px 0px;
                border-radius: 10px;
                text-align: center;
                vertical-align: top;
            }}
            .weather-card-content {{
                width:100px;
                text-align: center;
            }}
            .weather-time {{
                margin: 5px;
                font-size: 20px !important;
                font-weight: bold;
                color: #ffffff;
            }}
            .weather-icon2 {{
                width: 40px;
                height: 40px;
            }}
            .weather-temp {{
                margin: 5px;
                font-size: 20px !important;
                font-weight: bold;
                color: #ffffff;
            }}
        </style>
        <div class="weather-container2">
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def plot_graph(data, city, temp_unit, start_date, end_date, primary_columns, selected_columns, data_type):
    # Convert start_date and end_date to datetime if they are strings
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    # Check if only one column is selected
    if len(selected_columns) == 1:
        column = selected_columns[0]
        plot_type = st.selectbox("Select Plot Type", ["line", "scatter"], key= f'plot_type_select_{primary_columns}_{data_type}')

        data[column] = data[column].interpolate()

        if plot_type == "line":
            fig = px.line(
                data_frame=data,
                x="datetime",
                y=column,
                title=f"{column} in {city}: {start_date.date()} to {end_date.date()}",
                labels={"value": "Weather", "variable": "Category"},
            )
            fig.update_traces(mode= 'markers+lines')

        elif plot_type == "scatter":
            fig = px.scatter(
                data_frame=data,
                x="datetime",
                y=column,
                title=f"{column} in {city}: {start_date.date()} to {end_date.date()}",
                labels={"value": "Weather", "variable": "Category"}
            )
            fig.update_traces(mode= 'markers')
        fig.update_layout(
            template= 'plotly_dark',
            hovermode= 'x unified'
        )
        st.plotly_chart(fig)

    # Multi-column visualization logic
    if len(selected_columns) > 1:
        st.write("Visualizing multiple columns...")
        
        if primary_columns == f"Average Temperature {temp_unit}":
            with st.spinner("Just Wait!!"):
                time.sleep(3)
            st.write('### Graph 1: Temperature Overview')
            plot_type= st.selectbox("Select plot type:", ['line', 'scatter'], key=f'avg_temp_plot1_{primary_columns}_{data_type}')

            data[[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}']] = data[[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}']].interpolate()
            
            if plot_type == 'line':
                fig1= px.line(
                    data_frame=data,
                    x='datetime',
                    y= [f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}'],
                    title= f"Temperature in {city}: {start_date.date()} to {end_date.date()}",
                    labels={'value': f'Temperature {temp_unit}', 'variable': 'Category'},
                    color_discrete_sequence= ['red', 'green', 'blue']
                )
                fig1.update_traces(mode= 'markers+lines')
            
            elif plot_type == 'scatter':
                fig1= px.scatter(
                    data_frame=data,
                    x= 'datetime',
                    y= [f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}'],
                    title= f"Temperature in {city}: {start_date.date()} to {end_date.date()}",
                    labels= {'value': f'Temerature {temp_unit}', 'variable': 'Category'},
                    color_discrete_sequence= ['red', 'green', 'blue']
                )
                fig1.update_traces(mode= 'markers')

            fig1.update_layout(
                template= 'plotly_dark',
                showlegend= True,
                xaxis_type= 'date',
                legend_title= "Temperature Type",
                hovermode= 'x unified',
                xaxis= dict(
                    showgrid= True,
                    gridcolor= "gray",
                    gridwidth= 0.5
                ),
                yaxis= dict(
                    showgrid= True,
                    gridcolor= 'gray',
                    gridwidth= 0.5
                )
            )
            st.plotly_chart(fig1)

            st.write('### Graph 2: Average Temperature and Precipitation')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key=f'avgpre_{primary_columns}_{data_type}')
                
            data[[f'Average Temperature {temp_unit}', "Precipitation (mm)"]] = data[[f'Average Temperature {temp_unit}', 'Precipitation (mm)']].interpolate()

            if plot_type == 'line':
                fig2= px.line(
                    data_frame= data,
                    x= 'datetime',
                    y= [f'Average Temperature {temp_unit}', 'Precipitation (mm)'],
                    title= f'Average Temerature and Precipitation in {city}: {start_date.date()} to {end_date.date()}',
                    labels= {'value': 'Weather', 'variable': 'Category'}
                )
                fig2.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig2= px.scatter (
                    data_frame= data,
                    x= 'datetime',
                    y= [f'Average Temperature {temp_unit}', 'Precipitation (mm)'],
                    title= f'Average Temerature and Precipitation in {city}: {start_date.date()} to {end_date.date()}',
                    labels= {'value': 'Weather', 'variable': 'Category'}
                )
                fig2.update_traces(mode= 'markers')

            fig2.update_layout(
                template= 'plotly_dark',
                showlegend= True,
                xaxis_type= 'date',
                legend_title= "Weather Type",
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)
        
        elif primary_columns == f"Minimum Temperature {temp_unit}":
            # Graph 1: Combination of three temperature columns and precipitation
            with st.spinner("Just Wait!!"):
                time.sleep(3)
            st.write("### Graph 1: Temperature Overview")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f'min_temp_plot1_{primary_columns}_{data_type}')
            data[[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}']] = data[[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}']].interpolate()

            if plot_type == "line":
                fig1 = px.line(
                    data_frame=data,
                    x='datetime',
                    y=[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}'],
                    title=f"Temperature in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"value": "Temperature (°C)", "variable": "Category"},
                    color_discrete_sequence=['red','green','blue'])
                fig1.update_traces(mode= 'markers+lines')
            elif plot_type == "scatter":
                fig1 = px.scatter(
                    data_frame=data,
                    x='datetime',
                    y=[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}'],
                    title=f"Temperature in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"x": "Date/Time", "value": "Metric", "variable": "Category"},
                    color_discrete_sequence=['red','green','blue'])
                fig1.update_traces(mode= 'markers')

            fig1.update_layout(
                template= 'plotly_dark',
                showlegend=True,
                xaxis_type='date',
                hovermode= 'x unified',
                xaxis= dict(
                    showgrid= True,
                    gridcolor= "gray",
                    gridwidth= 0.5
                ),
                yaxis= dict(
                    showgrid= True,
                    gridcolor= 'gray',
                    gridwidth= 0.5
                )
                )
            st.plotly_chart(fig1)

            # Graph 2: Minimum Temperature and Precipitation
            st.write("### Graph 2: Minimum Temperature and Precipitation")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f"min_temp_precip_{primary_columns}_{data_type}")
            data[[f"Minimum Temperature {temp_unit}", "Precipitation (mm)"]] = data[[f"Minimum Temperature {temp_unit}", "Precipitation (mm)"]].interpolate()

            if plot_type == "line":
                fig2 = px.line(
                    data_frame=data,
                    x="datetime",
                    y=[f"Minimum Temperature {temp_unit}", "Precipitation (mm)"],
                    title=f"Minimum Temperature and Precipitation in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"value": "Weather", "variable": "Category"}
                )
                fig2.update_traces(mode= 'markers+lines')

            elif plot_type == "scatter":
                fig2 = px.scatter(
                    data_frame=data,
                    x="datetime",
                    y=[f"Minimum Temperature {temp_unit}", "Precipitation (mm)"],
                    title=f"Minimum Temperature and Precipitation in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"value": "Weather", "variable": "Category"}
                )
                fig2.update_traces(mode= 'markers')
            fig2.update_layout(
                template= 'plotly_dark',
                showlegend= True,
                xaxis_type= 'date',
                legend_title= "Weather Type",
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)

        elif primary_columns == f"Maximum Temperature {temp_unit}":
            # Graph 1: Combination of three temperature columns and precipitation
            with st.spinner("Just Wait!!"):
                time.sleep(3)
            st.write("### Graph 1: Temperature Overview")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f'max_temp_plot1_{primary_columns}_{data_type}')
            data[[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}']] = data[[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}']].interpolate()

            if plot_type == "line":
                fig1 = px.line(
                    data_frame=data,
                    x='datetime',
                    y=[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}'],
                    title=f"Temperature in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"value": "Temperature (°C)", "variable": "Category"},
                    color_discrete_sequence=['red','green','blue'])
                fig1.update_traces(mode= 'markers+lines')
            
            elif plot_type == "scatter":
                fig1 = px.scatter(
                    data_frame=data,
                    x='datetime',
                    y=[f'Maximum Temperature {temp_unit}', f'Average Temperature {temp_unit}',  f'Minimum Temperature {temp_unit}'],
                    title=f"Temperature in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"x": "Date/Time", "value": "Metric", "variable": "Category"},
                    color_discrete_sequence=['red','green','blue'])
                fig1.update_traces(mode= 'markers')

            fig1.update_layout(
                template= 'plotly_dark',
                showlegend=True,
                xaxis_type='date',
                hovermode= 'x unified',
                xaxis= dict(
                    showgrid= True,
                    gridcolor= "gray",
                    gridwidth= 0.5
                ),
                yaxis= dict(
                    showgrid= True,
                    gridcolor= 'gray',
                    gridwidth= 0.5
                )
                )
            st.plotly_chart(fig1)

            # Graph 2: Maximum Temperature and Precipitation
            st.write("### Graph 2: Maximum Temperature and Precipitation")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f"max_temp_precip_{primary_columns}_{data_type}")
            data[[f"Maximum Temperature {temp_unit}", "Precipitation (mm)"]] = data[[f"Maximum Temperature {temp_unit}", "Precipitation (mm)"]].interpolate()

            if plot_type == "line":
                fig2 = px.line(
                    data_frame=data,
                    x="datetime",
                    y=[f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                    title=f"Maximum Temperature and Precipitation in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"value": "Weather", "variable": "Category"}
                )
                fig2.update_traces(mode= 'markers+lines')
            elif plot_type == "scatter":
                fig2 = px.scatter(
                    data_frame=data,
                    x="datetime",
                    y=[f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                    title=f"Maximum Temperature and Precipitation in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"value": "Weather", "variable": "Category"}
                )
                fig2.update_traces(mode= 'markers')
            fig2.update_layout(
                template= 'plotly_dark',
                showlegend= True,
                xaxis_type= 'date',
                legend_title= "Weather Type",
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)

        elif primary_columns == "Precipitation (mm)":
            # Graph 1: Precipitation and Snowfall
            st.write("### Graph 1: Precipitation and Snowfall")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f"precip_snowfall_{primary_columns}_{data_type}")
            data[['Precipitation (mm)', 'Snowfall (mm)']] = data[['Precipitation (mm)', 'Snowfall (mm)']].interpolate()

            if plot_type == 'line':
                fig1 = px.line(
                    data_frame=data,
                    x='datetime',
                    y=['Precipitation (mm)', 'Snowfall (mm)'],
                    title=f"Precipitation and Snowfall in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"x": "Date/Time", "value": "Weather", "variable": "Category"}
                )
                fig1.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig1 = px.scatter(
                    data_frame=data,
                    x='datetime',
                    y=['Precipitation (mm)', 'Snowfall (mm)'],
                    title=f"Precipitation and Snowfall in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"x": "Date/Time", "value": "Weather", "variable": "Category"}
                )
                fig1.update_traces(mode= 'markers')
            fig1.update_layout(
                template= 'plotly_dark',
                showlegend=True,
                xaxis_type='date',
                hovermode= 'x unified',
                xaxis= dict(
                    showgrid= True,
                    gridcolor= "gray",
                    gridwidth= 0.5
                ),
                yaxis= dict(
                    showgrid= True,
                    gridcolor= 'gray',
                    gridwidth= 0.5
                )
                )
            st.plotly_chart(fig1)

            # Graph 2: Precipitation and Average Temperature
            st.write("### Graph 2: Precipitation and Average Temperature")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f"precip_temp_{primary_columns}_{data_type}")
            data[[f"Average Temperature {temp_unit}", "Precipitation (mm)"]] = data[[f"Average Temperature {temp_unit}", "Precipitation (mm)"]].interpolate()

            if plot_type == "line":
                fig2 = go.Figure()
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data["Precipitation (mm)"],
                    name= "Precipitation (mm)",
                    mode= "lines",
                    line= dict(color= 'blue', width= 2)))
                
                fig2.add_trace(go.Line(
                    x=data.index,
                    y= data[f"Average Temperature {temp_unit}"],
                    name= f"Average Temperature {temp_unit}",
                    mode= "lines",
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'))
                fig2.update_traces(mode= 'markers+lines')

            elif plot_type == "scatter":
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data["Precipitation (mm)"],
                    name= "Precipitation (mm)",
                    mode= "markers",
                    marker= dict(color= 'blue', size= 8)))
                
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data[f"Average Temperature {temp_unit}"],
                    name= f"Average Temperature {temp_unit}",
                    mode= "markers",
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'))
                fig2.update_traces(mode= 'markers')

            # Add layout for secondary y-axis
            fig2.update_layout(
                template= 'plotly_dark',
                title=f"Precipitation and Average Temperature in {city}: {start_date.date()} to {end_date.date()}",
                xaxis=dict(title="Date"),
                yaxis=dict(title="Precipitation (mm)"),
                yaxis2=dict(
                    title=f"Average Temperature {temp_unit}",
                    overlaying='y',
                    side='right'),
                legend=dict(
                    x=1.0,
                    xanchor='left',
                    y=1.1),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)

        elif primary_columns == "Snowfall (mm)":
            # Graph 1: Snowfall and Precipitation
            st.write("### Graph 1: Snowfall and Precipitation")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f"snowfall_precip_{primary_columns}_{data_type}")
            data[['Precipitation (mm)', 'Snowfall (mm)']] = data[['Precipitation (mm)', 'Snowfall (mm)']].interpolate()

            if plot_type == 'line':
                fig1 = px.line(
                    data_frame=data,
                    x='datetime',
                    y=['Precipitation (mm)', 'Snowfall (mm)'],
                    title=f"Snowfall and Precipitation in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"x": "Date/Time", "value": "Weather", "variable": "Category"}
                )
                fig1.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig1 = px.scatter(
                    data_frame=data,
                    x='datetime',
                    y=['Precipitation (mm)', 'Snowfall (mm)'],
                    title=f"Snowfall and Precipitation in {city}: {start_date.date()} to {end_date.date()}",
                    labels={"x": "Date/Time", "value": "Weather", "variable": "Category"}
                )
                fig1.update_traces(mode= 'markers')
            fig1.update_layout(
                template= 'plotly_dark',
                showlegend=True,
                xaxis_type='date',
                hovermode= 'x unified',
                xaxis= dict(
                    showgrid= True,
                    gridcolor= "gray",
                    gridwidth= 0.5
                ),
                yaxis= dict(
                    showgrid= True,
                    gridcolor= 'gray',
                    gridwidth= 0.5
                ))
            st.plotly_chart(fig1)

            # Graph 2: Snowfall and Average Temperature
            st.write("### Graph 2: Snowfall and Average Temperature")
            plot_type = st.selectbox("Select plot type:", ["line", "scatter"], key= f"snowfall_temp_{primary_columns}_{data_type}")
            data[[f"Average Temperature {temp_unit}", "Snowfall (mm)"]] = data[[f"Average Temperature {temp_unit}", "Snowfall (mm)"]].interpolate()

            if plot_type == "line":
                fig2 = go.Figure()
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data["Snowfall (mm)"],
                    name= "Snowfall (mm)",
                    mode= "lines",
                    line= dict(color= 'blue', width= 2)))
                
                fig2.add_trace(go.Line(
                    x=data.index,
                    y= data[f"Average Temperature {temp_unit}"],
                    name= f"Average Temperature {temp_unit}",
                    mode= "lines",
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'))
                fig2.update_traces(mode= 'markers+lines')
                
            elif plot_type == "scatter":
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data["Snowfall (mm)"],
                    name= "Snowfall (mm)",
                    mode= "markers",
                    marker= dict(color= 'blue', size= 8)))
                
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data[f"Average Temperature {temp_unit}"],
                    name= f"Average Temperature {temp_unit}",
                    mode= "markers",
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'))
                fig2.update_traces(mode= 'markers')

            # Add layout for secondary y-axis
            fig2.update_layout(
                template= 'plotly_dark',
                title=f"Snowfall and Average Temperature in {city}: {start_date.date()} to {end_date.date()}",
                xaxis=dict(title="Date"),
                yaxis=dict(title="Snowfall (mm)"),
                yaxis2=dict(
                    title=f"Average Temperature {temp_unit}",
                    overlaying='y',
                    side='right'),
                legend=dict(
                    x=1.0,
                    xanchor='left',
                    y=1.1),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)


        elif primary_columns == 'Wind Speed (km/h)':
            st.write('### Graph 1: Wind Speed and Wind Direction')
            plot_type= st.selectbox("Select plot type:", ['line', 'scatter'], key= f'wsdir_{primary_columns}_{data_type}')
            data[['Wind Direction (°)','Wind Speed (km/h)']] = data[['Wind Direction (°)','Wind Speed (km/h)']].interpolate()
            
            fig1= go.Figure()
            if plot_type == 'line':
                fig1.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))
                fig1.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig1.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig1.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig1.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig1.update_traces(mode= 'markers')

            fig1.update_layout(
                template= 'plotly_dark',
                title= f'Wind Data Visualization in {city}: {start_date.date()} to {end_date.date()}',
                xaxis= dict(title= "Date",
                            showgrid= True),
                yaxis= dict(title= 'Wind Direction (°)', showgrid= True),
                yaxis2= dict(
                    title= 'Wind Speed (km/h)',
                    overlaying= 'y',
                    side= 'right',
                    showgrid= False
                ),
                legend= dict(
                    x= 1.0,
                    xanchor= 'left',
                    y= 1.1
                ),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig1)

            st.write('### Graph 2: Wind Speed and Pressure')
            plot_type= st.selectbox("Select plot type", ['line', 'scatter'], key= f'wpre{primary_columns}_{data_type}')
            data[['Wind Speed (km/h)', 'Pressure (hPa)']] = data[['Wind Speed (km/h)', 'Pressure (hPa)']].interpolate()

            fig2= go.Figure()
            if plot_type == 'line':
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure (hPa)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure (hPa)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers')

            fig2.update_layout(
                template= 'plotly_dark',
                title= f'Wind Speed and Pressure in {city}: {start_date.date()} to {end_date.date()}',
                xaxis_title= 'Date',
                yaxis_title= 'Wind Speed (km/h)',
                yaxis2= dict(title= 'Pressure (hPa)',
                            overlaying= 'y',
                            side= 'right',
                            showgrid= False),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
                )
            st.plotly_chart(fig2)
        
        elif primary_columns == 'Wind Direction (°)':
            st.write('### Graph 1: Wind Direction and Wind Speed')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'wind_dir_plot1_{primary_columns}_{data_type}')
            data[['Wind Direction (°)', 'Wind Speed (km/h)']] = data[['Wind Direction (°)', 'Wind Speed (km/h)']].interpolate()                

            fig1= go.Figure()
            if plot_type== 'line':
                fig1.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))

                fig1.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig1.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig1.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig1.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig1.update_traces(mode= 'markers')

            fig1.update_layout(
                template= 'plotly_dark',
                title= f'Wind Direction and Wind Speed in {city}: {start_date.date()} to {end_date.date()}',
                xaxis= dict(title= 'Date',
                            showgrid= True),
                yaxis= dict(title= 'Wind Direction (°)'),
                yaxis2= dict(title= 'Wind Speed (km/h)',
                            overlaying= 'y',
                            side= 'right',
                            showgrid= False),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
            )   
            st.plotly_chart(fig1)

            st.write('### Graph 2: Wind Direction and Pressure')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'wdpr_{primary_columns}_{data_type}')
            data[['Wind Direction (°)', 'Pressure (hPa)']] = data[['Wind Direction (°)', 'Pressure (hPa)']].interpolate()

            fig2= go.Figure()
            if plot_type== 'line':
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure (hPa)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure (hPa)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers')

            fig2.update_layout(
                template= 'plotly_dark',
                title= f'Wind Direction and Pressure in {city}: {start_date.date()} to {end_date.date()}',
                xaxis= dict(title= 'Date'),
                yaxis= dict(title= 'Wind Direction (°)'),
                yaxis2= dict(title= 'Pressure (hPa)',
                            overlaying= 'y',
                            side= 'right'),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
            )   
            st.plotly_chart(fig2)
        
        elif primary_columns == 'Pressure (hPa)':
            st.write('### Graph 1: Pressure')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'pressure_plot1_{primary_columns}_{data_type}')
            data[['Pressure (hPa)']] = data[['Pressure (hPa)']].interpolate()

            if plot_type == 'line':
                fig1= px.line(
                    data_frame= data,
                    x= 'datetime',
                    y= ['Pressure (hPa)'],
                    title= f'Pressure in {city}: {start_date.date()} to {end_date.date()}',
                    labels= {'value': 'Pressure (hPa)', 'variable': 'Category'}
                )
                fig1.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig1= px.scatter(
                    data_frame= data,
                    x= 'datetime',
                    y= ['Pressure (hPa)'],
                    title= f'Pressure in {city}: {start_date.date()} to {end_date.date()}',
                    labels= {'value': 'Pressure (hPa)', 'variable': 'Category'}
                )
                fig1.update_traces(mode= 'markers')

            fig1.update_layout(
                template= 'plotly_dark',
                showlegend=True,
                xaxis_type='date',
                hovermode= 'x unified',
                xaxis= dict(
                    showgrid= True,
                    gridcolor= "gray",
                    gridwidth= 0.5
                ),
                yaxis= dict(
                    showgrid= True,
                    gridcolor= 'gray',
                    gridwidth= 0.5
                ))
            st.plotly_chart(fig1)

            st.write('### Graph 2: Pressure and Wind Speed')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'pws_{primary_columns}_{data_type}')
            data[['Pressure (hPa)', 'Wind Speed (km/h)']] = data[['Pressure (hPa)', 'Wind Speed (km/h)']].interpolate()

            fig2= go.Figure()
            if plot_type == 'line':
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure (hPa)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Speed (km/h)'],
                    name= 'Wind Speed (km/h)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers')

            fig2.update_layout(
                template= 'plotly_dark',
                title= f'Pressure and Wind Speed in {city}: {start_date.date()} to {end_date.date()}',
                xaxis= dict(title= 'Date'),
                yaxis= dict(title= 'Pressure (hPa)'),
                yaxis2= dict(title= 'Wind Speed (km/h)',
                            overlaying= 'y',
                            side= 'right',
                            showgrid= False),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)

            st.write('### Graph 3: Pressure and Wind Direction')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'prwd_{primary_columns}_{data_type}')
            data[['Pressure (hPa)', 'Wind Direction (°)']]= data[['Pressure (hPa)', 'Wind Direction (°)']].interpolate()

            if plot_type == 'line':
                fig3= go.Figure()
                fig3.add_trace(go.Line(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure (hPa)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))
                fig3.add_trace(go.Line(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig3.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig3= go.Figure()
                fig3.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Pressure (hPa)'],
                    name= 'Pressure (hPa)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig3.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Wind Direction (°)'],
                    name= 'Wind Direction (°)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig3.update_traces(mode= 'markers')

            fig3.update_layout(
                template= 'plotly_dark',
                title= f'Pressure and Wind Direction in {city}: {start_date.date()} to {end_date.date()}',
                xaxis= dict(title= 'Date'),
                yaxis= dict(title= 'Pressure'),
                yaxis2= dict(title= 'Wind Direction',
                            overlaying= 'y',
                            side= 'right',
                            showgrid= False),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig3)

        elif primary_columns == 'Relative Humidity (%)':
            st.write('### Graph 1: Relative Humidity and Dew Point')
            plot_type= st.selectbox("Select Plot Type", ["line", "scatter"], key= f'rh_dp_plot1_{primary_columns}_{data_type}')
            data[['Relative Humidity (%)', 'Dew Point (°C)']] = data[['Relative Humidity (%)', 'Dew Point (°C)']].interpolate()

            fig1= go.Figure()
            if plot_type == 'line':
                # Add the first trace for Wind Direction
                fig1.add_trace(go.Line(
                    x=data.index,
                    y=data['Relative Humidity (%)'],
                    name='Relative Humidity (%)',
                    mode='lines',
                    line=dict(color='blue', width=2)))
                
                # Add the second trace for Wind Speed with a secondary y-axis
                fig1.add_trace(go.Line(
                    x=data.index,
                    y=data['Dew Point (°C)'],
                    name='Dew Point (°C)',
                    mode='lines',
                    line=dict(color='red', width=2),
                    yaxis='y2'))
                fig1.update_traces(mode= 'markers+lines')
                
            elif plot_type == 'scatter':
                fig1.add_trace(go.Scatter(
                    x=data.index,
                    y=data['Relative Humidity (%)'],
                    name="Relative Humidity (%)",
                    mode='markers',
                    marker=dict(color='blue', size=8)))
                fig1.add_trace(go.Scatter(
                    x=data.index,
                    y=data['Dew Point (°C)'],
                    name="Dew Point (°C)",
                    mode='markers',
                    marker=dict(color='red', size=8),
                    yaxis='y2'))
                fig1.update_traces(mode= 'markers')
                
            # Add layout for secondary y-axis
            fig1.update_layout(
                template= 'plotly_dark',
                title=f"Relative Humidity and Dew Point in {city}: {start_date.date()} to {end_date.date()}",
                xaxis=dict(title="Date", showgrid= True),  # Corrected x-axis title
                yaxis=dict(title="Relative Humidity (%)", showgrid= True),  # Primary y-axis title
                yaxis2=dict(
                    title="Dew Point (°C)",  # Secondary y-axis title
                    overlaying='y',  # Overlay secondary y-axis on primary y-axis
                    side='right',
                    showgrid= False),  # Place secondary y-axis on the right
                legend=dict(
                    x=1.0,
                    xanchor='left',
                    y=1.1),
                hovermode= 'x unified')
                
            st.plotly_chart(fig1)

            st.write('### Graph 2: Relative Humidity and Snowfall')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'rhs_{primary_columns}_{data_type}')
            data[['Relative Humidity (%)', 'Snowfall (mm)']] = data[['Relative Humidity (%)', 'Snowfall (mm)']].interpolate()

            fig2= go.Figure()
            if plot_type == 'line':
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Relative Humidity (%)'],
                    name= 'Relative Humidity (%)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Snowfall (mm)'],
                    name= 'Snowfall (mm)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers+lines')
                
            elif plot_type == 'scatter':
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Relative Humidity (%)'],
                    name= 'Relative Humidity (%)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Snowfall (mm)'],
                    name= 'Snowfall (mm)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers')

            fig2.update_layout(
                template= 'plotly_dark',
                title= f"Relative Humidity and Snowfall in {city}: {start_date.date()} to {end_date.date()}",
                xaxis= dict(title= 'Date'),
                yaxis= dict(title= 'Relative Humidity (%)'),
                yaxis2= dict(title= 'Snowfall (mm)',
                            overlaying= 'y',
                            side= 'right',
                            showgrid= False),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)

        elif primary_columns == 'Dew Point (°C)':
            st.write('### Graph 1: Dew Point and Relative Humidity')
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'dw_rh_plot1_{primary_columns}_{data_type}')
            data[['Dew Point (°C)', 'Relative Humidity (%)']] = data[['Dew Point (°C)', 'Relative Humidity (%)']].interpolate()

            if plot_type == 'line':
                fig1= go.Figure()
                fig1.add_trace(go.Line(
                    x= data.index,
                    y= data['Dew Point (°C)'],
                    name= 'Dew Point (°C)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))

                fig1.add_trace(go.Line(
                    x= data.index,
                    y= data['Relative Humidity (%)'],
                    name= 'Relative Humidity (%)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig1.update_traces(mode= 'markers+lines')

            elif plot_type == 'scatter':
                fig1= go.Figure() 
                fig1.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Dew Point (°C)'],
                    name= 'Dew Point (°C)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig1.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Snowfall (mm)'],
                    name= 'Snowfall (mm)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig1.update_traces(mode= 'markers')

            fig1.update_layout(
                template= 'plotly_dark',
                title= f'Dew Point and Relative Humidity in {city}: {start_date.date()} to {end_date.date()}',
                xaxis= dict(title= 'Date', showgrid= True),
                yaxis= dict(title= 'Dew Point', showgrid= True),
                yaxis2= dict(title= 'Relative Humidity',
                            overlaying= 'y',
                            side= 'right',
                            showgrid= False),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig1)

            st.write("### Graph 2: Dew Point and Snowfall")
            plot_type= st.selectbox('Select plot type:', ['line', 'scatter'], key= f'dps_{primary_columns}_{data_type}')
            data[['Dew Point (°C)', 'Snowfall (mm)']] = data[['Dew Point (°C)', 'Snowfall (mm)']].interpolate()

            if plot_type == 'line':
                fig2 = go.Figure()
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Dew Point (°C)'],
                    name= 'Dew Point (°C)',
                    mode= 'lines',
                    line= dict(color= 'blue', width= 2)
                ))
                fig2.add_trace(go.Line(
                    x= data.index,
                    y= data['Snowfall (mm)'],
                    name= 'Snowfall (mm)',
                    mode= 'lines',
                    line= dict(color= 'red', width= 2),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers+lines')
            elif plot_type == 'scatter':
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Dew Point (°C)'],
                    name= 'Dew Point (°C)',
                    mode= 'markers',
                    marker= dict(color= 'blue', size= 8)
                ))
                fig2.add_trace(go.Scatter(
                    x= data.index,
                    y= data['Snowfall (mm)'],
                    name= 'Snowfall (mm)',
                    mode= 'markers',
                    marker= dict(color= 'red', size= 8),
                    yaxis= 'y2'
                ))
                fig2.update_traces(mode= 'markers')
            fig2.update_layout(
                template= 'plotly_dark',
                title= f'Dew Point and Snowfall in {city}: {start_date.date()} to {end_date.date()}',
                xaxis= dict(title= 'Date'),
                yaxis= dict(title= 'Dew Point'),
                yaxis2= dict(title= 'Snowfall',
                            overlaying= 'y',
                            side= 'right',
                            showgrid= False),
                legend= dict(x= 1.0,
                            xanchor= 'left',
                            y= 1.1),
                hovermode= 'x unified'
            )
            st.plotly_chart(fig2)

       
