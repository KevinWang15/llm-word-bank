import re
import nltk
import json
import markdown2
import pdfkit
from nltk.tokenize import sent_tokenize


# Define a class to hold the parts of the markdown file
class MarkdownParts:
    def __init__(self):
        self.transcript = ""
        self.wordBank = ""


# Ensure the Punkt tokenizer data is downloaded for sentence tokenization
nltk.download('punkt')


# Function to read a file and return its contents
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


# Function to load a JSON file and return its contents
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


# Load the annotated transcript and split it into sentences
annotated_transcript = read_file("./files/annotated_transcript.txt")
annotated_transcript_sentences = sent_tokenize(annotated_transcript)
annotated_transcript_sentences = [line.strip() for sentence in annotated_transcript_sentences for line in sentence.split('\n')]

markdown_parts = MarkdownParts()

# Define the pattern to match word bank references in the text
word_bank_matcher_pattern = re.compile(r'\[(\d+)\.(.*?)\]')

# Replace word bank references in the transcript with bold markdown
markdown_parts.transcript = word_bank_matcher_pattern.sub(r'**\2**', annotated_transcript)

# Load the word bank explanations and original word bank
word_bank_explanation = load_json("./files/wordbank_explanation.json")

# Build a dictionary to map numbers to original words from the word bank file
number_to_original = {}
with open('files/wordbank.txt', 'r') as file:
    for line in file:
        number, original = line.strip().split('. ', 1)
        number_to_original[int(number)] = original

# Add the original word to each item in the word bank explanation
for item in word_bank_explanation:
    item['original'] = number_to_original.get(item['number'], "")

# Find a sentence for each item in the word bank explanation
for item in word_bank_explanation:
    number = item['number']
    for sentence in annotated_transcript_sentences:
        match = re.search(f'\\[{number}.([^\\]]+)]', sentence)
        if match:
            # Highlight the matched word
            formatted_sentence = sentence.replace(match.group(0), f'**{match.group(1)}**')
            # Remove other word bank references
            formatted_sentence = word_bank_matcher_pattern.sub(r'\2', formatted_sentence)
            item['sentence'] = formatted_sentence
            break

# Build the word bank section of the markdown file
for item in word_bank_explanation:
    markdown_parts.wordBank += (
        f'{item["number"]}. **{item["original"]}**: *[{item["partOfSpeech"]}]* {item["chinese"]}\n'
        f'    - {item["sentence"]}\n'
    )

markdown_output_content_transcript = f'# Transcript\n\n{markdown_parts.transcript}'
markdown_output_content_word_bank = f'# Word Bank\n\n{markdown_parts.wordBank}'
# Write the markdown file
markdown_output_content = f'{markdown_output_content_transcript}\n\n{markdown_output_content_word_bank}'

with open("./output.md", 'w', encoding='utf-8') as file:
    file.write(markdown_output_content)

# Convert the markdown to HTML
html_content = f'''
<html>
<head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
</head>
<body>
    {markdown2.markdown(markdown_output_content_transcript)}
    <div style="page-break-before: always;"></div>
    {markdown2.markdown(markdown_output_content_word_bank)}
</body>
</html>
'''

# Convert the HTML content to PDF using pdfkit
# Including the custom CSS file for styling
pdfkit.from_string(
    html_content,
    "output.pdf",
    css="assets/pdf_style.css",
    options={
        'margin-top': '2.4cm',
        'margin-right': '2cm',
        'margin-bottom': '2.4cm',
        'margin-left': '2cm',
    }
)
