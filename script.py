import os
import io
import argparse
from PIL import Image
import fitz
import zipfile
import rarfile
from ebooklib import epub
from task import do_task

def extract_images_from_pdf(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image = Image.open(io.BytesIO(base_image["image"]))
            image.save(os.path.join(output_folder, f'{i}_{xref}.png'))

def extract_images_from_archive(archive_path, output_folder, archive_type):
    if archive_type == 'zip':
        archive = zipfile.ZipFile(archive_path, 'r')
    else:  # rar
        archive = rarfile.RarFile(archive_path, 'r')

    for filename in archive.namelist():
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(archive.open(filename))
            image.save(os.path.join(output_folder, os.path.basename(filename)))

def extract_images_from_epub(epub_path, output_folder):
    book = epub.read_epub(epub_path)
    for item in book.get_items():
        if item.get_type() == epub.EPUB_IMAGE:
            image = Image.open(io.BytesIO(item.get_content()))
            image.save(os.path.join(output_folder, item.file_name))

def process_image(image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    filename = os.path.basename(image_path)
    final_output_image_path = os.path.join(output_folder, 'processed_' + os.path.splitext(filename)[0] + '.png')
    do_task(image_path, final_output_image_path)

def process_all_images(source_folder, output_folder):
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', '.cbz', '.cbr', '.epub')):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                process_image(file_path, output_folder)
            elif filename.lower().endswith('.pdf'):
                extract_images_from_pdf(file_path, output_folder)
            elif filename.lower().endswith('.cbz'):
                extract_images_from_archive(file_path, output_folder, 'zip')
            elif filename.lower().endswith('.cbr'):
                extract_images_from_archive(file_path, output_folder, 'rar')
            elif filename.lower().endswith('.epub'):
                extract_images_from_epub(file_path, output_folder)

def main():
    parser = argparse.ArgumentParser(description='Process an image or all images in a folder.')
    parser.add_argument('--source', required=True, help='Source image file or folder with images.')
    parser.add_argument('--output', help='Optional output folder for processed images. Defaults to the same directory as the source or a subfolder in the source directory.')

    args = parser.parse_args()
    output_folder = args.output or (os.path.join(args.source, 'output') if os.path.isdir(args.source) else os.path.dirname(args.source))

    if os.path.isdir(args.source):
        process_all_images(args.source, output_folder)
    elif os.path.isfile(args.source):
        lower_source = args.source.lower()
        if any(lower_source.endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.pdf', '.cbz', '.cbr', '.epub')):
            process_all_images(os.path.dirname(args.source), output_folder)
        else:
            raise ValueError("The file specified is not a supported image file.")
    else:
        raise ValueError("The specified source is neither a file nor a directory.")

if __name__ == '__main__':
    main()
