import pandas as pd
import pyodbc
import streamlit as st

st.title("CRUD")

#VARIABEL DATABASE CONNECTOR
server = 'DESKTOP-J50KKQP'
database ='Data_Games'
username = 'manggala'
password = 'forhimself88'

#koneksi ke db CEK MYODBC klau error
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    f'Trusted_Connection=yes;'
    #f'Trusted_Certificate={path_to_ca_cert_bundle}'
)

data = pd.read_sql_query(f"""
                         SELECT * FROM DATA_GAMES
                         """, conn)
