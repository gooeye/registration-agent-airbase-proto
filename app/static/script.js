document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileNameSpan = document.getElementById('fileName');
    const messageDiv = document.getElementById('message');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const downloadLinkContainer = document.getElementById('downloadLinkContainer');
    const submitButton = uploadForm.querySelector('button[type="submit"]');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileNameSpan.textContent = fileInput.files[0].name;
            submitButton.disabled = false; // Enable button when a file is selected
        } else {
            fileNameSpan.textContent = 'No file chosen';
            submitButton.disabled = true; // Disable button if no file
        }
        messageDiv.textContent = ''; // Clear messages on new file selection
        messageDiv.className = 'message';
        downloadLinkContainer.innerHTML = ''; // Clear download link
        loadingIndicator.style.display = 'none'; // Hide loading indicator
    });

    // Initially disable the submit button
    submitButton.disabled = true;

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (fileInput.files.length === 0) {
            showMessage('Please select a file to upload.', 'error');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        messageDiv.textContent = '';
        messageDiv.className = 'message';
        downloadLinkContainer.innerHTML = '';
        loadingIndicator.style.display = 'block'; // Show loading indicator
        submitButton.disabled = true; // Disable button during upload

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const contentDisposition = response.headers.get('Content-Disposition');
                let filename = 'processed_file';
                if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
                    const filenameMatch = contentDisposition.match(/filename="([^"]+)"/);
                    if (filenameMatch && filenameMatch[1]) {
                        filename = filenameMatch[1];
                    }
                }

                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const downloadLink = document.createElement('a');
                downloadLink.href = downloadUrl;
                downloadLink.textContent = `Download Processed File: ${filename}`;
                downloadLink.setAttribute('download', filename);
                downloadLinkContainer.appendChild(downloadLink);
                showMessage('File processed successfully. Click the link to download.', 'success');
            } else {
                const errorData = await response.json();
                showMessage(errorData.error || 'An unknown error occurred.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Network error or server is unreachable.', 'error');
        } finally {
            loadingIndicator.style.display = 'none'; // Hide loading indicator
            submitButton.disabled = false; // Re-enable button after process
        }
    });

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
    }
});