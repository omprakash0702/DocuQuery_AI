let selectedFile = null;

/* ---------------- DRAG & DROP ------------------- */
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

dropZone.onclick = () => fileInput.click();

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");

    selectedFile = e.dataTransfer.files[0];
    document.getElementById("uploadLabel").innerText = "Uploaded: " + selectedFile.name;

    uploadImageOrText();
});

fileInput.onchange = async (e) => {
    selectedFile = e.target.files[0];
    document.getElementById("uploadLabel").innerText = "Uploaded: " + selectedFile.name;

    uploadImageOrText();
};

/* ------ AUTO-HANDLE IMAGE OR TEXT UPLOAD ------ */
async function uploadImageOrText() {
    if (!selectedFile) return;

    const form = new FormData();
    form.append("file", selectedFile);

    const res = await fetch("/upload", {
        method: "POST",
        body: form
    });

    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    // IMAGE
    if (data.meta.type === "image") {
        document.getElementById("previewImg").src =
            URL.createObjectURL(selectedFile);
        document.getElementById("previewImg").style.display = "block";

        document.getElementById("extractedText").value =
            data.extracted || "";
    }

    // TEXT FILE
    if (data.meta.type === "text") {
        document.getElementById("extractedText").value = data.extracted;
    }
}

/* ---------------- Preview PDF Page ------------------- */
document.getElementById("previewBtn").onclick = async () => {
    if (!selectedFile) return alert("Upload a file first");

    const page = document.getElementById("previewPage").value || 1;

    const form = new FormData();
    form.append("file", selectedFile);
    form.append("page", page);

    const res = await fetch("/preview_pdf_page", {
        method: "POST",
        body: form
    });

    if (!res.ok) {
        alert("Preview failed");
        return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);

    const img = document.getElementById("previewImg");
    img.src = url;
    img.style.display = "block";
};

/* ---------------- Extract Page ------------------- */
document.getElementById("extractPageBtn").onclick = async () => {
    if (!selectedFile) return alert("Upload a file first");

    const form = new FormData();
    form.append("file", selectedFile);
    form.append("page", document.getElementById("extractPage").value);
    form.append("ocr", document.getElementById("forceOCR").checked);

    const res = await fetch("/extract_pdf", { method: "POST", body: form });
    const data = await res.json();
    document.getElementById("extractedText").value = data.text || "";
};

/* ---------------- Extract Full ------------------- */
document.getElementById("extractFullBtn").onclick = async () => {
    if (!selectedFile) return alert("Upload a file first");

    const form = new FormData();
    form.append("file", selectedFile);
    form.append("ocr", document.getElementById("forceOCR").checked);

    const res = await fetch("/extract_pdf", { method: "POST", body: form });
    const data = await res.json();
    document.getElementById("extractedText").value = data.text || "";
};

/* ---------------- Extract Range ------------------- */
document.getElementById("rangeInput").onchange = async () => {
    if (!selectedFile) return;

    const range = document.getElementById("rangeInput").value;
    const form = new FormData();
    form.append("file", selectedFile);
    form.append("range", range);
    form.append("ocr", document.getElementById("forceOCR").checked);

    const res = await fetch("/extract_pdf", { method: "POST", body: form });
    const data = await res.json();
    document.getElementById("extractedText").value = data.text || "";
};

/* ---------------- Chat ------------------- */
document.getElementById("sendChat").onclick = async () => {
    const question = document.getElementById("chatInput").value;
    const docText = document.getElementById("extractedText").value;

    if (!question.trim()) return alert("Enter a question");
    if (!docText.trim()) return alert("Extract text first");

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_text: docText, message: question })
    });

    const data = await res.json();
    typeWriter(data.answer);
};

/* ---- Terminal typing animation ---- */
function typeWriter(text) {
    const output = document.getElementById("chatOutput");
    output.innerText = "";
    let i = 0;

    const interval = setInterval(() => {
        if (i < text.length) {
            output.innerText += text[i++];
        } else {
            clearInterval(interval);
        }
    }, 20);
}
