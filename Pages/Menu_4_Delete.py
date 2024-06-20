import pandas as pd
import pyodbc
import streamlit as st

st.title("Menu Delete Data")


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
# Price = st.text_input("Price")
# Final_Price = st.text_input("Final Price")

# if st.button("Delete Data"): 
#     title_to_delete = st.text_input("Enter Title to Delete")
    
#     if title_to_delete:
#         # Execute the DELETE query to delete the record
#         cursor.execute("""
#                        DELETE FROM DATA_GAMES 
#                        WHERE title = ?;
#                        """, (title_to_delete,))
        
#         # Execute the UPDATE query to set rank_game to -1
#         cursor.execute("""
#                        UPDATE DATA_GAMES 
#                        SET rank_game = -1 
#                        WHERE title = ?;
#                        """, (title_to_delete,))
        
#         # Commit the transaction
#         conn.commit()
        
#         # Display success message
#         st.success("User Berhasil Delete Data")


if st.button("Delete Data"): 
    cursor.execute(f"""
               DELETE FROM DATA_GAMES 
               WHERE
               title = ?
               """, (Title))
    conn.commit()
    # cursor.execute(f"""
    #            UPDATE DATA_GAMES
    #            SET rank_game = -1 
    #            WHERE
    #            title = ?
    #            """, (Title))
    # conn.commit()
    st.success("User Berhasil Delete Data")


# DELETE FROM DATA_GAMES WHERE title = ?;