import pandas as pd
import pyodbc
import streamlit as st

st.title("Menu Update Data")

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
cursor = conn.cursor()

#variabel input
st.subheader("Masukan Title Game :")
Title = st.text_input("Title")

st.subheader("Masukan Harga Awal Game :")
Price = st.text_input("Price")

if st.button("Update Price Awal Data"):
    # Persen_Disc = int(((int(Price) - int(Final_Price)) / int(Price)) * 100) 
    cursor.execute(f"""
               UPDATE DATA_GAMES
               SET 
                price = ?   
               WHERE
                title = ?
               """, (Price, Title))
    conn.commit()
    st.success("User Berhasil Update Data Price")

st.subheader("Masukan Harga Final Game :")
Final_Price = st.text_input("Final Price")

if st.button("Update Price Final Data"):
    # Persen_Disc = int(((int(Price) - int(Final_Price)) / int(Price)) * 100) 
    cursor.execute(f"""
               UPDATE DATA_GAMES
               SET 
                final_price = ?    
               WHERE
                title = ?
               """, (Final_Price, Title))
    conn.commit()
    st.success("User Berhasil Update Data Final Price")
    
# UPDATE DATA_GAMES
#     SET price = 50000
# Where
#     title = 'tes'