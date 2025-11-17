import os
import io
import json
import logging
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv()

# local config (ensure CONFIG file exists)
from config import PORT, OPENAI_API_KEY  # OPENAI_API_KEY may be used by other modules

# local utilities
from pdf_utils import (
    extract_text_from_pdf_bytes,
    extract_pdf_page_image_bytes,
    pdf_page_count,
)
from ocr_utils import ocr_sync
from rag_utils import chunk_text
from file_utils import (
    extract_text_from_docx,
    extract_text_from_pptx,
    extract_text_from_xlsx_csv,
    extract_text_from_text_or_code,
    extract_text_from_ipynb,
)

from graph import run_rag_sync

# ===== app setup =====
app = Flask(__name__, template_folder="templates", static_folder="static")

# Limit uploads to 50 MB (adjust as needed)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

# Simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docuquery")

# If your frontend runs on a different origin, enable CORS
try:
    from flask_cors import CORS

    CORS(app)
    logger.info("CORS enabled")
except Exception:
    logger.info("flask_cors not installed or CORS not required")


def json_error(message, code=400):
    """Consistent JSON error helper."""
    return jsonify({"error": message}), code


@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# FILE UPLOAD
# ============================================================
@app.route("/upload", methods=["POST"])
def upload_file():
    from werkzeug.utils import secure_filename

    f = request.files.get("file")
    if not f:
        return json_error("No file uploaded", 400)

    filename = secure_filename(f.filename or "unnamed")
    data = f.read()
    size = len(data)
    logger.info("Upload: %s (%d bytes)", filename, size)

    lower = filename.lower()

    # -------------------------- IMAGE --------------------------
    if lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
        try:
            # ocr_sync should accept raw image bytes; confirm in your implementation
            extracted = ocr_sync(data)
            return jsonify(
                {
                    "meta": {"filename": filename, "size": size, "type": "image"},
                    "preview": {"type": "image"},
                    "extracted": extracted,
                }
            )
        except Exception as e:
            logger.exception("OCR failed")
            return json_error(f"OCR failed: {e}", 500)

    # -------------------------- PDF ----------------------------
    if lower.endswith(".pdf"):
        # try to get page count with pdf2image (optional)
        pages = 1
        try:
            from pdf2image import pdfinfo_from_bytes

            info = pdfinfo_from_bytes(data)
            pages = int(info.get("Pages", 1))
        except Exception as e:
            logger.info("pdf2image/pdfinfo unavailable or failed: %s", e)
            pages = 1

        return jsonify(
            {
                "meta": {
                    "filename": filename,
                    "size": size,
                    "type": "pdf",
                    "pages": pages,
                },
                "preview": {"type": "pdf", "pages": pages},
                "extracted": "",
            }
        )

    # -------------------------- TEXT / CODE ---------------------
    if lower.endswith((".txt", ".py", ".js", ".html", ".css", ".json", ".md")):
        try:
            text = data.decode(errors="ignore")
        except Exception:
            text = ""
        return jsonify(
            {
                "meta": {"filename": filename, "size": size, "type": "text"},
                "preview": {"type": "text"},
                "extracted": text,
            }
        )

    # -------------------------- UNSUPPORTED ---------------------
    return json_error("Unsupported file type", 400)


# ============================================================
# PDF PREVIEW PAGE (render to PNG)
# ============================================================
@app.route("/preview_pdf_page", methods=["POST"])
def preview_pdf_page():
    f = request.files.get("file")
    page = int(request.form.get("page", 1))

    if not f:
        return json_error("no file", 400)

    try:
        pdf_bytes = f.read()
        img_bytes = extract_pdf_page_image_bytes(pdf_bytes, page)
        return send_file(io.BytesIO(img_bytes), mimetype="image/png")
    except Exception as e:
        logger.exception("preview_pdf_page failed")
        return json_error(f"Preview error: {e}", 500)


