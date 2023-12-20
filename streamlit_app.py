import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_data(file):
    return pd.read_csv(file)

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
st.title("Interactive Data Visualization")

# File Uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)
    columns = st.multiselect('Select columns to plot', data.columns)

    # Axis Manipulation
    x_origin = st.slider("Adjust X Origin", min_value=0, max_value=len(data), value=0)
    y_origin = st.slider("Adjust Y Origin", min_value=int(data[columns].min().min()), max_value=int(data[columns].max().max()), value=0)

    # Plotting
    fig = plot_data(data, x_origin, y_origin, columns)
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
