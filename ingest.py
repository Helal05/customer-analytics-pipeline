import pandas as pd
import sys
import os

def load_and_save_raw_data(file_path, output_filename):
    """
    Loads data from the file_path [Req 21] and saves a copy 
    as output_filename.
    """
    print(f"[Ingest] Loading data from {file_path}...")
    
    # 1. Load the data
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except FileNotFoundError:
        print(f"!Error: Input file not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while loading: {e}")
        sys.exit(1)

    # 2. Save a raw copy
    try:
        df.to_csv(output_filename, index=False)
        print(f"[Ingest] Raw data saved successfully to: {output_filename}")
    except Exception as e:
        print(f"An error occurred while saving: {e}")
        sys.exit(1)

def call_next_script(next_script_name, file_to_pass):
    """
    Calls the next script in the pipeline.
    """
    print(f"[Ingest] Triggering next step: {next_script_name}...")
    os.system(f'python {next_script_name} {file_to_pass}')

# --- This is the main part of the script ---
if __name__ == "__main__":
    
    # 1. Check for command-line argument
    if len(sys.argv) != 2:
        print("!Error: Usage: python ingest.py <input_file_path>")
        sys.exit(1)
    
    # 2. Define filenames
    INPUT_FILE = sys.argv[1]         # e.g., "data.csv"
    OUTPUT_FILE = "data_raw.csv"     # As required by 
    NEXT_SCRIPT = "preprocess.py"
    
    # 3. Call the functions in order
    load_and_save_raw_data(INPUT_FILE, OUTPUT_FILE)
    call_next_script(NEXT_SCRIPT, OUTPUT_FILE)

    print("[Ingest] Done.")