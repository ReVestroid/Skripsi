import pandas as pd
import pyodbc
import streamlit as st

st.title("Menu Insert Data")

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
Title = st.text_input("Title")
Price = st.text_input("Price")
Final_Price = st.text_input("Final Price")

if st.button("Input Data"): 
    Persen_Disc = int(((int(Price) - int(Final_Price)) / int(Price)) * 100)
    cursor.execute(f"""
               INSERT INTO DATA_GAMES
               (title, price, final_price, persen_disc)
               VALUES
               (?,?,?,?)
               """, (Title, Price, Final_Price, Persen_Disc))
    conn.commit()
    st.success("User Berhasil Input Data")
    


##CREATE TABLE DATA_GAMES(
##	rank_game int identity(1,1) PRIMARY KEY,
##	title varchar(225) NOT NULL,
##	price int ,
##	final_price int,
##-);

##INSERT INTO DATA_GAMES
##VALUES
##	('Counter-Strike 2',0,0)