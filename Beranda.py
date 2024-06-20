import streamlit as st
import pandas as pd
import subprocess

st.set_page_config(page_title="Aplikasi K-Medoids")
st.title("Aplikasi Steam Menentukan Penjualan Game Terbaik K-Medoids")

# Function to execute the external script
def run_external_script():
    subprocess.Popen(["C:/Program Files/Python312/python.exe", "e:/CRUD/Steam_Combine.py"])
    
def refresh_page():
    # Reload the page using Streamlit's rerun API
    st.experimental_rerun()

# Read the CSV file
df = pd.read_csv(games_data.csv')

# Display the CSV data
st.subheader("Data CSV hasil Scrapt")
st.dataframe(df)

# Button to run the external script
if st.button("Update Scrap"):
    run_external_script()
    refresh_page()
