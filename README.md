# 📄 DocuQuery AI – AI-Powered Document Query System

DocuQuery AI is an **Applied AI project** that allows users to upload documents (PDFs, images, or text files), extract their content using **PDF parsing and OCR**, and ask questions using a **Retrieval-Augmented Generation (RAG)** workflow powered by an LLM.

This project was built for the **EONVERSE AI Intern – Applied AI Build Challenge (Option 2)**.

---

## 🚀 Features

- Upload and process:
  - PDF files
  - Scanned PDFs
  - Images (JPG, PNG, WEBP)
  - Text and code files
- Automatic file type detection
- PDF text extraction using `pdfplumber`
- OCR fallback for scanned documents using `pytesseract`
- PDF page preview using `pdf2image`
- AI-powered question answering using OpenAI (RAG-style)
- Clean and interactive web UI
- REST API based backend (Flask)

---

## 🧠 Core AI Concepts Used

- Optical Character Recognition (OCR)
- Document parsing and preprocessing
- Retrieval-Augmented Generation (RAG)
- Prompt engineering
- LLM API integration
- End-to-end AI pipeline design

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

### AI
- OpenAI API (LLM-based answering)

### Frontend
- HTML
- CSS
- JavaScript (Fetch API)

---

## 🏗️ System Workflow

1. User uploads a file from the UI.
2. Backend detects file type.
3. If file is:
   - **PDF (digital)** → Text extracted using `pdfplumber`
   - **PDF (scanned)** → Converted to image → OCR using `pytesseract`
   - **Image** → OCR applied directly
   - **Text file** → Direct decoding
4. Extracted text becomes the context for the LLM.
5. User enters a question.
6. Document text + user query is sent to the OpenAI API.
7. AI returns a grounded answer based on the document.
8. Result is displayed in the UI.

---

## 📁 Project Structure

DocuQuery_AI/
│
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
│
├── templates/
│ └── index.html
│
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

A short demo video explaining the workflow and code is included in the submission as required by EONVERSE.

---

## 📎 GitHub Repository
https://github.com/omprakash0702/DocuQuery_AI

---

## ✅ Conclusion

DocuQuery AI demonstrates a complete **Applied AI system** that combines document processing, OCR, and LLM-based reasoning into a practical solution. It reflects curiosity, technical depth, and strong system integration skills.

---

**Developed by:** Omprakash  
**Category:** Applied AI | Document Intelligence | RAG System  
