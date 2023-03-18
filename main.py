# Tried of having to pay for pdf summarizers? Well look no further. 70% of code was me the rest was GPT generated
# haha. Developer: Niraj Nepal Date: 03/16/2023 References:
# https://pypdf2.readthedocs.io/en/latest/user/extract-text.html ,
# https://platform.openai.com/docs/api-reference/models/retrieve?lang=python ,
# https://analyzingalpha.com/openai-api-python-tutorial

import openai
import PyPDF2

openai.api_key = "your api key here"


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text


# Function to split the text into chunks
def chunk_text(text, chunk_size=2048):
    tokens = text.split()
    chunks = []
    current_chunk = []

    for token in tokens:
        if len(current_chunk) + len(token) + 1 > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
        current_chunk.append(token)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


# Define your prompt and what the summary should output, incase you want it to extract certain information
# Function to summarize text using GPT-3
def summarize_text(text, model="text-davinci-002",
                   tokens=150):  # model = gpt-4 ( once limited beta is released. ) tokens change to 8000 once release
    response = openai.Completion.create(
        engine=model,
        # define your prompt here prompt=f"Please summarize the following text, and give main points and ideas about
        # crisis communication, I want 10-12 great points on crisis communication:\n\n{text}\n",
        prompt=f"Summarize the pdf give detailed information, give me about 4 paragraphs, give me bullet points as well:\n\n{text}\n",
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary


# Modified function to summarize text using GPT-3 in chunks
def summarize_text_chunks(text, model="text-davinci-002", tokens=150):
    chunks = chunk_text(text)
    summarized_chunks = []

    for chunk in chunks:
        summary = summarize_text(chunk, model=model, tokens=tokens)
        summarized_chunks.append(summary)

    return ' '.join(summarized_chunks)


# Function to save the summary to a text file
def save_summary_to_file(summary, output_file):
    with open(output_file, 'w') as file:
        file.write(summary)


# Main function
def main(pdf_path, output_file):
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text_chunks(text)
    save_summary_to_file(summary, output_file)
    print(f"Summary saved to {output_file}")


# PDF_Path = file location + output_file = summary location
############################################################################################
if __name__ == "__main__":
    pdf_path = r"C:\Users\pokem\Downloads\lol.pdf"
    output_file = r"C:\Users\pokem\OneDrive\Desktop\output.txt"
    main(pdf_path, output_file)
############################################################################################
