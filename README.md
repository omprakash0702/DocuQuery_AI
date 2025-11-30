# 📄 DocuQuery AI – AI-Powered Document Intelligence System

DocuQuery AI is an end-to-end **AI-powered document understanding and question-answering system** that allows users to upload documents (PDFs, images, or text files), automatically extract their content using **PDF parsing and OCR**, and ask natural language questions using a **Retrieval-Augmented Generation (RAG)** workflow powered by a Large Language Model (LLM).

This project focuses on building a **practical, production-style AI pipeline** by integrating document processing, OCR, backend APIs, and LLM-based reasoning into a single system.

---

## 🚀 Key Features

- Upload and process:
  - Digital PDFs
  - Scanned PDFs
  - Images (JPG, PNG, WEBP)
  - Text and code files
- Automatic file type detection
- Text extraction from PDFs using `pdfplumber`
- OCR fallback for scanned documents using `pytesseract`
- PDF page preview using `pdf2image`
- AI-powered question answering using LLM-based RAG
- REST API-based backend using Flask
- Interactive and responsive web interface

---

## 🧠 Core AI & Engineering Concepts

- Optical Character Recognition (OCR)
- Document parsing and preprocessing
- Retrieval-Augmented Generation (RAG)
- Prompt engineering
- LLM API integration
- REST API design
- Full-stack AI system integration
- Error handling and fallback pipelines

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- pdfplumber
- pdf2image
- pytesseract
- Pillow
- python-dotenv
- Werkzeug

### AI
- OpenAI API (LLM-based question answering)

### Frontend
- HTML
- CSS
- JavaScript (Fetch API)

---

## 🏗️ System Workflow

1. User uploads a document from the web interface.
2. Backend detects the file type automatically.
3. Based on file type:
   - **Digital PDF** → Text extracted using `pdfplumber`
   - **Scanned PDF** → Converted to image → OCR using `pytesseract`
   - **Image file** → OCR applied directly
   - **Text file** → Direct decoding
4. Extracted text is stored as contextual knowledge.
5. User submits a natural language question.
6. Document text + user query are sent to the LLM through a RAG-style prompt.
7. The AI generates a grounded answer based strictly on the document.
8. The response is displayed in the UI in real time.

---

## 📁 Project Structure


DocuQuery_AI/
|
├── app.py
├── config.py
├── pdf_utils.py
├── ocr_utils.py
├── rag_utils.py
├── file_utils.py
├── graph.py
├── requirements.txt
├── runtime.txt
├── README.md
|
├── templates/
|   └── index.html
|
└── static/
    ├── app.js
    └── style.css



---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/` | GET | Home page |
| `/upload` | POST | Upload and process a file |
| `/preview_pdf_page` | POST | Preview selected PDF page |
| `/extract_pdf` | POST | Extract PDF text (page/range/full) |
| `/ocr` | POST | Run OCR on image |
| `/chat` | POST | Ask questions using RAG |

---

## 🧪 Example Use Cases

- Ask questions from research papers
- Extract text from scanned notes
- Summarize PDF reports
- Query invoices or bills
- Educational document analysis

---

## 📊 Learnings

- Designed a full multi-step AI workflow
- Integrated OCR + LLM reasoning
- Built REST APIs for document processing
- Handled real-world document edge cases
- Implemented RAG-style question answering
- Learned practical deployment challenges

---

## 🔮 Future Improvements

- Add vector embeddings + FAISS for advanced RAG
- Use EasyOCR / PaddleOCR for better accuracy
- Multi-document querying
- Automatic summarization and key-entity extraction
- Session memory and chat history
- Full cloud deployment (Render / AWS / Streamlit Cloud)

---

## 📹 Demo Video

https://drive.google.com/file/d/1d-gUCekkUgPPC9ay5JFjKJeG5n1fy5xv/view?usp=drive_link
---

## 📎 GitHub Repository
https://github.com/omprakash0702/DocuQuery_AI


---

## ✅ Conclusion

DocuQuery AI is a complete **Document Intelligence and Question-Answering system** that demonstrates how OCR, PDF parsing, and LLM-based reasoning can be combined into a real-world AI application. The project highlights strong applied AI skills, system design thinking, and clean backend–frontend integration.

---

**Author:** Omprakash  
**Domain:** Applied AI | Document Intelligence | RAG Systems

