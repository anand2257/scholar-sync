
**SCHOLAR SYNC: OFFICIAL REPOSITORY**

**OVERVIEW**

Scholar Sync is a high-end academic research tool designed to transform static PDF documents into interactive, searchable knowledge bases. By leveraging Retrieval-Augmented Generation (RAG) through Google’s Gemini 1.5 Flash, this application allows students and researchers to extract precise information from complex documents with a sleek, distraction-free interface.

---

**CORE FEATURES**

1. Intelligent Knowledge Sync: The system creates a mathematical map of your PDF, allowing the AI to "read" and "remember" specific sections of the text to provide grounded, factual answers.
2. Premium Typewriter UI: Responses are generated letter-by-letter to mimic a real-time academic assistant. All messy formatting is automatically cleaned for a high-quality reading experience.
3. Study-Optimized Layout: Using a Bento-grid architecture, the workspace separates your library from your chat environment to maximize focus.

---

**TECHNOLOGY STACK AND LIBRARIES**

The following libraries are required to run Scholar Sync. These specific versions ensure the AI logic and the Flask server communicate without errors.

* flask==3.0.2 (Web Framework)
* flask-cors==4.0.0 (Cross-Origin Resource Sharing)
* langchain-google-genai==1.0.1 (Gemini API Integration)
* langchain-community==0.0.27 (RAG Utilities)
* pypdf==4.1.0 (PDF Parsing)
* chromadb==0.4.24 (Vector Database)
* python-dotenv==1.0.1 (Secret Management)
* google-generativeai==0.4.1 (Core Gemini Engine)

---

**INSTALLATION GUIDE**

Step 1: Environment Preparation
python -m venv venv
.\venv\Scripts\activate

Step 2: Dependency Installation
pip install -r requirements.txt

Step 3: Configuration
Create a file named .env in the main folder and add your key:
GOOGLE_API_KEY=your_gemini_key_here

Step 4: Launch
python app.py

---

**HOW IT WORKS**

1. Ingestion: The pypdf library extracts raw text from your uploaded document.
2. Chunking: Recursive text splitters break the document into 2000-character segments.
3. Embedding: The Google text-embedding-004 model converts text into vectors.
4. Storage: ChromaDB stores these vectors locally on your machine.
5. Generation: When a question is asked, Gemini 1.5 Flash uses the retrieved chunks to write a human-like response.

---
