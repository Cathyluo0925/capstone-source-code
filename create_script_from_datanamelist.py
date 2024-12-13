import random
import pandas as pd

# Load the uploaded CSV file
file_path = '/Users/yaoyujun/Downloads/augmentation_list_new.csv'
data = pd.read_csv(file_path)

# Function to randomly select one cell from a row
def random_cell(row):
    return row.sample(n=1).iloc[0]

# Initialize the resulting dataframe
result_data = {
    "Anchor": [],
    "Positive": [],
    "Negative": []
}

# Generate 10 such triplets as an example
for _ in range(20000):
    # Randomly select 4 rows from the dataset
    selected_rows = data.sample(n=4, random_state=random.randint(0, 1000))
    
    # Anchor: Randomly select one cell from each of the 4 rows
    anchor_files = [random_cell(row) for _, row in selected_rows.iterrows()]
    
    # Positive: Randomly select one cell from the same 4 rows again
    positive_files = [random_cell(row) for _, row in selected_rows.iterrows()]
    
    # Negative: Randomly select 4 rows from the entire dataset and one cell each
    negative_files = [random_cell(row) for _, row in data.sample(n=4, random_state=random.randint(0, 1000)).iterrows()]
    
    # Append to the result data
    result_data["Anchor"].append(anchor_files)
    result_data["Positive"].append(positive_files)
    result_data["Negative"].append(negative_files)

# Convert result data into a DataFrame
result_df = pd.DataFrame(result_data)

# Save the resulting DataFrame to a new CSV file
result_csv_path = "/Users/yaoyujun/Downloads/script_new.csv"
result_df.to_csv(result_csv_path, index=False)