# ============================================================
# PDF EXTRACTION (page / range / full)
# ============================================================
@app.route("/extract_pdf", methods=["POST"])
def extract_pdf_endpoint():
    f = request.files.get("file")
    if not f:
        return json_error("no file", 400)

    # prevent images from accidentally being sent here
    if f.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return json_error("Use /ocr for image extraction", 400)

    pdf_bytes = f.read()
    page = request.form.get("page")
    rng = request.form.get("range")
    do_ocr = request.form.get("ocr", "false").lower() == "true"

    # -------------------- SINGLE PAGE --------------------------
    if page:
        try:
            p = int(page)
        except Exception:
            return json_error("page must be numeric", 400)

        try:
            import pdfplumber

            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                total_pages = len(pdf.pages)
                if p < 1 or p > total_pages:
                    return json_error("page out of range", 400)

                text = pdf.pages[p - 1].extract_text()
                if (not text or not text.strip()) and do_ocr:
                    img = extract_pdf_page_image_bytes(pdf_bytes, p)
                    text = ocr_sync(img)

                return jsonify({"text": text or ""})
        except Exception as e:
            logger.exception("extract_pdf single page failed")
            return json_error(str(e), 500)

    # -------------------- RANGE X-Y -----------------------------
    if rng:
        if "-" not in rng:
            return json_error("Range must be 'start-end'", 400)

        try:
            start, end = [int(x.strip()) for x in rng.split("-", 1)]
        except Exception:
            return json_error("Range must be numeric", 400)

        if start > end:
            return json_error("Start cannot be greater than end", 400)

        try:
            import pdfplumber

            texts = []
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                total = len(pdf.pages)
                start_clamped = max(1, start)
                end_clamped = min(end, total)

                for p in range(start_clamped, end_clamped + 1):
                    t = pdf.pages[p - 1].extract_text()
                    if (not t or not t.strip()) and do_ocr:
                        img = extract_pdf_page_image_bytes(pdf_bytes, p)
                        t = ocr_sync(img)
                    texts.append(t or "")

            return jsonify({"text": "\n\n".join(texts)})
        except Exception as e:
            logger.exception("extract_pdf range failed")
            return json_error(f"PDF error: {e}", 500)

    # -------------------- FULL DOCUMENT -------------------------
    try:
        text = extract_text_from_pdf_bytes(pdf_bytes)
    except Exception as e:
        logger.exception("extract_text_from_pdf_bytes failed")
        return json_error(f"PDF extraction failed: {e}", 500)

    # fallback to OCR across pages if requested
    if (not text or text == "NO_TEXT_FOUND_PDF") and do_ocr:
        try:
            pages = pdf_page_count(pdf_bytes)
            all_text = []
            for p in range(1, pages + 1):
                img = extract_pdf_page_image_bytes(pdf_bytes, p)
                all_text.append(ocr_sync(img))
            return jsonify({"text": "\n\n".join(all_text)})
        except Exception as e:
            logger.exception("full OCR failed")
            return json_error(f"OCR error: {e}", 500)

    return jsonify({"text": text})


# ============================================================
# IMAGE OCR ENDPOINT
# ============================================================
@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    f = request.files.get("file")
    if not f:
        return json_error("no file", 400)

    try:
        img_bytes = f.read()
        text = ocr_sync(img_bytes)
        return jsonify({"text": text})
    except Exception as e:
        logger.exception("ocr failed")
        return json_error(f"OCR failed: {e}", 500)


# ============================================================
# CHAT + RAG PIPELINE
# ============================================================
@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json or {}
    doc_text = (payload.get("doc_text") or "").strip()
    message = (payload.get("message") or "").strip()

    if not message:
        return json_error("message required", 400)

    if not doc_text:
        # respond with consistent JSON
        return jsonify({"answer": "Please extract or upload a document first."})

    try:
        result = run_rag_sync(doc_text, message)
        return jsonify({"answer": result.get("answer", "")})
    except Exception as e:
        logger.exception("RAG failed")
        return jsonify({"answer": f"ERROR: {e}"})


# ============================================================
if __name__ == "__main__":
    # Use PORT from config or fallback to 8080
    port = int(os.environ.get("PORT", getattr(__import__("config"), "PORT", 8080)))
    app.run(host="0.0.0.0", port=port)
