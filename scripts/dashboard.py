import streamlit as st
import plotly.graph_objects as go

def create_dashboard():
    st.title("Trading System Dashboard")
    
    # Performance Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Win Rate", "67%")
    col2.metric("Total Return", "+23.5%")
    col3.metric("Active Trades", "3")
    
    # Trading History Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=cumulative_returns))
    st.plotly_chart(fig) 