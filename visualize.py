import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """
    Loads the preprocessed data file.
    """
    print(f"[Visualize] Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"!Error: File not found: {file_path}")
        sys.exit(1)
    return df

def create_and_save_plot(df, plot_filename):
    """
    Creates one meaningful scatter plot [Req 35] 
    and saves it [Req 36].
    """
    print(f"[Visualize] Creating scatter plot and saving to {plot_filename}...")
    try:
        # 1. Set the figure size
        plt.figure(figsize=(10, 6))
        
        # 2. Create the scatter plot using seaborn
        sns.scatterplot(
            x='PCA1',      # Put PCA1 on the x-axis
            y='PCA2',      # Put PCA2 on the y-axis
            data=df,       # Use our dataframe
            alpha=0.5      # Make points slightly transparent
        )
        
        # 3. Add titles for clarity
        plt.title("PCA Scatter Plot of Customer Data")
        plt.xlabel("Principal Component 1 (PCA1)")
        plt.ylabel("Principal Component 2 (PCA2)")
        
        # 4. Save the plot to the file
        plt.savefig(plot_filename)
        plt.close() # Close the plot to free up memory
        
    except Exception as e:
        print(f"!Error creating or saving plot: {e}")
        sys.exit(1)

def call_next_script(next_script_name, file_to_pass):
    """
    Calls the final script in the pipeline [Req 48].
    """
    print(f"[Visualize] Calling next script: {next_script_name}...")
    os.system(f'python {next_script_name} {file_to_pass}')

# --- This is the main part of the script ---
if __name__ == "__main__":
    
    # 1. Get file path from command line
    if len(sys.argv) != 2:
        print("!Error: Usage: python visualize.py <input_file_path>")
        sys.exit(1)
    
    # 2. Define filenames
    INPUT_FILE = sys.argv[1]         # "data_preprocessed.csv"
    OUTPUT_FILE = "summary_plot.png" 
    NEXT_SCRIPT = "cluster.py"
    
    # 3. Call the functions in order
    df = load_data(INPUT_FILE)
    create_and_save_plot(df, OUTPUT_FILE)
    
    # Pass the data file (INPUT_FILE), not the plot, to the next step
    call_next_script(NEXT_SCRIPT, INPUT_FILE) 

    print("[Visualize] Done.")