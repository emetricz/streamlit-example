import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
        yaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
        dragmode='pan'
    )

    fig.update_xaxes(rangeslider_visible=True)
    return fig

# Streamlit App
st.title("Interactive Multi-Line Data Visualization with Point Selection")

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

        # Set offsets for each line
        for col in selected_columns:
            col1, col2 = st.columns(2)
            with col1:
                x_offset = st.slider(f"X Offset for {col} in {uploaded_file.name}", min_value=-100, max_value=100, value=0, key=f"x_{uploaded_file.name}_{col}")
            with col2:
                y_offset = st.slider(f"Y Offset for {col} in {uploaded_file.name}", min_value=-100, max_value=100, value=0, key=f"y_{uploaded_file.name}_{col}")
            
            offsets[(uploaded_file.name, col)] = {'x': x_offset, 'y': y_offset}

    if st.button("Plot Data"):
        fig = plot_data(dataframes, offsets)
        st.plotly_chart(fig, use_container_width=True)

# Manual Input for Point Selection
col1, col2 = st.columns(2)
with col1:
    point1_x = st.number_input("Point 1 X Value", value=0)
    point1_y = st.number_input("Point 1 Y Value", value=0)

with col2:
    point2_x = st.number_input("Point 2 X Value", value=0)
    point2_y = st.number_input("Point 2 Y Value", value=0)

# Calculate and Display Differences
if st.button("Calculate Difference"):
    diff_x = point2_x - point1_x
    diff_y = point2_y - point1_y
    st.write(f"Difference in X: {diff_x}")
    st.write(f"Difference in Y: {diff_y}")

# Save, Print, Reset Buttons
col1, col2, col3 = st.columns(3)
if col1.button("Save Graph"):
    fig.write_image("plot.png")
    st.success("Saved as plot.png")
