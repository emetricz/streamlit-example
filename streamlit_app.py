import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_data(dataframes, line_names):
    fig = go.Figure()

    for file_name, df_info in dataframes.items():
        df, selected_columns = df_info
        for col in selected_columns:
            line_name = line_names.get(file_name, {}).get(col, col)
            fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=line_name))

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
line_names = {}

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.write(f"Data from: {uploaded_file.name}")
        st.dataframe(df.head())

        # Select columns to plot
        selected_columns = st.multiselect(f"Select columns to plot from {uploaded_file.name}", df.columns)
        dataframes[uploaded_file.name] = (df, selected_columns)

        # Rename line names
        for col in selected_columns:
            default_name = f"{uploaded_file.name} - {col}"
            line_name = st.text_input(f"Rename line for {col} in {uploaded_file.name}", value=default_name)
            if line_name:
                line_names.setdefault(uploaded_file.name, {})[col] = line_name

    if st.button("Plot Data"):
        fig = plot_data(dataframes, line_names)
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
