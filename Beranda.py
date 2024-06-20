import streamlit as st
import pandas as pd
import subprocess

st.set_page_config(page_title="Aplikasi K-Medoids")
st.title("Aplikasi Steam Menentukan Penjualan Game Terbaik K-Medoids")

def main():
    st.sidebar.title('Sidebar Options')
    st.sidebar.header('Choose an option')

    option = st.sidebar.selectbox(
        'Select an option:',
        ('Option 1', 'Option 2', 'Option 3', 'Option 4')
    )

    if option == 'Option 1':
        st.title('Option 1 selected')
        st.write('You selected Option 1.')
        # Menjalankan file coba.py
        try:
            subprocess.run(['python', 'Pages/Menu_5_Chart.py'])
        except Exception as e:
            st.error(f"Error running coba.py: {e}")
    elif option == 'Option 2':
        st.title('Option 2 selected')
        st.write('You selected Option 2.')
        # Menjalankan file coba.py
        try:
            subprocess.run(['python', 'Menu_6_Clustering.py'])
        except Exception as e:
            st.error(f"Error running coba.py: {e}")
    elif option == 'Option 3':
        st.title('Option 3 selected')
        st.write('You selected Option 3.')
        # Menjalankan file coba.py
        try:
            subprocess.run(['python', 'Menu_7_Price.py'])
        except Exception as e:
            st.error(f"Error running coba.py: {e}")
    elif option == 'Option 4':
        st.title('Option 3 selected')
        st.write('You selected Option 3.')
        # Menjalankan file coba.py
        try:
            subprocess.run(['python', 'Menu_8_Review.py'])
        except Exception as e:
            st.error(f"Error running coba.py: {e}")

# Function to execute the external script
def run_external_script():
    subprocess.Popen(["C:/Program Files/Python312/python.exe", "e:/CRUD/Steam_Combine.py"])
    
def refresh_page():
    # Reload the page using Streamlit's rerun API
    st.experimental_rerun()

# Read the CSV file
df = pd.read_csv('games_data.csv')

# Display the CSV data
st.subheader("Data CSV hasil Scrapt")
st.dataframe(df)

# Button to run the external script
if st.button("Update Scrap"):
    run_external_script()
    refresh_page()

if __name__ == '__main__':
    main()
