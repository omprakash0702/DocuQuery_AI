import io
import pdfplumber
from pypdf import PdfReader
from PIL import Image
import fitz  # PyMuPDF

def extract_text_from_pdf_bytes(pdf_bytes):
    # Try pdfplumber first
    try:
        text = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text.append(t)
        if text:
            return "\n".join(text)
    except Exception:
        pass

    # fallback PyPDF / pypdf
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        out = []
        for p in reader.pages:
            txt = p.extract_text()
            if txt:
                out.append(txt)
        if out:
            return "\n".join(out)
    except Exception:
        pass

    return "NO_TEXT_FOUND_PDF"

def pdf_page_count(pdf_bytes):
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        return len(reader.pages)
    except Exception:
        try:
            import pdfplumber, io as _io
            with pdfplumber.open(_io.BytesIO(pdf_bytes)) as pdf:
                return len(pdf.pages)
        except:
            return 0

def extract_pdf_page_image_bytes(pdf_bytes, page_number=1, zoom=2):
    """
    Render a PDF page to PNG bytes using PyMuPDF (fitz).
    page_number is 1-indexed.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc.load_page(page_number - 1)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_bytes = pix.tobytes("png")
        return img_bytes
    except Exception as e:
        # fallback using pdfplumber + PIL rasterize (slower)
        try:
            import pdfplumber, io as _io
            with pdfplumber.open(_io.BytesIO(pdf_bytes)) as pdf:
                page = pdf.pages[page_number - 1]
                im = page.to_image(resolution=150)
                pil = im.original
                buf = io.BytesIO()
                pil.save(buf, format="PNG")
                return buf.getvalue()
        except Exception:
            raise e
