import os
from task import do_task

def process_all_images(source_folder, output_folder):
    # Check if output folder exists, create if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the source directory
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(source_folder, filename)
            final_output_image_path = os.path.join(output_folder, 'processed_' + filename + '.png')
            do_task(image_path, final_output_image_path)

# Usage example
source_folder = 'test'
output_folder = 'output'
process_all_images(source_folder, output_folder)
