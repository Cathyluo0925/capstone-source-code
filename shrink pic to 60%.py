import os
import csv
from PIL import Image, ImageOps

def resize_and_adjust_image(input_path, output_path, scale):
    try:
        # Open the image
        original_image = Image.open(input_path)
        
        # Get original dimensions
        original_width, original_height = original_image.size

        # Calculate new dimensions
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # Resize the image
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        if new_width < original_width or new_height < original_height:
            # If the resized image is smaller, pad with black bars
            new_image = Image.new("RGB", (original_width, original_height), (0, 0, 0))
            x_offset = (original_width - new_width) // 2
            y_offset = (original_height - new_height) // 2
            new_image.paste(resized_image, (x_offset, y_offset))
        else:
            # If the resized image is larger, crop the center
            left = (new_width - original_width) // 2
            top = (new_height - original_height) // 2
            right = left + original_width
            bottom = top + original_height
            new_image = resized_image.crop((left, top, right, bottom))

        # Save the resulting image
        new_image.save(output_path)
        print(f"Processed and saved: {output_path}")

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_csv_and_images(csv_path, image_directory, output_directory_base, scale=1.0, suffix=""):
    # Make a unique output directory for the current scale and suffix
    output_directory = os.path.join(output_directory_base, f"scaled_{suffix}")
    os.makedirs(output_directory, exist_ok=True)

    # Read the CSV file
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for filename in row:
                # Add the .jpg extension to the filename
                filename_with_extension = f"{filename}.jpg"

                # Define input and output file paths
                input_path = os.path.join(image_directory, filename_with_extension)

                # Add the suffix to the output filename
                filename_with_suffix = f"{filename}{suffix}.jpg"
                output_path = os.path.join(output_directory, filename_with_suffix)

                # Check if the input file exists
                if os.path.exists(input_path):
                    resize_and_adjust_image(input_path, output_path, scale)
                else:
                    print(f"File not found: {input_path}")

# Example usage
csv_file_path = "/Users/yaoyujun/Downloads/augmentation_list.csv"  # Replace with your CSV file path
image_folder_path = "/Users/yaoyujun/Desktop/frames/frames_original"  # Replace with the folder containing the original images
output_folder_base = "/Users/yaoyujun/Desktop/frames"  # Base directory for output folders

# Enlarge and shrink images with different scales
process_csv_and_images(csv_file_path, image_folder_path, output_folder_base, scale=1.1, suffix="_110%")
#process_csv_and_images(csv_file_path, image_folder_path, output_folder_base, scale=1.3, suffix="_130%")
#process_csv_and_images(csv_file_path, image_folder_path, output_folder_base, scale=0.9, suffix="_90%")
process_csv_and_images(csv_file_path, image_folder_path, output_folder_base, scale=0.8, suffix="_80%")
#process_csv_and_images(csv_file_path, image_folder_path, output_folder_base, scale=0.7, suffix="_70%")
process_csv_and_images(csv_file_path, image_folder_path, output_folder_base, scale=0.6, suffix="_60%")
