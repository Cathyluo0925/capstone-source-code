import os
from PIL import Image

# Define the directory containing the images and the output directory
input_directory = '/Users/yaoyujun/Documents/frames/app/Nov27_1_frames/test5a'  # Replace with your images folder path
output_directory = '/Users/yaoyujun/Documents/frames/app/Nov27_1_frames/test5a_outcome_integrate'  # Replace with your output folder path
os.makedirs(output_directory, exist_ok=True)

# Get a sorted list of all images in the input directory
image_files = sorted([f for f in os.listdir(input_directory) if f.endswith('.jpg')])
image_files = [str(f) + ".jpg" for f in range(1, 142)] # change this to the total number of frames + 1
print (image_files)

# Function to combine images into a 2x2 grid
def combine_images(image_paths):
    images = [Image.open(path) for path in image_paths]
    
    # Check that we have exactly 4 images
    if len(images) != 4:
        print(f"Expected 4 images, but got {len(images)}.")
        return None

    # Assuming all images are the same size
    width, height = images[0].size
    new_image = Image.new('RGB', (width * 2, height * 2))

    # Paste images into the 2x2 grid
    new_image.paste(images[0], (0, 0))  # Top-left
    new_image.paste(images[1], (width, 0))  # Top-right
    new_image.paste(images[2], (0, height))  # Bottom-left
    new_image.paste(images[3], (width, height))  # Bottom-right

    return new_image

# Loop through images with a sliding window of 4 images
for i in range(0, len(image_files)//4):
    # Get the file paths for the current 4 images
    image_paths = [os.path.join(input_directory, image_files[i * 4 + j]) for j in range(0,4)]
    print(image_paths)

    # Combine the images into one 2x2 grid
    combined_image = combine_images(image_paths)
    
    if combined_image:
        # Save the combined image in the output directory
        combined_image.save(os.path.join(output_directory, f"combined_{i + 1}.jpg"))

print("All images have been combined and saved successfully.")
