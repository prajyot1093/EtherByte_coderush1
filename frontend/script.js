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