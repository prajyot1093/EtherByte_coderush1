document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const outputDiv = document.getElementById("output");
if (fileInput.files.length === 0) {
        outputDiv.textContent = "⚠️ Please select a file first.";
        return;
    }
        const file = fileInput.files[0];
    outputDiv.innerHTML = `
        ✅ File <b>${file.name}</b> uploaded successfully.<br>
        🔍 Running analysis (plagiarism + AI detection + style check)...
    `;

 setTimeout(() => {
        outputDiv.innerHTML += `
            <p><b>Results:</b></p>
            <ul>
                <li>Plagiarism: 12%</li>
                <li>AI-Generated Probability: 35%</li>
                <li>Stylometric Match: Consistent ✅</li>
            </ul>
        `;
    }, 2000);
});

// --- Enhanced Upload & Submission Logic for CMT ---

// Elements
const form = document.getElementById("plagiarismForm");
const fileInput = document.getElementById("fileUpload");
const textInput = document.getElementById("sampleText");
const outputDiv = document.getElementById("plagiarismResult");
const filePreview = document.getElementById("filePreview");
const uploadArea = document.getElementById("uploadArea");
const uploadText = document.getElementById("uploadText");

// Drag & Drop Events
if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
        uploadText.textContent = "Drop your file here!";
    });
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        uploadText.textContent = "Drag & Drop or Click to Upload File";
    });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            showFilePreview(files[0]);
        }
        uploadText.textContent = "Drag & Drop or Click to Upload File";
    });
}

// File input change
if (fileInput) {
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length) {
            showFilePreview(fileInput.files[0]);
        } else {
            hideFilePreview();
        }
    });
}

// Show file preview
function showFilePreview(file) {
    if (!filePreview) return;
    filePreview.innerHTML = `
        <span>📄 ${file.name} (${Math.round(file.size/1024)} KB)</span>
        <button class="file-remove" title="Remove file">&times;</button>
    `;
    filePreview.classList.add('active');
    filePreview.querySelector('.file-remove').onclick = function() {
        fileInput.value = "";
        hideFilePreview();
    };
}
function hideFilePreview() {
    if (!filePreview) return;
    filePreview.classList.remove('active');
    filePreview.innerHTML = "";
}

// Clicking the upload area triggers file input
const uploadLabel = document.querySelector('.upload-label');
if (uploadLabel) {
    uploadLabel.addEventListener('click', function(e) {
        fileInput.click();
    });
}

// --- Submission to FastAPI backend ---
if (form) {
    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        outputDiv.textContent = "Analyzing submission...";

        const formData = new FormData();
        if (fileInput && fileInput.files.length) {
            formData.append('file', fileInput.files[0]);
        }
        if (textInput && textInput.value.trim()) {
            formData.append('text', textInput.value.trim());
        }

        if (!fileInput.files.length && (!textInput.value || !textInput.value.trim())) {
            outputDiv.textContent = "⚠️ Please upload a file or paste some text.";
            return;
        }

        try {
            const res = await fetch('http://127.0.0.1:8000/analyze', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            outputDiv.innerHTML = `
                <b>${data.message}</b>
                <br>
                <span style="font-size:0.95em;">
                    AI Score: ${data.ai_score} | Plagiarism Score: ${data.plagiarism_score} | Stylometric Score: ${data.stylometric_score}
                </span>
            `;
        } catch (err) {
            outputDiv.textContent = "❌ Error connecting to backend.";
        }
    });
}

// --- Dashboard Stats Fetch ---
async function updateDashboard() {
    try {
        const res = await fetch('http://127.0.0.1:8000/stats');
        const stats = await res.json();
        if(document.getElementById('submissions-processed')) document.getElementById('submissions-processed').textContent = stats.submissions_processed;
        if(document.getElementById('ai-flagged')) document.getElementById('ai-flagged').textContent = stats.ai_flagged + "%";
        if(document.getElementById('plagiarism-detected')) document.getElementById('plagiarism-detected').textContent = stats.plagiarism_detected + "%";
        if(document.getElementById('confidence-score')) document.getElementById('confidence-score').textContent = stats.confidence_score + "%";
        if(document.getElementById('processing-time')) document.getElementById('processing-time').textContent = stats.processing_time + "s";
        if(document.getElementById('false-positives')) document.getElementById('false-positives').textContent = stats.false_positives + "%";
    } catch (err) {
        // Optionally show error
    }
}
updateDashboard();
setInterval(updateDashboard, 10000); // Update every 10s

// --- Optional: Fetch submission history (for admin/history view) ---
// fetch('http://127.0.0.1:8000/submissions')
//   .then(res => res.json())
//   .then(data => { /* render submission history if needed */ });