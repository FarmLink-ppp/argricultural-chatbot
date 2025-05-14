# app.py
from flask import Flask, render_template, request, jsonify
from chat1 import fetch_website_content, initialize_vector_store
from chat2 import setup_retrieval_qa
from test import extract_text_file

app = Flask(__name__)

# Example URLs and PDF files
urls = ["https://boosteno.com/"]   # Make sure no invisible bad characters
pdf_files = ["Data/farmerbook.txt"]

# Fetch content from websites
website_contents = [fetch_website_content(url) for url in urls]

# Extract text from PDF files
pdf_texts = [extract_text_file(pdf_file) for pdf_file in pdf_files]

# Combine all content into chunks
all_contents = website_contents + pdf_texts

# Initialize the vector store
db = initialize_vector_store(all_contents)

# Set up the RetrievalQA chain
chain = setup_retrieval_qa(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()  # <-- Read JSON body
    if not data or 'messageText' not in data:
        return jsonify({"error": "Missing 'messageText' in JSON body."}), 400

    query = data['messageText'].strip().lower()

    if query in ["who developed you?", "who created you?", "who made you?"]:
        return jsonify({"answer": "I was developed by Wayzello."})

    response = chain(query)
    return jsonify({"answer": response['result']})

if __name__ == "__main__":
    app.run(debug=True)