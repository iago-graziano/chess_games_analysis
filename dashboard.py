"""
Streamlit Interactive Dashboard for Chess Games Analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from utils import load_chess_data, preprocess_data, get_opening_category

# Page configuration
st.set_page_config(
    page_title="Chess Games Analysis Dashboard",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #ecf0f1;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">♟️ Chess Games Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("📊 Dashboard Controls")

# Data loading
@st.cache_data
def load_data(sample_size=500000):
    """Load and cache chess games data"""
    try:
        df_raw = load_chess_data('chess_games.csv', sample_size=sample_size)
        df = preprocess_data(df_raw)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Sidebar controls
sample_size = st.sidebar.slider(
    "Sample Size",
    min_value=10000,
    max_value=1000000,
    value=500000,
    step=50000,
    help="Adjust the number of games to analyze (larger samples take longer to load)"
)

# Load data
with st.spinner("Loading chess games data..."):
    df = load_data(sample_size=sample_size)

if df is None or df.empty:
    st.error("Failed to load data. Please check that chess_games.csv exists in the project directory.")
    st.stop()

# Sidebar filters
st.sidebar.subheader("🔍 Filters")

# Time control filter
time_controls = ['All'] + sorted(df['TimeControl_Grouped'].dropna().unique().tolist())
selected_time_control = st.sidebar.selectbox("Time Control", time_controls)

# ELO range filter
min_elo = int(df[['WhiteElo', 'BlackElo']].min().min())
max_elo = int(df[['WhiteElo', 'BlackElo']].max().max())
elo_range = st.sidebar.slider(
    "Average ELO Range",
    min_value=min_elo,
    max_value=max_elo,
    value=(min_elo, max_elo),
    step=100
)

# Apply filters
df_filtered = df.copy()
if selected_time_control != 'All':
    df_filtered = df_filtered[df_filtered['TimeControl_Grouped'] == selected_time_control]
df_filtered = df_filtered[
    (df_filtered['AvgElo'] >= elo_range[0]) &
    (df_filtered['AvgElo'] <= elo_range[1])
]

# Key metrics
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Games", f"{len(df_filtered):,}")
with col2:
    white_wins = (df_filtered['Result'] == '1-0').sum()
    st.metric("White Wins", f"{white_wins:,}", f"{white_wins/len(df_filtered)*100:.1f}%")
with col3:
    black_wins = (df_filtered['Result'] == '0-1').sum()
    st.metric("Black Wins", f"{black_wins:,}", f"{black_wins/len(df_filtered)*100:.1f}%")
with col4:
    draws = (df_filtered['Result'] == '1/2-1/2').sum()
    st.metric("Draws", f"{draws:,}", f"{draws/len(df_filtered)*100:.1f}%")

st.markdown("---")

# Visualization tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Game Results",
    "⭐ ELO Analysis",
    "📖 Openings",
    "⏱️ Time Controls",
    "📅 Temporal Patterns"
])

# Tab 1: Game Results
with tab1:
    st.header("Game Results Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Results distribution pie chart
        result_counts = df_filtered['Result'].value_counts()
        result_labels = {'1-0': 'White Wins', '0-1': 'Black Wins', '1/2-1/2': 'Draw'}
        result_counts_labeled = result_counts.rename(index=result_labels)

        fig_pie = px.pie(
            values=result_counts_labeled.values,
            names=result_counts_labeled.index,
            title="Game Results Distribution",
            color_discrete_map={'White Wins': '#3498db', 'Black Wins': '#e74c3c', 'Draw': '#95a5a6'}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Termination reasons
        termination_counts = df_filtered['Termination'].value_counts().head(10)
        fig_bar = px.bar(
            x=termination_counts.values,
            y=termination_counts.index,
            orientation='h',
            title="Top 10 Game Termination Reasons",
            labels={'x': 'Number of Games', 'y': 'Termination Reason'},
            color=termination_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# Tab 2: ELO Analysis
with tab2:
    st.header("ELO Rating Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # ELO distribution
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df_filtered['WhiteElo'].dropna(),
            name='White ELO',
            opacity=0.7,
            marker_color='#3498db'
        ))
        fig_hist.add_trace(go.Histogram(
            x=df_filtered['BlackElo'].dropna(),
            name='Black ELO',
            opacity=0.7,
            marker_color='#e74c3c'
        ))
        fig_hist.update_layout(
            title="ELO Rating Distribution",
            xaxis_title="ELO Rating",
            yaxis_title="Frequency",
            barmode='overlay'
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # ELO difference vs win rate
        df_filtered['EloDiff'] = abs(df_filtered['WhiteElo'] - df_filtered['BlackElo'])
        df_filtered['HigherEloWins'] = (
            ((df_filtered['WhiteElo'] > df_filtered['BlackElo']) & (df_filtered['Result'] == '1-0')) |
            ((df_filtered['BlackElo'] > df_filtered['WhiteElo']) & (df_filtered['Result'] == '0-1'))
        )

        df_filtered['EloDiffBin'] = pd.cut(
            df_filtered['EloDiff'],
            bins=[0, 50, 100, 200, 500, 1000],
            labels=['0-50', '50-100', '100-200', '200-500', '500+']
        )

        win_rate_by_elo_diff = df_filtered.groupby('EloDiffBin')['HigherEloWins'].mean() * 100

        fig_bar = px.bar(
            x=win_rate_by_elo_diff.index.astype(str),
            y=win_rate_by_elo_diff.values,
            title="Win Rate of Higher Rated Player by ELO Difference",
            labels={'x': 'ELO Difference', 'y': 'Win Rate (%)'},
            color=win_rate_by_elo_diff.values,
            color_continuous_scale='Greens'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Draw rate by ELO
    st.subheader("Draw Rate by Average ELO")
    df_filtered['AvgEloBin'] = pd.cut(
        df_filtered['AvgElo'],
        bins=[0, 1000, 1200, 1400, 1600, 1800, 2000, 3000],
        labels=['<1000', '1000-1200', '1200-1400', '1400-1600', '1600-1800', '1800-2000', '2000+']
    )

    draw_rate_by_elo = df_filtered.groupby('AvgEloBin')['Draw'].mean() * 100

    fig_bar = px.bar(
        x=draw_rate_by_elo.index.astype(str),
        y=draw_rate_by_elo.values,
        title="Draw Rate by Average Player ELO",
        labels={'x': 'Average ELO Range', 'y': 'Draw Rate (%)'},
        color=draw_rate_by_elo.values,
        color_continuous_scale='Purples'
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# Tab 3: Openings
with tab3:
    st.header("Chess Openings Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Top openings
        top_openings = df_filtered['Opening'].value_counts().head(15)
        fig_bar = px.bar(
            x=top_openings.values,
            y=top_openings.index,
            orientation='h',
            title="Top 15 Most Popular Openings",
            labels={'x': 'Number of Games', 'y': 'Opening'},
            color=top_openings.values,
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Opening categories
        df_filtered['OpeningCategory'] = df_filtered['ECO'].apply(get_opening_category)
        opening_cat_counts = df_filtered['OpeningCategory'].value_counts()

        fig_pie = px.pie(
            values=opening_cat_counts.values,
            names=opening_cat_counts.index,
            title="Openings by Category (ECO)",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Outcomes by opening category
    st.subheader("Game Outcomes by Opening Category")
    opening_outcomes = df_filtered.groupby('OpeningCategory')['Result'].value_counts(normalize=True).unstack(fill_value=0) * 100

    fig_bar = px.bar(
        opening_outcomes,
        title="Game Outcomes by Opening Category",
        labels={'value': 'Percentage (%)', 'OpeningCategory': 'Opening Category'},
        color_discrete_map={'1-0': '#3498db', '0-1': '#e74c3c', '1/2-1/2': '#95a5a6'}
    )
    fig_bar.update_layout(xaxis_title="Opening Category", yaxis_title="Percentage (%)")
    st.plotly_chart(fig_bar, use_container_width=True)

# Tab 4: Time Controls
with tab4:
    st.header("Time Control Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Time control distribution
        time_control_counts = df_filtered['TimeControl_Grouped'].value_counts()
        fig_pie = px.pie(
            values=time_control_counts.values,
            names=time_control_counts.index,
            title="Time Control Distribution",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Outcomes by time control
        time_outcomes = df_filtered.groupby('TimeControl_Grouped')['Result'].value_counts(normalize=True).unstack(fill_value=0) * 100

        fig_bar = px.bar(
            time_outcomes,
            title="Game Outcomes by Time Control",
            labels={'value': 'Percentage (%)', 'TimeControl_Grouped': 'Time Control'},
            color_discrete_map={'1-0': '#3498db', '0-1': '#e74c3c', '1/2-1/2': '#95a5a6'}
        )
        fig_bar.update_layout(xaxis_title="Time Control", yaxis_title="Percentage (%)")
        st.plotly_chart(fig_bar, use_container_width=True)

# Tab 5: Temporal Patterns
with tab5:
    st.header("Temporal Patterns")

    col1, col2 = st.columns(2)

    with col1:
        # Games by hour
        games_by_hour = df_filtered['Hour'].value_counts().sort_index()
        fig_line = px.line(
            x=games_by_hour.index,
            y=games_by_hour.values,
            title="Games Played by Hour of Day (UTC)",
            labels={'x': 'Hour of Day (UTC)', 'y': 'Number of Games'},
            markers=True
        )
        fig_line.update_traces(fill='tonexty', fillcolor='rgba(230, 126, 34, 0.3)', line_color='#e67e22')
        fig_line.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=2))
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        # Games by day of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        games_by_day = df_filtered['DayOfWeek'].value_counts().reindex(day_order)

        fig_bar = px.bar(
            x=games_by_day.index,
            y=games_by_day.values,
            title="Games Played by Day of Week",
            labels={'x': 'Day of Week', 'y': 'Number of Games'},
            color=games_by_day.values,
            color_continuous_scale='Greys'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d; padding: 2rem;'>
        <p>Chess Games Analysis Dashboard | Data from lichess.org (July 2016)</p>
        <p>Built with Streamlit, Plotly, and Pandas</p>
    </div>
    """,
    unsafe_allow_html=True
)
