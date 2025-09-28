import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # or your actual MySQL username
        password="Root",      # or your actual password
        database="db_schema"
    )