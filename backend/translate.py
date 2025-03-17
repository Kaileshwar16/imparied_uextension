import re
import os
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.parse.stanford import StanfordParser
import nltk
from num2words import num2words
from flask import Flask, request, jsonify

# Initialize Flask
app = Flask(__name__)

# Set up Stanford Parser (ensure you have the correct path to your jars)
java_path = "C:\\Program Files\\Java\\jdk-22\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path

sp = StanfordParser(path_to_jar="C:\\Users\\baran\\Downloads\\stanford-parser-full-2018-02-27\\stanford-parser-full-2018-02-27\\stanford-parser.jar",
                    path_to_models_jar="C:\\Users\\baran\\Downloads\\stanford-parser-full-2018-02-27\\stanford-parser-full-2018-02-27\\stanford-parser-3.9.1-models.jar")

stopwords_set = set(['a', 'an', 'the', 'is', 'to', 'The', 'in', 'of', 'us'])
root_path = 'NLP_dataset'
yt_path = 'yt'

# Load the NLP_videos CSV
NLP_videos = pd.read_csv("NLP_videos.csv")

def get_gif_path(character):
    gif_path = f"alphabet\\{character}_small.gif"
    
    if not os.path.exists(gif_path):
        print(f"Warning: GIF for character '{character}' not found. Skipping.")
        return None
    return gif_path

# Function to convert text to ISL
def text_to_isl(sentence):
    # Remove punctuation
    sentence = re.sub(r'[^\w\s]', '', sentence)
    englishtree = [tree for tree in sp.parse(sentence.split())]
    parsetree = englishtree[0]
    words = parsetree.leaves()
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(w) for w in words]
    islsentence = " ".join(w.lower() for w in lemmatized_words if w not in stopwords_set)
    return islsentence

def text_to_isl_images(input_text, chunk_size=500):
    def process_chunk(chunk):
        images = []  # List to store ISL sign images

        sentence = text_to_isl(chunk)
        words = sentence.split()

        for word in words:
            if (NLP_videos['Name'].eq(word)).any():
                idx = NLP_videos.index[NLP_videos['Name'] == word].tolist()[0]
                # Handle ISL sign for known words
                image_path = NLP_videos['isl_image_path'].iloc[idx]
                if os.path.exists(image_path):
                    images.append(image_path)
            else:
                # Handle unknown words (spelling out using gifs/images)
                for char in word:
                    if char.isalpha():
                        gif_path = get_gif_path(char.lower())  # Get image path for character
                        if gif_path:
                            images.append(gif_path)
                    elif char.isdigit():
                        # Handle numbers by spelling them out
                        number_name = num2words(int(char)).lower()
                        for letter in number_name:
                            if letter.isalpha():
                                gif_path = get_gif_path(letter)
                                if gif_path:
                                    images.append(gif_path)

        return images

    # Split the input text into manageable chunks
    chunks = [input_text[i:i + chunk_size] for i in range(0, len(input_text), chunk_size)]

    all_images = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}")
        chunk_images = process_chunk(chunk)
        all_images.extend(chunk_images)

    return all_images

# Define the route to handle text-to-ISL conversion
@app.route('/convert_to_isl', methods=['POST'])
def convert_to_isl_api():
    try:
        # Get the text input from the frontend
        data = request.get_json()
        input_text = data.get('sentence', '')

        # Process the text and get ISL image paths
        isl_images = text_to_isl_images(input_text)

        # Return the ISL images (paths or URLs) to the frontend
        return jsonify({"isl_images": isl_images})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
