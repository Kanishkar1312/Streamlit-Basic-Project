import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kanishkar@1312',
    'database': 'SPORTSRADARTENNIS'
}

def connect_db():
    return pymysql.connect(**DB_CONFIG)

def run_query(query, params=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(results, columns=cols)

def get_competitions():
    return run_query("SELECT * FROM competitions")

def get_categories():
    return run_query("SELECT * FROM categories")

def get_rankings():
    return run_query("""
        SELECT r.id, r.name, r.year, r.week, c.name as competitor_name, cr.rank, cr.points
        FROM rankings r
        JOIN competitor_rankings cr ON r.id = cr.ranking_id
        JOIN competitors c ON c.id = cr.competitor_id
    """)

st.set_page_config(page_title="Tennis Dashboard", layout="wide")
st.title("🎾 SportsRadar Tennis Dashboard")

# Sidebar filters
category_df = get_categories()
category_options = category_df["name"].tolist()
selected_category = st.sidebar.selectbox("Select Category", category_options)

competition_df = get_competitions()
filtered_competitions = competition_df[competition_df["category_id"] == category_df[category_df["name"] == selected_category]["id"].values[0]]

# Show competition data
st.subheader("Competitions in Selected Category")
st.dataframe(filtered_competitions)

# Rankings
ranking_df = get_rankings()
st.subheader("Player Rankings")
st.dataframe(ranking_df)

# Chart
chart = px.bar(ranking_df.head(10), x="competitor_name", y="points", color="rank",
               title="Top 10 Players by Points")
st.plotly_chart(chart, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Built with Streamlit and MySQL ❤️")
