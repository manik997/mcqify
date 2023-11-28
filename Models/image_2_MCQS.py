from transformers import pipeline
import pytesseract
from PIL import Image
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
import base64
import requests
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
import os
import re

def check_for_text(image):
    image = Image.open(image)
    text = pytesseract.image_to_string(image)
    return len(text) > 0  


def image_captions(image):
    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    preds = image_to_text(image)
    text = preds[0]['generated_text']
    print(text)
    return text

def ocr(image):
    image = Image.open(image)
    text = pytesseract.image_to_string(image)
    return text




    
# Path to your image
# image_path = "/home/vamsinadh/MS/DL/GenerateMCQs/testfiles/sol.jpeg"
def mcqs_from_image(image_path,num_questions=10):
    prompt = f"""
        You are an expert teacher with comprehensive knowledge of all concepts across various domains. Your task is to create {num_questions} multiple-choice questions (MCQs) based on the provided image or text . Each MCQ should include a question stem, four answer choices (labeled A, B, C, and D), and indicate the correct answer. Ensure that the questions test on key facts, concepts, and important details contained within the text.

            Please generate MCQs for this image:
            Question1: [Question here]
            A) Option A
            B) Option B
            C) Option C
            D) Option D
            Answer: [Correct option here]

            Question2: [Next question here]
            A) Option A
            B) Option B
            C) Option C
            D) Option D
            Answer: [Correct option here]
        [Continue with more questions as needed]
            """
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    # Getting the base64 string
    base64_image = encode_image(image_path)
    api_key = os.environ.get('OPENAI_API_KEY',)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 4000,
        
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    response = response.json()['choices'][0]['message']['content']

    # Split the string into individual questions and answers
    questions = re.split(r'\n\n', response.strip())

    json_data = []
    qnum = 0
    for q in questions:
        # Extract question and options
        parts = re.split(r'\n', q)

        question_label, question_text = parts[0].split(': ')
        options = {opt.split(')')[0]: opt.split(') ')[1] for opt in parts[1:5]}
        answer_label, answer_text = parts[5].split(': ')

        # Extract the answer key (A, B, C, D) from the answer text
        answer_key = answer_text.split(')')[0]

        # Construct the dictionary for each question
        question_dict = {
            question_label: question_text,
            "A": options['A'],
            "B": options['B'],
            "C": options['C'],
            "D": options['D'],
            "Answer": answer_key
        }
        json_data.append(question_dict)
        qnum += 1

    return json_data


def convert_to_dict(response):
    questions = re.split(r'\n\n', response.strip())

    json_data = []
    qnum = 0
    for q in questions:
        # Extract question and options
        parts = re.split(r'\n', q)
        question_label, question_text = parts[0].split(': ')
        options = {opt.split(')')[0]: opt.split(') ')[1] for opt in parts[1:5]}
        answer_label, answer_text = parts[5].split(': ')

        # Extract the answer key (A, B, C, D) from the answer text
        answer_key = answer_text.split(')')[0]

        # Construct the dictionary for each question
        question_dict = {
            question_label: question_text + str(qnum),
            "A": options['A'],
            "B": options['B'],
            "C": options['C'],
            "D": options['D'],
            "Answer": answer_key
        }
        json_data.append(question_dict)
        qnum += 1

    return json_data




# try:
#     image_path = "/home/vamsinadh/MS/DL/GenerateMCQs/testfiles/sol.jpeg"
#     m = mcqs_from_image(image_path)
#     print(m)
#     mcqs = convert_to_dict(m)
#     print(mcqs)


# except Exception as e:
#     print("Error: " + str(e))
