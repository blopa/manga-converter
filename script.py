import os
import argparse
from task import do_task

def process_image(image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    filename = os.path.basename(image_path)
    final_output_image_path = os.path.join(output_folder, 'processed_' + os.path.splitext(filename)[0] + '.png')
    do_task(image_path, final_output_image_path)

def process_all_images(source_folder, output_folder):
    # List all files in the source directory
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(source_folder, filename)
            process_image(image_path, output_folder)

def main():
    parser = argparse.ArgumentParser(description='Process an image or all images in a folder.')
    parser.add_argument('--source', required=True, help='Source image file or folder with images.')
    parser.add_argument('--output', help='Optional output folder for processed images. Defaults to the same directory as the source or a subfolder in the source directory.')

    args = parser.parse_args()

    # Determine output directory based on input type
    if args.output:
        output_folder = args.output
    else:
        if os.path.isdir(args.source):
            output_folder = os.path.join(args.source, 'output')
        else:
            output_folder = os.path.dirname(args.source)

    # Check if the source is a file or a directory
    if os.path.isdir(args.source):
        process_all_images(args.source, output_folder)
    elif os.path.isfile(args.source):
        if args.source.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image(args.source, output_folder)
        else:
            raise ValueError("The file specified is not a supported image file.")
    else:
        raise ValueError("The specified source is neither a file nor a directory.")

if __name__ == '__main__':
    main()
