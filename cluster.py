import pandas as pd
import sys
import os
from sklearn.cluster import KMeans

def load_data(file_path):
    """
    Loads the preprocessed data file.
    """
    print(f"[Cluster] Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"!Error: File not found: {file_path}")
        sys.exit(1)
    return df

def apply_kmeans_and_save(df, features_list, num_clusters, output_filename):
    """
    Applies K-Means clustering and saves the
    sample counts per cluster.
    """
    print(f"[Cluster] Applying K-Means (k={num_clusters}) on {features_list}...")
    
    # 1. Select the features for clustering
    df_cluster = df[features_list]
    
    # 2. Initialize and run K-Means
    # n_clusters=4 -> We want to find 4 groups
    # random_state=42 -> Ensures we get the same result every time (reproducible)
    # n_init='auto' -> Suppresses a future warning
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
    kmeans.fit(df_cluster)
    
    # 3. Get the cluster label for each row (e.g., 0, 1, 2, or 3)
    df['Cluster_Label'] = kmeans.labels_
    
    # 4. Count the number of samples (rows) in each cluster
    cluster_counts = df['Cluster_Label'].value_counts().sort_index()
    
    # 5. Save the result to the output file
    print(f"[Cluster] Saving cluster counts to {output_filename}...")
    try:
        with open(output_filename, "w") as f:
            f.write(f"--- K-Means Cluster Sample Counts (k={num_clusters}) ---\n")
            f.write(cluster_counts.to_string())
    except Exception as e:
        print(f"!Error saving cluster results: {e}")
        sys.exit(1)


# --- This is the main part of the script ---
if __name__ == "__main__":
    
    # 1. Get file path from command line
    if len(sys.argv) != 2:
        print("!Error: Usage: python cluster.py <input_file_path>")
        sys.exit(1)
    
    # 2. Define parameters
    INPUT_FILE = sys.argv[1]         # "data_preprocessed.csv"
    OUTPUT_FILE = "clusters.txt"
    K_VALUE = 4                      # We choose to find 4 clusters
    CLUSTERING_FEATURES = ['PCA1', 'PCA2'] 
    
    # 3. Call the functions in order
    df = load_data(INPUT_FILE)
    apply_kmeans_and_save(df, CLUSTERING_FEATURES, K_VALUE, OUTPUT_FILE)

    print("[Cluster] Done. (Pipeline end)")