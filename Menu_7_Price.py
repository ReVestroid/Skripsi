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
df = pd.read_csv('games_data.csv', usecols=['rank', 'price', 'disc_price', 'persen_disc'])

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Display the table
st.write("Table:")
st.write(df)

st.write("Summary Statistics:")
st.write(df.describe())

# Calculate distortion for different values of k
distortions = []
max_k = 10
for k in range(1, max_k + 1):
    kmedoids = KMedoids(n_clusters=k, random_state=0)
    kmedoids.fit(X_scaled)
    distortions.append(kmedoids.inertia_)

# Plotting the elbow plot
st.write("Elbow Plot:")
plt.plot(range(1, max_k + 1), distortions, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Distortion')
plt.title('Elbow Plot')
st.pyplot(plt)

# Sidebar
st.title("K-Medoids Clustering")
k = st.slider("Number of Clusters (k)", 2, 10, 2)

# K-Medoids clustering
kmedoids = KMedoids(n_clusters=k, random_state=0)
clusters = kmedoids.fit_predict(X_scaled)

# Add cluster labels to DataFrame
df['Cluster'] = clusters

# Visualization of clustering process
for i in range(1, k + 1):
    st.write(f"Iteration {i}")
    kmedoids.n_clusters = i
    kmedoids.fit(X_scaled)
    clusters = kmedoids.predict(X_scaled)

    # Get indices of medoids
    medoid_indices = kmedoids.medoid_indices_
    
    # Determine new centroids
    new_centroids = []
    for j, medoid_index in enumerate(medoid_indices):
        cluster_points = X_scaled[clusters == j]
        distances_to_medoid = pairwise_distances(cluster_points, [X_scaled[medoid_index]])
        new_centroid_index = np.argmin(distances_to_medoid)
        new_centroid = cluster_points[new_centroid_index]
        new_centroids.append(new_centroid)

    # Convert new centroids to a DataFrame
    new_centroids_df = pd.DataFrame(new_centroids, columns=df.columns[:-1]) # Exclude 'Cluster' column
    print("Shape of new_centroids_df:", new_centroids_df.shape)
    print("Columns of new_centroids_df:", new_centroids_df.columns)
    print(new_centroids_df)
    print("Shape of df:", df.shape)
    print("Columns of df:",df.columns)
    print(df)
    
    # Display centroids
    st.write(f'Centroids for {i} clusters:')
    st.write(scaler.inverse_transform(new_centroids_df))

# Display final clustering results
st.header("Final Clustering Results")

# Add cluster labels to the DataFrame
df['Cluster'] = clusters

# Display final clustered data
st.write("Final Clustered Data:")
st.write(df)

# Calculate silhouette score
silhouette_avg = silhouette_score(X_scaled, clusters)
st.subheader(f'Silhouette Score: {silhouette_avg}')

# Calculate final cluster centers
final_cluster_centers = scaler.inverse_transform(kmedoids.cluster_centers_)

# Print the shape of final_cluster_centers
print("Shape of final_cluster_centers:", final_cluster_centers.shape)

# Create DataFrame from final cluster centers
st.write("Final Cluster Centers:")
final_cluster_centers_df = pd.DataFrame(final_cluster_centers, columns=df.columns[:-1])
st.write(final_cluster_centers_df)

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

st.subheader("Total Cluster Method K-Medoids")
# Create pivot table
pivot_table = pd.pivot_table(df, index='Cluster', aggfunc='size')

# Display pivot table
st.write("Pivot Table:")
st.write(pivot_table)

# Display pivot table as bar chart
st.write("Bar Chart:")
st.bar_chart(pivot_table)