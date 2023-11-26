from openai import OpenAI

from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from pathlib import Path
import os


def extract_pages_with_complex_content(pdf_path, output_folder, page_start, page_end):
    # Read the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)

        # Loop through each page
        for page_num in range(page_start, page_end):
            page = reader.pages[page_num]
            text = page.extract_text()
            print(text)
            # Check for complex content
            if '[equation]' in text or '[figure]' in text:
                # Convert the page to an image
                images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)

                # Save the image
                for img in images:
                    img_path = os.path.join(output_folder, f'page_{page_num + 1}.png')
                    img.save(img_path, 'PNG')

                    print(f'Saved image of page {page_num + 1} at {img_path}')
    return text


pdf_path = 'probabilitytextbook.pdf'  # Path to your PDF
output_folder = 'images'  # Folder to save images
os.makedirs(output_folder, exist_ok=True)
pdftext = extract_pages_with_complex_content(pdf_path, output_folder, 316, 317)
messageText = """This is an excerpt from Papoulis 'Probability and Random Variables.' Textbook.
                  Imagine you are reading aloud from a textbook. Your task is to describe and explain the 
                  content in a way that is clear and understandable, especially focusing on equations and 
                  complex topics. Assume the reader is listening to this as an audio book and does not have
                  visual access to the content. Speak in the POV that you are the text. Do not reference "The Text" """ \
              + "Please try to structure your response similar to the text. Please do your best. This is very important for my career." \
              + "Here is some extracted text from the textbook [N.B. it may be noisy]: " + pdftext

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text",
                 "text": messageText,
                 },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://i.ibb.co/z8PBrrY/2461299a-4977-4f13-b169-8ea7b86cc893.png",
                    },
                },
            ],
        }
    ],
    max_tokens=4000,
)

print(response.choices[0].message.content)

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=response.choices[0].message.content
)

response.stream_to_file(speech_file_path)
print('done')
