document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const processBtn = document.getElementById('processBtn');
    let currentFile = null;

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary-color)';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-color)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-color)';
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    // Click to upload
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // Process button click handler
    processBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        try {
            processBtn.disabled = true;
            processBtn.textContent = 'Processing...';

            const formData = new FormData();
            formData.append('file', currentFile);

            const baseUrl = 'http://localhost:8000';  // Make sure this matches your FastAPI port
            
            // Update fetch configuration
            const uploadResponse = await fetch(`${baseUrl}/upload`, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                },
                credentials: 'include'
            });

            if (!uploadResponse.ok) {
                const errorData = await uploadResponse.json();
                throw new Error(errorData.detail || 'Failed to upload document');
            }

            const uploadData = await uploadResponse.json();
            
            const chatResponse = await fetch(`${baseUrl}/chatid/${uploadData.document_id}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                },
                credentials: 'include'
            });

            if (!chatResponse.ok) {
                throw new Error('Failed to get chat session');
            }

            const chatData = await chatResponse.json();

            // Show success message
            fileInfo.innerHTML = `
                <p class="success">✅ Document uploaded successfully</p>
                <p>Document ID: ${uploadData.document_id}</p>
                <p>Chat Session ID: ${chatData.chatid}</p>
            `;
            
        } catch (error) {
            console.error('Error:', error);
            if (error.message === 'Failed to fetch') {
                fileInfo.innerHTML = `
                    <p class="error">❌ Cannot connect to server. Please make sure the backend is running.</p>
                `;
            } else {
                fileInfo.innerHTML = `
                    <p class="error">❌ ${error.message}</p>
                `;
            }
        } finally {
            processBtn.disabled = false;
            processBtn.textContent = 'Process Document';
        }
    });

    // File handling function
    function handleFiles(files) {
        if (files.length === 0) return;

        const file = files[0];
        if (file.type !== 'application/pdf') {
            fileInfo.innerHTML = '<p class="error">❌ Please upload a PDF file</p>';
            processBtn.disabled = true;
            return;
        }

        if (file.size > 10 * 1024 * 1024) { // 10MB limit
            fileInfo.innerHTML = '<p class="error">❌ File size should be less than 10MB</p>';
            processBtn.disabled = true;
            return;
        }

        currentFile = file;
        fileInfo.innerHTML = `
            <p>Selected file: ${file.name}</p>
            <p>Size: ${(file.size / 1024).toFixed(2)} KB</p>
        `;
        processBtn.disabled = false;
    }
});
