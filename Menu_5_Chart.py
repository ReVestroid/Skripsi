import streamlit as st
import pandas as pd
import numpy as np
from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


st.title("Menu Chart Tiap Data")
df = pd.read_csv('games_data.csv', dtype={'rank': int,'price': int, 'disc_price': int, 'persen_disc': int, 'review_data': str, 'percent_review': float, 'total_review': float})
st.write("Table Awal:")
st.dataframe(df)

st.header("Chart Harga Awal")
pivot_table_price = df.pivot_table(index='price', values='title', aggfunc='count', fill_value=0)
# Display the pivot table
st.write("Table:")
st.dataframe(pivot_table_price)
# Plot the pivot table
st.write("Chart:")
st.bar_chart(pivot_table_price)

st.header("Chart Harga Final")
pivot_table_dprice = df.pivot_table(index='disc_price', values='title', aggfunc='count', fill_value=0)
# Display the pivot table
st.write("Table:")
st.dataframe(pivot_table_dprice)
# Plot the pivot table
st.write("Chart:")
st.bar_chart(pivot_table_dprice)

st.header("Chart Diskon")
pivot_table_disc = df.pivot_table(index='persen_disc', values='title', aggfunc='count', fill_value=0)
# Display the pivot table
st.write("Table:")
st.dataframe(pivot_table_disc)
# Plot the pivot table
st.write("Chart:")
st.bar_chart(pivot_table_disc)

st.header("Chart Review")
pivot_table_review = df.pivot_table(index='review_data', values='title', aggfunc='count', fill_value=0)
# Display the pivot table
st.write("Table:")
st.dataframe(pivot_table_review)
# Plot the pivot table
st.write("Chart:")
st.bar_chart(pivot_table_review)

st.header("Chart Percent Positive Review")
pivot_table_perpos = df.pivot_table(index='percent_review', values='title', aggfunc='count', fill_value=0)
# Display the pivot table
st.write("Table:")
st.dataframe(pivot_table_perpos)
# Plot the pivot table
st.write("Chart:")
st.bar_chart(pivot_table_perpos)

st.header("Chart Total Review")
# Create bins for the 'Price' column
bins = [0, 1000, 10000, 50000, 250000, 1000000, df['total_review'].max()]
labels = ['0-1.000', '1.001-10.000', '10.001-50.001', '50.001-250.000', '250.001-1.000.000', '1.000.001+']
df['Range'] = pd.cut(df['total_review'], bins=bins, labels=labels, right=False)

# Pivot table to summarize the counts for each price range
pivot_table_treview = df.pivot_table(index='Range', aggfunc='size', fill_value=0)
pivot_table_treview = pivot_table_treview.reset_index(name='Count')

# Pivot table to summarize the counts for each total review range
pivot_table_treview = df.pivot_table(index='Range', aggfunc='size', fill_value=0)
pivot_table_treview = pivot_table_treview.reset_index(name='Count')
# Display the pivot table
st.write("Table:")
st.dataframe(pivot_table_treview)
# Plotting the pivot table
st.write("Chart:")
st.bar_chart(pivot_table_treview.set_index('Range'))



# # Read the CSV file
# df = pd.read_csv('games_data.csv', usecols=['rank', 'price', 'disc_price', 'persen_disc', 'review_data', 'percent_review', 'total_review'])
# st.write("Summary Statistics:")
# st.write(df.describe())

# # Drop non-numeric columns if any
# numeric_df = df.drop(columns=['review_data'])

# # Fill missing values with mean
# numeric_df.fillna(numeric_df.mean(), inplace=True)

# # Calculate distortion for different values of k
# distortions = []
# max_k = 10
# for k in range(1, max_k + 1):
#     kmeans = KMedoids(n_clusters=k, random_state=0)
#     kmeans.fit(numeric_df)
#     distortions.append(kmeans.inertia_)

# # Plotting the elbow plot
# st.write("Elbow Plot:")
# plt.plot(range(1, max_k + 1), distortions, marker='o')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Distortion')
# plt.title('Elbow Plot')
# st.pyplot(plt)

# # Standardize the features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(numeric_df)

# # Sidebar
# st.sidebar.title("K-Medoids Clustering")
# k = st.sidebar.slider("Number of Clusters (k)", 2, 10, 2)

# # K-Medoids clustering
# kmedoids = KMedoids(n_clusters=k, random_state=0)
# clusters = kmedoids.fit_predict(X_scaled)

# # Add cluster labels to DataFrame
# df['Cluster'] = clusters

# # Display cluster centers
# st.write("Cluster Centers:")
# cluster_centers = scaler.inverse_transform(kmedoids.cluster_centers_)
# st.write(pd.DataFrame(cluster_centers, columns=numeric_df.columns))

# # Display scatter plot
# st.write("Scatter Plot:")
# plt.figure(figsize=(8, 6))
# for i in range(k):
#     plt.scatter(X_scaled[clusters == i, 0], X_scaled[clusters == i, 1], label=f'Cluster {i+1}')
# plt.xlabel('Feature 1 (Standardized)')
# plt.ylabel('Feature 2 (Standardized)')
# plt.legend()
# st.pyplot(plt)

# st.subheader("Hasil Data Cluster Metode K-Medoids")
# # center
# cluster_centers_df = pd.DataFrame(cluster_centers, columns=numeric_df.columns)
# # st.write(cluster_centers_df)

# # Display clustered data
# st.write("Clustered Data:")
# st.write(df)


# # hsl = pd.read_csv(r'E:\CRUD\Hasil_Cluster.csv')
# # st.dataframe(hsl)

# st.subheader("Total Cluster Metode K-Medoids")
# # Create pivot table
# pivot_table = pd.pivot_table(df, index='Cluster', aggfunc='size')

# # Display pivot table
# st.write("Pivot Table:")
# st.write(pivot_table)

# # Display pivot table as bar chart
# st.write("Bar Chart:")
# st.bar_chart(pivot_table)