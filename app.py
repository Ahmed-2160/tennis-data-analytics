import streamlit as st
import pandas as pd
import mysql.connector

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root",  # replace with your actual MySQL password
        database="tennis_db"
    )



st.title("🎾 Tennis Data Analytics Dashboard")

conn = get_connection()
cursor = conn.cursor()

# Example: total players
cursor.execute("SELECT COUNT(*) FROM players")
total_players = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT nationality) FROM players")
total_countries = cursor.fetchone()[0]

st.metric("Total Players", total_players)
st.metric("Countries Represented", total_countries)




st.header("🔍 Search Players")
name = st.text_input("Enter player name")
if name:
    query = f"SELECT * FROM players WHERE name LIKE '%{name}%'"
    df = pd.read_sql(query, conn)
    st.dataframe(df)




st.header("🌍 Country-wise Analysis")
query = """
SELECT nationality, COUNT(*) as num_players
FROM players
GROUP BY nationality
ORDER BY num_players DESC
"""
df = pd.read_sql(query, conn)
st.bar_chart(df.set_index("nationality"))



st.header("🏆 Leaderboard - Top Players (by Ranking)")
query = "SELECT name, nationality, ranking FROM players WHERE ranking IS NOT NULL ORDER BY ranking ASC LIMIT 10"
df = pd.read_sql(query, conn)
st.table(df)

