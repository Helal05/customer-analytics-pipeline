import pandas as pd
import numpy as np
import sys
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def clean_data(df):
    """
    Performs data cleaning tasks as required by [Req 25].
    """
    print("[Preprocess] Cleaning data...")
    
    # Task 1: Handle missing values (drop rows without CustomerID)
    df.dropna(subset=['CustomerID'], inplace=True)
    
    # Task 2: Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Bonus Task: Remove cancelled orders (negative quantity)
    df = df[df['Quantity'] > 0].copy()
    
    return df

def transform_and_engineer(df):
    """
    Performs feature engineering, discretization [Req 28], 
    and transformation.
    """
    print("[Preprocess] Transforming data (Engineering, Binning, Scaling, Encoding)...")
    
    # 1. Feature Engineering: Create TotalPrice for analysis
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    # 2. Discretization : Bin 'TotalPrice'
    try:
        df['Price_Bin'] = pd.qcut(df['TotalPrice'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])
    except ValueError:
        # Fallback if qcut fails (e.g., not enough unique values)
        df['Price_Bin'] = pd.cut(df['TotalPrice'], bins=4, labels=['Low', 'Medium', 'High', 'Very High'])

    # 3. Transformation 
    # Task A: Encode categorical column 'Country'
    df['Country_Code'] = pd.factorize(df['Country'])[0]
    
    # Task B: Scale numeric columns
    numeric_cols = ['Quantity', 'UnitPrice', 'TotalPrice']
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    return df, numeric_cols

def reduce_dimensions(df, numeric_cols):
    """
    Performs dimensionality reduction tasks [Req 27].
    """
    print("[Preprocess] Reducing dimensions (PCA & Selection)...")
    
    # Task 1: Apply PCA on scaled numeric columns
    pca = PCA(n_components=2, random_state=42)
    pca_features = pca.fit_transform(df[numeric_cols])
    df['PCA1'] = pca_features[:, 0]
    df['PCA2'] = pca_features[:, 1]
    
    # Task 2: Select the final subset of columns
    final_columns = [
        'Country', 
        'Price_Bin', 
        'TotalPrice', 
        'Country_Code', 
        'PCA1', 
        'PCA2'
    ]
    df_final = df[final_columns].copy()
    
    return df_final

# --- This is the main part of the script ---
if __name__ == "__main__":
    
    # 1. Get file path from command line 
    if len(sys.argv) != 2:
        print("!Error: Please provide the data file path.")
        print("Example: python preprocess.py data_raw.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "data_preprocessed.csv"

    print(f"[Preprocess] Loading data from {input_file}...")

    # 2. Load the data
    try:
        df = pd.read_csv(input_file, encoding='ISO-8859-1')
    except FileNotFoundError:
        print(f"!Error: File not found: {input_file}")
        sys.exit(1)

    print("[Preprocess] Starting pipeline...")

    # 3. Call the functions in order
    df_cleaned = clean_data(df)
    df_transformed, numeric_cols_list = transform_and_engineer(df_cleaned)
    df_final = reduce_dimensions(df_transformed, numeric_cols_list)

    # 4. Save the final data 
    df_final.to_csv(output_file, index=False)
    print(f"[Preprocess] Saved processed data to {output_file}")

    # 5. Call the next script 
    print(f"[Preprocess] Calling next script: analytics.py...")
    os.system(f"python analytics.py {output_file}")

    print("[Preprocess] Done.")