import easyocr
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import torch

def extract_text_from_manga(base_image, lang='en'):
    reader = easyocr.Reader([lang], gpu=torch.cuda.is_available())
    try:
        if isinstance(base_image, Image.Image):
            base_image = np.array(base_image)
        results = reader.readtext(base_image, detail=1)
    except Exception as e:
        print(f"Failed to process image with EasyOCR: {e}")
        results = []
    
    extracted_data = []
    for result in results:
        data = {
            "text": result[1],
            "location": [int(point) for point in result[0][0]],
            "width": int(result[0][2][0] - result[0][0][0]),
            "height": int(result[0][2][1] - result[0][0][1])
        }
        extracted_data.append(data)
    return json.dumps(extracted_data, ensure_ascii=False)

def create_image_with_text(base_image_path, data):
    base_image = Image.open(base_image_path)
    width, height = base_image.size
    new_image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(new_image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
#     font_path = "GenEiKoburiMin6-R.ttf"

    for item in json.loads(data):
        text = item['text']
        x, y = item['location']
        box_width, box_height = item['width'], item['height']

        # Check if dimensions are valid
        if box_width <= 0 or box_height <= 0:
            continue  # Skip this entry

        fontsize = 1  # Start with the smallest possible font size
        font = ImageFont.truetype(font_path, fontsize)
        text_width, text_height = font.getbbox(text, anchor='lt')[2:4]

        # Increase font size until it no longer fits
        while text_width < box_width and text_height < box_height and fontsize < 100:  # added a reasonable limit to fontsize
            fontsize += 1
            font = ImageFont.truetype(font_path, fontsize)
            text_width, text_height = font.getbbox(text, anchor='lt')[2:4]

        # Ensure fontsize is greater than zero
        if fontsize > 1:
            fontsize -= 1  # Decrement to fit within the box
            font = ImageFont.truetype(font_path, fontsize)
            draw.text((x, y), text, font=font, fill=(0, 0, 0))

    new_image.save('output_image.png')
    new_image.show()

def create_image_with_inverted_text_placement(base_image, data):
    width, height = base_image.size
    new_image = Image.new('RGBA', (width, height), (255, 255, 255, 0))

    data = json.loads(data)
    for index, item in enumerate(data):
        x, y = item['location']
        box_width, box_height = item['width'], item['height']
        if box_width <= 0 or box_height <= 0:
            continue

        new_x = width - x - box_width
        cropped_image = base_image.crop((x, y, x + box_width, y + box_height))
        cropped_image = cropped_image.convert('RGBA')
        new_image.paste(cropped_image, (new_x, y), cropped_image)

    return new_image

def overlay_flipped_with_transparent(base_image, transparent_image, final_output_image_path='final_output_image.png'):
    flipped_base_image = base_image.transpose(Image.FLIP_LEFT_RIGHT).convert('RGBA')

    if transparent_image.mode != 'RGBA':
        transparent_image = transparent_image.convert('RGBA')

    combined_image = Image.alpha_composite(flipped_base_image, transparent_image)

    if final_output_image_path.lower().endswith('.jpg') or final_output_image_path.lower().endswith('.jpeg'):
        combined_image = combined_image.convert('RGB')

    combined_image.save(final_output_image_path)

def do_task(base_image, final_output_image_path, lang='en'):
    if isinstance(base_image, str):
        base_image = Image.open(base_image)
    extracted_text = extract_text_from_manga(base_image, lang)
    base_image = Image.open(base_image) if isinstance(base_image, str) else base_image
    transparent_image = create_image_with_inverted_text_placement(base_image, extracted_text)
    overlay_flipped_with_transparent(base_image, transparent_image, final_output_image_path)
