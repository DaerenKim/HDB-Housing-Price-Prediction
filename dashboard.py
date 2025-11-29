import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import random

# ------------------------------
# Load Dataset
# ------------------------------
datafile = "data/cleaned_resale_flat_price.csv"
df = pd.read_csv(datafile)

# Log price for later use
df['resale_price_log'] = np.log(df['resale_price'])

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Housing Price Dashboard", page_icon=":bar_chart:", layout='wide')
st.markdown(    """
            <h1 style="
                text-align:center;
                margin-top: 0px;
                margin-bottom: 0px;
                padding: 0px;
            ">
                🏠 Housing Price Dashboard
            </h1>
            """, 
            unsafe_allow_html=True)

# ------------------------------
# Sidebar Configuration
# ------------------------------
st.sidebar.header("Filters")
st.sidebar.subheader("Select Towns")

# Create checklist for towns
selected_towns = []
for town in sorted(df['town'].unique()):
    if st.sidebar.checkbox(town, value=True):
        selected_towns.append(town)

# Filter dataset based on selection
filtered_df = df[df['town'].isin(selected_towns)]

if filtered_df.empty:
    st.warning("No towns selected or no data available. Please select at least one town.")
    st.stop()

# ------------------------------
# Helper Functions
# ------------------------------

def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
            },
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=150,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Visualisation Methods
# ------------------------------
def plot_top_left():
    # Average Price Increase since 2017
    avg_price_2017 = filtered_df[filtered_df['year'] == 2017]['resale_price'].mean()
    avg_price_2024 = filtered_df[filtered_df['year'] == 2024]['resale_price'].mean()
    price_increase = avg_price_2024 - avg_price_2017
    pct_increase = (price_increase / avg_price_2017) * 100

    st.markdown(
        '<h4 style="color:red; text-align:center;">Average Price Increase <br>(2017 → 2024)</h4>',
        unsafe_allow_html=True
    )

    # Optional: gauge for % increase
    plot_gauge(
        pct_increase,
        "red",
        "%",
        "",
        max_bound=100
    )

def plot_top_mid():
    # Most Expensive Town and Most Expensive Flat Type
    most_expensive_region = filtered_df.groupby('town')['resale_price'].mean().idxmax()
    most_expensive_region_price = filtered_df.groupby('town')['resale_price'].mean().max()

    top3_expensive_streets = (
        filtered_df.groupby('street_name')['resale_price'].mean()
        .sort_values(ascending=False)
        .head(3)
    )
    max_price_flat_type = filtered_df.groupby('flat_type')['resale_price'].mean().idxmax()
    max_price_flat_type_value = filtered_df.groupby('flat_type')['resale_price'].mean().max()

    plot_metric(
        f"Most Expensive Town:<br>{most_expensive_region}",
        most_expensive_region_price,
        prefix="$",
        show_graph=True,
        color_graph="rgba(0, 200, 83, 0.2)",
    )
    plot_metric(
        f"Most Expensive Flat Type:<br>{max_price_flat_type}",
        max_price_flat_type_value,
        prefix="$",
        show_graph=True,
        color_graph="rgba(0, 104, 201, 0.2)",
    )

def plot_top_right():
    # Top Lease Commence Years + Predict Next
    top_3_years = [1985, 2000, 2015]
    next_pred_year = 2030

    st.markdown(
        '<h4 style="color:black; margin-bottom: 5px; text-align: center;">Top Lease Commence Peaks</h4>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            font-size: 17px;
            line-height: 1.6;
            text-align: center;
            width: 100%;
        ">
            <ol style="
                margin: 0 auto;
                display: inline-block;
                text-align: left;
            ">
                <li><b>1985</b></li>
                <li><b>2000</b></li>
                <li><b>2015</b></li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            margin-top: 10px;
            font-size: 17px;
            background-color: #fff3cd;
            padding: 12px 14px;
            border-radius: 8px;
            border-left: 5px solid #ffb300;
            text-align: center;
        ">
            🔮 <b>Predicted Next Peak:</b> {next_pred_year}
        </div>
        """,
        unsafe_allow_html=True
    )


def plot_bot_left():
    # Top 10 Average Price by Town
    avg_price_town = (
        filtered_df.groupby('town')['resale_price']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig1 = px.bar(
        avg_price_town,
        x='town',
        y='resale_price',
        color='resale_price',
        color_continuous_scale=['#48CAE4', '#3399FF'],
        labels={'town':'Town', 'resale_price':'Average Resale Price'},
        title="Top 10 Average Price by Town"
    )
    fig1.update_coloraxes(showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

def plot_bot_mid():
    # Resale Price Distribution by Flat Type
    avg_price_type = (
        filtered_df.groupby('flat_type')['resale_price']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig2 = px.bar(
        avg_price_type,
        y='flat_type',
        x='resale_price',
        orientation='h',
        color='resale_price',
        color_continuous_scale=['#00ffff', '#3399FF'],
        labels={'flat_type':'Flat Type', 'resale_price':'Average Resale Price'},
        title="Resale Price Distribution by Flat Type"
    )
    fig2.update_coloraxes(showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

def plot_bot_right():
    top_towns = filtered_df.groupby('town')['resale_price'].mean().nlargest(5).index
    price_trend = (
        filtered_df[filtered_df['town'].isin(top_towns)]
        .groupby(['town', 'year'])['resale_price']
        .mean()
        .reset_index()
    )
    fig3 = px.line(
        price_trend,
        x='year',
        y='resale_price',
        color='town',
        labels={'year':'Year', 'resale_price':'Avg Resale Price'},
        title="Resale Price Trend Over Years (Top 5 Towns)"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ------------------------------
# Streamlit Layout
# ------------------------------
# Create 3 columns for metrics
col1, col2, col3 = st.columns(3)

# Column 1: Average Price Increase since 2017 
with col1:
    plot_top_left()

# Column 2: Most Expensive Town and Most Expensive Flat Type
with col2:
    plot_top_mid()

# Column 3: Top Lease Commence Years + Predict Next
with col3:
    plot_top_right()

with st.container():
    col1, col2, col3 = st.columns(3)
    
    # Column 1: Top 10 Average Price by Town
    with col1:
        plot_bot_left()
    
    # Column 2: Resale Price Distribution by Flat Type
    with col2:
        plot_bot_mid()
    
    # Column 3: Resale Price Trend Over Years (Top 5 Towns)
    with col3:
        plot_bot_right()
