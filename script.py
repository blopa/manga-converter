import os
import io
import argparse
from PIL import Image
import fitz  # PyMuPDF
import zipfile
import rarfile
from ebooklib import epub
from task import do_task
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')

def extract_images_from_pdf(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image = Image.open(io.BytesIO(base_image["image"]))
            image.save(os.path.join(output_folder, f'{i}_{xref}.png'))

def pack_images_into_archive(processed_files, output_folder, archive_type, archive_name):
    archive_path = os.path.join(output_folder, archive_name)
    if archive_type == 'zip':
        with zipfile.ZipFile(archive_path, 'w') as archive:
            for file_path in processed_files:
                archive.write(file_path, arcname=os.path.basename(file_path))
    elif archive_type == 'rar':
        # RAR file creation might require external tools like rarfile library interfacing with RAR executable
        with rarfile.RarFile(archive_path, 'w') as archive:
            for file_path in processed_files:
                archive.add(file_path, arcname=os.path.basename(file_path))

def extract_images_from_archive(archive_path, output_folder, archive_type):
    processed_files = []

    if archive_type == 'zip':
        archive = zipfile.ZipFile(archive_path, 'r')
    else:
        archive = rarfile.RarFile(archive_path, 'r')

    for filename in archive.namelist():
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            with archive.open(filename) as file:
                image = Image.open(file)
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                final_output_image_path = os.path.join(output_folder, 'processed_' + os.path.splitext(filename)[0] + '.jpg')
                print('Processing page', filename)
                process_image(image, final_output_image_path, output_folder)
                print('Processed:', archive_path)
                processed_files.append(final_output_image_path)

    return processed_files

def extract_images_from_epub(epub_path, output_folder):
    book = epub.read_epub(epub_path)
    for item in book.get_items():
        if item.get_type() == epub.EPUB_IMAGE:
            image = Image.open(io.BytesIO(item.get_content()))
            image.save(os.path.join(output_folder, item.file_name))

def process_image(image, final_output_image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    do_task(image, final_output_image_path)

def process_single_file(file_path, output_folder):
    filename = os.path.basename(file_path)
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        image = Image.open(file_path)
        final_output_image_path = os.path.join(output_folder, 'processed_' + os.path.splitext(filename)[0] + '.png')
        process_image(image, final_output_image_path, output_folder)
    elif file_path.lower().endswith('.pdf'):
        extract_images_from_pdf(file_path, output_folder)
    elif file_path.lower().endswith('.cbz'):
        processed_files = extract_images_from_archive(file_path, output_folder, 'zip')
        pack_images_into_archive(processed_files, output_folder, 'zip', 'processed_' + os.path.splitext(filename)[0] + '.cbz')
    elif file_path.lower().endswith('.cbr'):
        extract_images_from_archive(file_path, output_folder, 'rar')
    elif file_path.lower().endswith('.epub'):
        extract_images_from_epub(file_path, output_folder)
    else:
        raise ValueError("The file specified is not a supported image file.")

def process_all_images(source_folder, output_folder):
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        process_single_file(file_path, output_folder)

def main():
    parser = argparse.ArgumentParser(description='Process an image or all images in a folder.')
    parser.add_argument('--source', required=True, help='Source image file or folder with images.')
    parser.add_argument('--output', help='Optional output folder for processed images. Defaults to the same directory as the source or a subfolder in the source directory.')

    args = parser.parse_args()
    output_folder = args.output or (os.path.join(args.source, 'output') if os.path.isdir(args.source) else os.path.dirname(args.source))

    if os.path.isdir(args.source):
        process_all_images(args.source, output_folder)
    elif os.path.isfile(args.source):
        process_single_file(args.source, output_folder)
    else:
        raise ValueError("The specified source is neither a file nor a directory.")

if __name__ == '__main__':
    main()
