import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_data(dataframes, offsets, line_positions):
    fig = go.Figure()

    # Plotting the data
    for file_name, df_info in dataframes.items():
        df, selected_columns = df_info
        for col in selected_columns:
            x_offset = offsets.get((file_name, col), {}).get('x', 0)
            y_offset = offsets.get((file_name, col), {}).get('y', 0)
            fig.add_trace(go.Scatter(x=df.index + x_offset, y=df[col] + y_offset, mode='lines', name=f"{file_name} - {col}"))

    # Adding horizontal lines
    for line_y in line_positions:
        fig.add_hline(y=line_y, line_dash="dot", annotation_text=f"y={line_y}", annotation_position="bottom right")

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
st.title("Interactive Multi-Line Data Visualization with Individual Offsets and Horizontal Lines")

# File Uploader for multiple files
uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

dataframes = {}
offsets = {}
line_positions = []

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
                x_offset = st.slider(f"Set X Offset for {col} in {uploaded_file.name}", min_value=-100, max_value=100, value=0, key=f"x_{uploaded_file.name}_{col}")
            with col2:
                y_offset = st.slider(f"Set Y Offset for {col} in {uploaded_file.name}", min_value=-100, max_value=100, value=0, key=f"y_{uploaded_file.name}_{col}")
            
            offsets[(uploaded_file.name, col)] = {'x': x_offset, 'y': y_offset}

# Adding horizontal lines
line_count = st.slider("Select number of horizontal lines", 0, 5, 1)
for i in range(line_count):
    line_y = st.number_input(f"Position of line {i+1}", key=f'line_{i}')
    line_positions.append(line_y)

if st.button("Plot Data"):
    fig = plot_data(dataframes, offsets, line_positions)
    st.plotly_chart(fig, use_container_width=True)

# Save, Print, Reset Buttons
col1, col2, col3 = st.columns(3)
if col1.button("Save Graph"):
    fig.write_image("plot.png")
    st.success("Saved as plot.png")

if col2.button("Print Graph"):
    fig.show(renderer="browser")

if col3.button("Reset Graph"):
    st.experimental_rerun()
