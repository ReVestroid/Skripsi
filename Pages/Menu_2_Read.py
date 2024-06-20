import pandas as pd
import pyodbc
import streamlit as st

st.title("Data pada Database SQL")

# VARIABEL DATABASE CONNECTOR
server = 'DESKTOP-J50KKQP'
database ='Data_Games'
username = 'manggala'
password = 'forhimself88'

# Koneksi ke db
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    f'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Read data from CSV
df = pd.read_csv(r'E:\CRUD\games_data.csv')

def import_to_sql(df):
    for _, row in df.iterrows():
        title = row['title']
        price = row['price']
        disc_price = row['disc_price']
        persen_disc = row['persen_disc']

        cursor.execute("""
                       INSERT INTO DATA_GAMES 
                       (title, price, final_price, persen_disc)
                       VALUES 
                       (?, ?, ?, ?);
                       """, (title, price, disc_price, persen_disc))
        
    conn.commit()
    st.success("Data imported successfully!")

def truncate_table():
    cursor.execute("TRUNCATE TABLE DATA_GAMES;")
    conn.commit()
    st.success("Table DATA_GAMES is Empty!")

# Read data from SQL table
data = pd.read_sql_query("SELECT * FROM DATA_GAMES", conn)
st.table(data)

# Button trigger data import
if st.button("Import Data Scrapt Ke Tabel"):
    truncate_table()
    import_to_sql(df)
    st.experimental_rerun()

# Button truncate the table
if st.button("Delete Semua Data Pada Tabel"):
    truncate_table()
    st.experimental_rerun()
    

# data = pd.read_sql_query(f"""
#                          SELECT * FROM DATA_GAMES
#                          """, conn)

# st.table(data)