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

    # Adding lines
    for y in h_lines:
        fig.add_hline(y=y, line_dash="dash", line_color="red")
    for x in v_lines:
        fig.add_vline(x=x, line_dash="dash", line_color="blue")

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

# Streamlit App
st.title("Interactive Multi-Line Data Visualization")

# File Uploader for multiple files
uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

dataframes = {}
offsets = {}
h_lines = [2.0, 3.0]  # Default horizontal lines
v_lines = [1.0, 2.0]  # Default vertical lines

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.write(f"Data from: {uploaded_file.name}")
        st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select columns to plot from {uploaded_file.name}", df.columns)
        dataframes[uploaded_file.name] = (df, selected_columns)

# Offset Controls
st.write("Offset Controls:")
for uploaded_file in uploaded_files:
    for col in dataframes[uploaded_file.name][1]:
        col1, col2 = st.columns(2)
        with col1:
            x_offset = st.number_input(f"X Offset for {col} in {uploaded_file.name}", value=0, key=f"x_{uploaded_file.name}_{col}")
        with col2:
            y_offset = st.number_input(f"Y Offset for {col} in {uploaded_file.name}", value=0, key=f"y_{uploaded_file.name}_{col}")
        offsets[(uploaded_file.name, col)] = {'x': x_offset, 'y': y_offset}

# Plotting
if st.button("Plot Data"):
    fig = plot_data(dataframes, offsets, h_lines, v_lines)
    st.plotly_chart(fig, use_container_width=True)

# Reset Button
if st.button("Reset Graph"):
    st.experimental_rerun()
