import os
from docx import Document
import pandas as pd

# Specify the folder containing the .docx files
input_folder = '/Users/yaoyujun/Desktop/1/0'
output_folder = '/Users/yaoyujun/Desktop/1/csv_outputs0'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all .docx files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith('.docx'):
        # Construct the full path to the .docx file
        doc_path = os.path.join(input_folder, filename)
        
        # Load the .docx file
        document = Document(doc_path)

        # Initialize lists for columns
        col1, col2, col3 = [], [], []

        # Process the document paragraph by paragraph
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            # Extract x and y from "Testing Positive Image x with Anchor Image y"
            if "Testing Positive Image" in text and "with Anchor Image" in text:
                parts = text.split()
                col1.append("A" + str(parts[3]))  # Positive Image x
                col2.append("B" + str(parts[7]))  # Anchor Image y
            elif "Predicted Euclidean Distance" in text:
                # Extract the digit value following "Predicted Euclidean Distance"
                value = text.split(":")[-1].strip()
                col3.append(value)

        # Ensure all columns have the same length by balancing col3
        if len(col3) < len(col1):
            col3.extend([""] * (len(col1) - len(col3)))

        # Create a DataFrame
        data = {'Positive Image': col1, 'Anchor Image': col2, 'Distance': col3}
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file with the same name as the .docx file
        output_filename = os.path.splitext(filename)[0] + '.csv'
        output_path = os.path.join(output_folder, output_filename)
        df.to_csv(output_path, index=False)

        print(f"Processed: {filename} → {output_filename}")

print(f"All files processed. CSV files are saved in: {output_folder}")
