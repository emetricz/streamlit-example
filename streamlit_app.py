import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_data(dataframes, offsets, h_lines, v_lines):
    fig = go.Figure()

    # Plotting the data
    for file_name, df_info in dataframes.items():
        df, selected_columns = df_info
        for col in selected_columns:
            x_offset = offsets.get((file_name, col), {}).get('x', 0)
            y_offset = offsets.get((file_name, col), {}).get('y', 0)
            fig.add_trace(go.Scatter(x=df.index + x_offset, y=df[col] + y_offset, mode='lines', name=f"{file_name} - {col}"))

    # Adding lines and calculating deltas
    h_deltas = []
    v_deltas = []
    for i in range(len(h_lines) - 1):
        h_deltas.append(abs(h_lines[i] - h_lines[i+1]))
        fig.add_hline(y=h_lines[i], line_dash="dash", line_color="red")
    if h_lines:
        fig.add_hline(y=h_lines[-1], line_dash="dash", line_color="red")

    for i in range(len(v_lines) - 1):
        v_deltas.append(abs(v_lines[i] - v_lines[i+1]))
        fig.add_vline(x=v_lines[i], line_dash="dash", line_color="blue")
    if v_lines:
        fig.add_vline(x=v_lines[-1], line_dash="dash", line_color="blue")

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
    return fig, h_deltas, v_deltas

# Streamlit App
st.title("Interactive Multi-Line Data Visualization with Delta Calculation")

# File Uploader for multiple files
uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

dataframes = {}
offsets = {}
h_lines = []
v_lines = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.write(f"Data from: {uploaded_file.name}")
        st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select columns to plot from {uploaded_file.name}", df.columns)
        dataframes[uploaded_file.name] = (df, selected_columns)

# Line and Offset Controls
st.sidebar.title("Line Controls")
with st.sidebar:
    st.subheader("Horizontal Lines")
    h_line_count = st.number_input("Number of horizontal lines", 0, 5, 0)
    h_lines = [st.number_input(f"Y position of line {i+1}", value=0.0, key=f"h_line_{i}") for i in range(h_line_count)]

    st.subheader("Vertical Lines")
    v_line_count = st.number_input("Number of vertical lines", 0, 5, 0)
    v_lines = [st.number_input(f"X position of line {i+1}", value=0.0, key=f"v_line_{i}") for i in range(v_line_count)]

st.write("Offset Controls:")
for uploaded_file in uploaded_files:
    for col in dataframes[uploaded_file.name][1]:
        col1, col2 = st.columns(2)
        with col1:
            x_offset = st.number_input(f"X Offset for {col} in {uploaded_file.name}", value=0, key=f"x_{uploaded_file.name}_{col}")
        with col2:
            y_offset = st.number_input(f"Y Offset for {col} in {uploaded_file.name}", value=0, key=f"y_{uploaded_file.name}_{col}")
        offsets[(uploaded_file.name, col)] = {'x': x_offset, 'y': y_offset}

# Plotting and Displaying Deltas
if st.button("Plot Data"):
    fig, h_deltas, v_deltas = plot_data(dataframes, offsets, h_lines, v_lines)
    st.plotly_chart(fig, use_container_width=True)

    if h_deltas:
        st.write(f"Delta Y between Horizontal Lines: {h_deltas}")
    if v_deltas:
        st.write(f"Delta X between Vertical Lines: {v_deltas}")

# Save, Print, Reset Buttons
col1, col2 = st.columns(2)
if col1.button("Save Graph"):
    fig.write_html("plot.html")
    st.success("Saved as plot.html")

if col2.button("Reset Graph"):
    st.experimental_rerun()
