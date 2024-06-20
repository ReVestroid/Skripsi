# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn_extra.cluster import KMedoids
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt

# st.title("Menu Chart & Hasil")

# # Read the CSV file
# df = pd.read_csv('games_data.csv', usecols=['rank', 'price', 'disc_price', 'persen_disc', 'review_data', 'percent_review', 'total_review'])
# # Map the review_data values to numerical values
# review_mapping = {
#     'No Data': 10,
#     'Overwhelmingly Positive': 1,
#     'Very Positive': 2,
#     'Positive': 3,
#     'Mostly Positive': 4,
#     'Mixed': 5,
#     'Mostly Negative': 6,
#     'Negative': 7,
#     'Very Negative': 8,
#     'Overwhelmingly Negative': 9
# }
# df['review_data'] = df['review_data'].replace(review_mapping)
# # df.to_csv('games_data.csv', index=False)

# # Check for missing values
# missing_values = df.isnull().sum()
# print(missing_values)

# # Fill missing values with mean
# df.fillna(df.mean(), inplace=True)

# # Display the table
# st.write("Table:")
# st.write(df)

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
#     kmedoids = KMedoids(n_clusters=k, random_state=0)
#     kmedoids.fit(numeric_df)
#     distortions.append(kmedoids.inertia_)

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
# # Display clustered data
# st.write("Clustered Data:")
# st.write(df)

# st.subheader("Total Cluster Metode K-Medoids")
# # Create pivot table
# pivot_table = pd.pivot_table(df, index='Cluster', aggfunc='size')

# # Display pivot table
# st.write("Pivot Table:")
# st.write(pivot_table)

# # Display pivot table as bar chart
# st.write("Bar Chart:")
# st.bar_chart(pivot_table)