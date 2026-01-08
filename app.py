from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import time
from dotenv import load_dotenv

# Load the variables from .env
load_dotenv()

# Get the key from the environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# --- GOOGLE AI STUDIO IMPORTS ---
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

app = Flask(__name__)
CORS(app)


# Global variable for the knowledge base
vectorstore = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global vectorstore
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_path = f"./temp_{file.filename}"
    file.save(file_path)

    try:
        # 1. Load and Split
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        chunks = text_splitter.split_documents(pages)

        # 2. Embed using Google (Latest model to avoid quota issues)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", 
            google_api_key=GOOGLE_API_KEY
        )
        
        # Batch upload to avoid 429 Rate Limit
        vectorstore = Chroma(embedding_function=embeddings)
        batch_size = 5
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            vectorstore.add_documents(batch)
            time.sleep(1) # Safety pause

        os.remove(file_path)
        return jsonify({"message": f"Successfully indexed {len(pages)} pages!"}), 200
    
    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    global vectorstore
    data = request.json
    user_query = data.get("question")

    if not vectorstore:
        return jsonify({"error": "Please upload a PDF first"}), 400

    try:
        # 3. Retrieve context
        docs = vectorstore.similarity_search(user_query, k=4)
        context = "\n".join([d.page_content for d in docs])
        
        # 4. Generate Answer using Gemini
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=GOOGLE_API_KEY
        )
        
        prompt = f"Context: {context}\n\nQuestion: {user_query}\n\nAnswer clearly based on the PDF."
        response = llm.invoke(prompt)
        
        # Fixed return statement (resolves your Pylance error "d is not defined")
        return jsonify({
            "answer": response.content,
            "sources": [doc.metadata.get("page", 0) + 1 for doc in docs]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)