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

