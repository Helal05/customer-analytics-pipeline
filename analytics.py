import pandas as pd
import sys
import os

def load_data(file_path):
    """
    Loads the preprocessed data file.
    """
    print(f"[Analytics] Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"!Error: File not found: {file_path}")
        sys.exit(1)
    return df

def generate_and_save_insights(df):
    """
    Generates and saves four text insights.
    """
    print("[Analytics] Generating and saving insights...")
    
    try:
        # Insight 1: Top 5 countries by transaction count
        top_5_countries = df['Country'].value_counts().head(5)
        with open("insight1.txt", "w") as f:
            f.write("--- Top 5 Countries by Number of Transactions ---\n")
            f.write(top_5_countries.to_string())

        # Insight 2: Transaction distribution by price category
        price_bin_distribution = df['Price_Bin'].value_counts()
        with open("insight2.txt", "w") as f:
            f.write("--- Transaction Distribution by Price Bin ---\n")
            f.write(price_bin_distribution.to_string())

        # Insight 3: Average (scaled) total price
        average_total_price = df['TotalPrice'].mean()
        with open("insight3.txt", "w") as f:
            f.write("--- Average Scaled TotalPrice ---\n")
            f.write(f"Average Scaled TotalPrice: {average_total_price:.4f}")
            
        # Correlation between the two principal components (PCA1, PCA2)
        # .corr() calculates the Pearson correlation coefficient
        pca_correlation = df['PCA1'].corr(df['PCA2'])
        with open("insight4.txt", "w") as f:
            f.write("--- Correlation between PCA1 and PCA2 ---\n")
            f.write(f"Pearson Correlation: {pca_correlation:.4f}")

    except Exception as e:
        print(f"!Error generating or saving insights: {e}")
        sys.exit(1)

def call_next_script(input_file):
    """
    Calls the next script in the pipeline [Req 48].
    """
    print(f"[Analytics] Calling next script: visualize.py...")
    os.system(f"python visualize.py {input_file}")

# --- This is the main part of the script ---
if __name__ == "__main__":
    
    # 1. Get file path from command line
    if len(sys.argv) != 2:
        print("!Error: Please provide the data file path.")
        print("Example: python analytics.py data_preprocessed.csv")
        sys.exit(1)

    input_file = sys.argv[1]

    # 2. Call the functions in order
    df = load_data(input_file)
    generate_and_save_insights(df)
    call_next_script(input_file) # Pass the filename to the next script

    print("[Analytics] Done.")