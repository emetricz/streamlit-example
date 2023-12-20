import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_data(data, x_origin, y_origin, columns):
    fig = go.Figure()

    for col in columns:
        fig.add_trace(go.Scatter(x=data.index - x_origin, y=data[col] - y_origin, mode='lines', name=col))

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
st.title("Interactive Data Visualization with Multiple CSVs")

# File Uploader for multiple files
uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)
dataframes = {}

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Reading each file
        df = pd.read_csv(uploaded_file)
        st.write(f"Data from: {uploaded_file.name}")
        st.dataframe(df.head())

        # Allow user to rename columns
        new_column_names = st.text_input(f"Rename columns for {uploaded_file.name} (comma-separated)", value=",".join(df.columns))
        if new_column_names:
            df.columns = [name.strip() for name in new_column_names.split(",")]

        dataframes[uploaded_file.name] = df

    # Selecting a dataframe to plot
    file_to_plot = st.selectbox("Select a file to plot", options=list(dataframes.keys()))
    selected_df = dataframes[file_to_plot]
    columns_to_plot = st.multiselect("Select columns to plot", selected_df.columns)

    # Axis Manipulation
    x_origin = st.slider("Adjust X Origin", min_value=0, max_value=len(selected_df), value=0)
    y_origin = st.slider("Adjust Y Origin", min_value=int(selected_df[columns_to_plot].min().min()), max_value=int(selected_df[columns_to_plot].max().max()), value=0)

    # Plotting
    if columns_to_plot:
        fig = plot_data(selected_df, x_origin, y_origin, columns_to_plot)
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
