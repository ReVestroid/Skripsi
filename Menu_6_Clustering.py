import streamlit as st
import pandas as pd
import numpy as np
from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Determine clusters using initial medoid centroids
def determine_clusters(data, centroids):
    distances = pairwise_distances(data, centroids)
    return np.argmin(distances, axis=1)

st.title("Menu K-Medoids")

# Read the CSV file
df = pd.read_csv('games_data.csv', usecols=['rank', 'price', 'disc_price', 'persen_disc', 'review_data', 'percent_review', 'total_review'])
df1 = pd.read_csv('games_data.csv', usecols=['rank', 'price', 'disc_price', 'persen_disc'])
df2 = pd.read_csv('games_data.csv', usecols=['rank', 'review_data', 'percent_review', 'total_review'])
# Map the review_data values to numerical values
review_mapping = {
    'No Data': 10,
    'Overwhelmingly Positive': 1,
    'Very Positive': 2,
    'Positive': 3,
    'Mostly Positive': 4,
    'Mixed': 5,
    'Mostly Negative': 6,
    'Negative': 7,
    'Very Negative': 8,
    'Overwhelmingly Negative': 9
}
df['review_data'] = df['review_data'].replace(review_mapping)
df2['review_data'] = df2['review_data'].replace(review_mapping)
df.to_csv('games_data2.csv', index=False)
df1.to_csv('games_data_price.csv', index=False)
df2.to_csv('games_data_review.csv', index=False)

# Check for missing values
# missing_values = df.isnull().sum()
# print(missing_values)

# # Fill missing values with mean
# df.fillna(df.mean(), inplace=True)

# Display the table
st.write("Table:")
st.write(df)

st.write("Summary Statistics:")
st.write(df.describe())

# Drop non-numeric columns if any
numeric_df = df.drop(columns=['review_data'])

# Fill missing values with mean
numeric_df.fillna(numeric_df.mean(), inplace=True)

# X, _ = numeric_df(n_samples=n_samples, centers=4, n_features=n_features, random_state=random_state)

# Calculate distortion for different values of k
distortions = []
max_k = 10
for k in range(1, max_k + 1):
    kmedoids = KMedoids(n_clusters=k, random_state=0)
    kmedoids.fit(numeric_df)
    distortions.append(kmedoids.inertia_)

# Plotting the elbow plot
st.write("Elbow Plot:")
plt.plot(range(1, max_k + 1), distortions, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Distortion')
plt.title('Elbow Plot')
st.pyplot(plt)

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_df)

# Sidebar
st.title("K-Medoids Clustering")
k = st.slider("Number of Clusters (k)", 2, 10, 2)

# K-Medoids clustering
kmedoids = KMedoids(n_clusters=k, random_state=0)
clusters = kmedoids.fit_predict(X_scaled)

# Add cluster labels to DataFrame
df['Cluster'] = clusters

# # K-Medoids clustering
# kmedoids = KMedoids(n_clusters=k, random_state=0)

# Visualization of clustering process
for i in range(1, k + 1):
    st.write(f"Iteration {i}")
    kmedoids.n_clusters = i
    kmedoids.fit(X_scaled)
    clusters = kmedoids.predict(X_scaled)

    # Calculate distances to medoids
    distances = pairwise_distances(X_scaled, kmedoids.cluster_centers_)

    # Display distances to medoids
    # st.write('Distances to Medoids:')
    # st.write(distances)
    
    # Get indices of medoids
    medoid_indices = kmedoids.medoid_indices_ + 1
    
    # Determine new centroids
    new_centroids = []
    for j, medoid_index in enumerate(medoid_indices):
        cluster_points = X_scaled[clusters == j]
        distances_to_medoid = distances[medoid_index]
        new_centroid_index = np.argmin(distances_to_medoid)
        new_centroid = cluster_points[new_centroid_index]
        new_centroids.append(new_centroid)
    new_centroids_df = pd.DataFrame(new_centroids, columns=numeric_df.columns)

    # Display centroids from # Get indices of medoids
    st.write('Centroids awal medoids:')
    st.write(scaler.inverse_transform(new_centroids_df))
    cluster_centers = scaler.inverse_transform(kmedoids.cluster_centers_)
    
    

    # Determine clusters using initial medoid centroids
    initial_medoid_indices = kmedoids.medoid_indices_
    initial_medoid_centroids = X_scaled[initial_medoid_indices]
    initial_clusters = determine_clusters(X_scaled, initial_medoid_centroids)

    # Visualize clusters using initial medoid centroids
    plt.figure(figsize=(8, 6))
    for cluster_label in range(i):
        plt.scatter(X_scaled[initial_clusters == cluster_label, 0], X_scaled[initial_clusters == cluster_label, 1], label=f'Cluster {cluster_label + 1}')
    plt.scatter(initial_medoid_centroids[:, 0], initial_medoid_centroids[:, 1], marker='o', s=200, c='red', label='Centroids Final Medoids')
    plt.scatter(new_centroids_df.iloc[:, 0], new_centroids_df.iloc[:, 1], marker='o', s=200, c='Green', label='Centroids Awal Medoids')
    plt.xlabel('Feature 1 (Standardized)')
    plt.ylabel('Feature 2 (Standardized)')
    plt.legend()
    st.pyplot(plt)
    
    # Visualize cluster centers
    st.write("Cluster Centers:")
    st.write(pd.DataFrame(cluster_centers, columns=numeric_df.columns))

# Display final clustering results
st.header("Final Clustering Results")
# Fit K-Medoids with the final number of clusters
kmedoids.n_clusters = k
kmedoids.fit(X_scaled)
clusters = kmedoids.predict(X_scaled)

# Add cluster labels to the DataFrame
df['Cluster'] = clusters

# Display final clustered data
st.write("Final Clustered Data:")
st.write(df)

silhouette_avg = silhouette_score(X_scaled, clusters)

st.subheader(f'Silhouette Score: {silhouette_avg}')

# Visualize final clusters
plt.figure(figsize=(8, 6))
for cluster_label in range(k):
    plt.scatter(X_scaled[clusters == cluster_label, 0], X_scaled[clusters == cluster_label, 1], label=f'Cluster {cluster_label+1}')
plt.xlabel('Feature 1 (Standardized)')
plt.ylabel('Feature 2 (Standardized)')
plt.legend()
st.pyplot(plt)

# Display final cluster centers
st.write("Final Cluster Centers:")
final_cluster_centers = scaler.inverse_transform(kmedoids.cluster_centers_)
st.write(pd.DataFrame(final_cluster_centers, columns=numeric_df.columns))


# Display clustered data per cluster
st.header("Clustered Data per Cluster:")
for cluster_label in range(k):
    st.subheader(f"Cluster {cluster_label + 1}:")
    st.write("Table:")
    cluster_data = df[df['Cluster'] == cluster_label]
    st.write(cluster_data)
    # Summary statistics for each cluster
    st.write("Summary Statistics:")
    st.write(cluster_data.describe())

st.subheader("Total Cluster Metode K-Medoids")
# Create pivot table
pivot_table = pd.pivot_table(df, index='Cluster', aggfunc='size')

# Display pivot table
st.write("Pivot Table:")
st.write(pivot_table)

# Display pivot table as bar chart
st.write("Bar Chart:")
st.bar_chart(pivot_table)
