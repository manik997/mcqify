import openai
import re
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from openai import OpenAI
import json
def mcqs_from_text(text, num_questions = 10):
    client = OpenAI()

    prompt = f"""
        You are an expert teacher with comprehensive knowledge of all concepts across various domains. Your task is to create {num_questions} multiple-choice questions (MCQs) based on the provided text. Each MCQ should include a question stem, four answer choices (labeled A, B, C, and D), and indicate the correct answer. Ensure that the questions test on key facts, concepts, and important details contained within the text.

            Text:

            Please generate MCQs for this text:
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
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    response_format={ "type": "text" },
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ],
    max_tokens=4000
    )
    
    response = response.choices[0].message.content

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

# text = """
# The United States of America (USA), commonly known as the United States (U.S.) or simply America, is a country primarily located in North America and consisting of 50 states, a federal district, five major unincorporated territories, and nine Minor Outlying Islands.[i] It includes 326 Indian reservations. It is the world's third-largest country by both land and total area.[c] It shares land borders with Canada to its north and with Mexico to its south and has maritime borders with the Bahamas, Cuba, Russia, and other nations.[j] With a population of over 333 million,[k] it is the most populous country in the Americas and the third-most populous in the world. The national capital of the United States is Washington, D.C., and its most populous city and principal financial center is New York City.

# Indigenous peoples have inhabited the Americas for thousands of years. Beginning in 1607, British colonization led to the establishment of the Thirteen Colonies in what is now the Eastern United States. They clashed with the British Crown over taxation and political representation, which led to the American Revolution and the ensuing Revolutionary War. The United States declared independence on July 4, 1776, becoming the first nation-state founded on Enlightenment principles of unalienable natural rights, consent of the governed, and liberal democracy. The country began expanding across North America, spanning the continent by 1848. Sectional division over slavery (primarily of Africans) led to the secession of the Confederate States of America, which fought the remaining states of the Union during the American Civil War (1861–1865). With the Union's victory and preservation, slavery was abolished nationally. However, racial discrimination and inequality continued into subsequent centuries. By 1900, the United States had established itself as a great power, becoming the world's largest economy. After Japan's attack on Pearl Harbor in 1941, the U.S. entered World War II on the side of the Allies. The aftermath of the war left the United States and the Soviet Union as the world's two superpowers and led to the Cold War, during which both countries engaged in a struggle for ideological dominance and international influence but avoided direct military conflict. During the Space Race, the United States landed the first humans on the Moon, notably with the Apollo 11 mission in 1969. Following the Soviet Union's collapse and the end of the Cold War, the United States emerged as the world's sole superpower.

# The United States government is a federal presidential constitutional republic and liberal democracy with three separate branches of government: executive, legislative, and judicial. It has a bicameral national legislature composed of the House of Representatives, a lower house based on population; and the Senate,
# """
# response = mcqs_from_text(text)
# print(response)

