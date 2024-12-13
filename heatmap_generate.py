import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Specify the folder containing the CSV outputs
csv_folder = '/Users/yaoyujun/Desktop/1/csv_outputs0'
output_folder = '/Users/yaoyujun/Desktop/1/heat0'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define colormap range (adjust these as needed)
colormap_min = 0  # Minimum value for the colormap
colormap_max = 6.5  # Maximum value for the colormap

# Loop through all CSV files in the folder
for filename in os.listdir(csv_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_folder, filename)
        
        # Load the CSV file
        data = pd.read_csv(file_path)
        
        # Handle duplicates by averaging the distances
        data = data.groupby(['Positive Image', 'Anchor Image'], as_index=False)['Distance'].mean()
        
        # Pivot the data to create a heatmap matrix
        heatmap_data = data.pivot(index='Positive Image', columns='Anchor Image', values='Distance')

        # Convert distances to numeric
        heatmap_data = heatmap_data.apply(pd.to_numeric, errors='coerce')

        # Sort the labels in ascending order (e.g., A1, A2, ..., An)
        y_labels = sorted(heatmap_data.index, key=lambda x: int(x[1:]))
        x_labels = sorted(heatmap_data.columns, key=lambda x: int(x[1:]))

        # Generate the heatmap
        plt.figure(figsize=(15, 10))  # Adjust the figure size
        sns.heatmap(
            heatmap_data.reindex(index=y_labels, columns=x_labels),  # Align data with sorted labels
            cmap="PuBu_r",  # Reversed color map
            annot=False,  # Disable annotations (numbers in cells)
            cbar=True,  # Show color bar
            vmin=colormap_min,  # Minimum value for the colormap
            vmax=colormap_max,  # Maximum value for the colormap
            cbar_kws={'label': 'Euclidean Distance'}  # Label for the color bar
        )

        # Customize the plot
        plt.title(f"Heatmap for {filename}", fontsize=16)
        plt.xlabel('Anchor Image', fontsize=12)
        plt.ylabel('Positive Image', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Save the heatmap as an image
        output_filename = os.path.splitext(filename)[0] + '_heatmap.png'
        output_path = os.path.join(output_folder, output_filename)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()  # Close the plot to avoid memory issues

        print(f"Heatmap saved for {filename} as {output_filename}")

print(f"All heatmaps are saved in: {output_folder}")
