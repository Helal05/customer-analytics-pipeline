#!/bin/bash
# This is a shell script to summarize the pipeline results.

# --- 1. Define Variables ---
# !!IMPORTANT!!: We must use this name when we run our container.
CONTAINER_NAME="big_data_pipeline"
# The local directory to save results to [Req 41, 63]
RESULTS_DIR="results"

# --- 2. Create results directory on host ---README
mkdir -p $RESULTS_DIR
echo "[Summary] Created local directory: $RESULTS_DIR"
README
# --- 3. Copy files from container to host [Req 41] ---
echo "[Summary] Copying files from container '$CONTAINER_NAME'..."

# Copy CSV files
docker cp "$CONTAINER_NAME":/app/pipeline/data_raw.csv "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/data_preprocessed.csv "$RESULTS_DIR/"

# Copy TXT files
docker cp "$CONTAINER_NAME":/app/pipeline/insight1.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/insight2.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/insight3.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/insight4.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/clusters.txt "$RESULTS_DIR/"

# Copy PNG file
docker cp "$CONTAINER_NAME":/app/pipeline/summary_plot.png "$RESULTS_DIR/"

echo "[Summary] All results copied to $RESULTS_DIR."

# --- 4. Stop and remove the container [Req 42] ---
echo "[Summary] Stopping container: $CONTAINER_NAME..."
docker stop "$CONTAINER_NAME"

echo "[Summary] Removing container: $CONTAINER_NAME..."
docker rm "$CONTAINER_NAME"

echo "[Summary] Cleanup complete."