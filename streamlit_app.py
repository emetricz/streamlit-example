import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def plot_data(dataframes, offsets):
    fig = go.Figure()

    for file_name, df_info in dataframes.items():
        df, selected_columns = df_info
        for col in selected_columns:
            x_offset = offsets.get((file_name, col), {}).get('x', 0)
            y_offset = offsets.get((file_name, col), {}).get('y', 0)
            fig.add_trace(go.Scatter(x=df.index + x_offset, y=df[col] + y_offset, mode='lines+markers', name=f"{file_name} - {col}"))

    fig.update_layout(
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
        yaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
        dragmode='pan'
    )

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(hovermode='x')
    return fig

def calculate_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Streamlit App
st.title("Interactive Multi-Line Data Visualization with Distance Measurement")

# File Uploader for multiple files
uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

dataframes = {}
offsets = {}

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.write(f"Data from: {uploaded_file.name}")
        st.dataframe(df.head())

        # Select columns to plot
        selected_columns = st.multiselect(f"Select columns to plot from {uploaded_file.name}", df.columns)
        dataframes[uploaded_file.name] = (df, selected_columns)

    if st.button("Plot Data"):
        fig = plot_data(dataframes, offsets)
        st.plotly_chart(fig, use_container_width=True)

# Distance Measurement
st.write("Distance Measurement:")
col1, col2 = st.columns(2)
with col1:
    point1_x = st.number_input("Point 1 X", key="p1x")
    point1_y = st.number_input("Point 1 Y", key="p1y")
with col2:
    point2_x = st.number_input("Point 2 X", key="p2x")
    point2_y = st.number_input("Point 2 Y", key="p2y")

if st.button("Calculate Distance"):
    distance = calculate_distance((point1_x, point1_y), (point2_x, point2_y))
    st.write(f"Distance: {distance}")

# Save, Print, Reset Buttons
col1, col2, col3 = st.columns(3)
if col1.button("Save Graph"):
    fig.write_image("plot.png")
    st.success("Saved as plot.png")

if col2.button("Print Graph"):
    fig.show(renderer="browser")

if col3.button("Reset Graph"):
    st.experimental_rerun()
