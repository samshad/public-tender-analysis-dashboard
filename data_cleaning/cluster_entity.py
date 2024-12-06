import pandas as pd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans, AgglomerativeClustering

from utils.constants import ENTITY_CLUSTER_NAME


# --- Visualization Functions ---
def elbow_test(texts, max_clusters=10):
    """
    Perform the Elbow Test to determine the optimal number of clusters.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    wcss = []
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, random_state=0)
        kmeans.fit(embeddings)
        wcss.append(kmeans.inertia_)
    # Plot the elbow graph
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), wcss, marker='o')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.show()


# --- Clustering Functions ---
def encode_texts(texts):
    """
    Encode the texts using a pre-trained SentenceTransformer model.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(texts)


def cluster_texts_kmeans(texts, num_clusters=10):
    """
    Cluster texts using KMeans.
    """
    embeddings = encode_texts(texts)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(embeddings)
    return kmeans.labels_


def cluster_texts_agglomerative(texts, num_clusters=10):
    """
    Cluster texts using Agglomerative Clustering.
    """
    embeddings = encode_texts(texts)
    agglomerative = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
    return agglomerative.fit_predict(embeddings)


def assign_cluster_names(data, texts, clusters, cluster_names):
    """
    Map entities to cluster names and add them to the DataFrame.
    """
    cluster_mapping = pd.DataFrame({
        'Entity': texts,
        'Cluster': clusters,
        'ClusterName': [cluster_names[cluster] for cluster in clusters]
    })
    # Map ENTITY to their cluster names
    entity_to_cluster_name = dict(zip(cluster_mapping['Entity'], cluster_mapping['ClusterName']))
    data = data.assign(ENTITY_CLUSTER_NAME=data['ENTITY'].map(entity_to_cluster_name))
    return data, cluster_mapping


def display_cluster_groups(cluster_mapping):
    """
    Display entities grouped by clusters.
    """
    print("\nGrouped Entities by Cluster:")
    for cluster_num in sorted(cluster_mapping['Cluster'].unique()):
        print(
            f"Cluster {cluster_num} ({cluster_mapping[cluster_mapping['Cluster'] == cluster_num]['ClusterName'].iloc[0]}):")
        cluster_entities = cluster_mapping[cluster_mapping['Cluster'] == cluster_num]['Entity'].tolist()
        for entity in cluster_entities:
            print(f" - {entity}")
        print("\n")


# --- Main Analysis Function ---
def analyze_entity_clusters(data, num_kmeans_clusters=15, num_agglomerative_clusters=15):
    """
    Perform clustering analysis on ENTITY column in the dataset.
    """
    # Perform Elbow Test
    print("\nPerforming Elbow Test:")
    texts = data['ENTITY'].dropna().unique()
    # Open elbow test for decide cluster size
    elbow_test(texts, max_clusters=20)
    # Perform KMeans clustering
    print("\nKMeans Clustering:")
    kmeans_clusters = cluster_texts_kmeans(texts, num_kmeans_clusters)
    # Perform Agglomerative Clustering
    print("\nAgglomerative Clustering:")
    agg_clusters = cluster_texts_agglomerative(texts, num_agglomerative_clusters)
    # Cluster Names Mapping (Set on constants.py)
    cluster_names = ENTITY_CLUSTER_NAME
    # Map and assign cluster names
    data, cluster_mapping = assign_cluster_names(data, texts, agg_clusters, cluster_names)
    # Display clusters and entities
    print("\nEntity Cluster Mapping:")
    print(cluster_mapping)
    display_cluster_groups(cluster_mapping)
    print("\nUpdated DataFrame:")
    print(data.head())
    return data, cluster_mapping