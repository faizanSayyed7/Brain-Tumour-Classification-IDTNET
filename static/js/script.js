document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.getElementById('uploadZone');
    const imageInput = document.getElementById('imageInput');
    const uploadForm = document.getElementById('uploadForm');
    const classifyBtn = document.querySelector('.classify-btn');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

    uploadZone.addEventListener('click', () => imageInput.click());
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) handleFileSelection(files[0]);
    });
    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleFileSelection(e.target.files[0]);
    });

    function handleFileSelection(file) {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/dicom'];
        if (!validTypes.includes(file.type) && !file.name.toLowerCase().endsWith('.dcm')) {
            showAlert('Please select a valid image file (JPEG, PNG) or DICOM file.', 'warning');
            return;
        }
        if (file.size > 16 * 1024 * 1024) {
            showAlert('File size too large. Please select a file smaller than 16MB.', 'warning');
            return;
        }
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
            classifyBtn.disabled = false;
            uploadZone.classList.add('file-selected');
            uploadZone.querySelector('.upload-content').innerHTML =
                `<i class="fas fa-check-circle text-success"></i>
                <h5 class="text-success">File Selected: ${file.name}</h5>
                <p class="text-muted">Ready for classification</p>`;
        };
        reader.readAsDataURL(file);
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!imageInput.files.length) {
            showAlert('Please select an image file first.', 'warning');
            return;
        }
        loadingModal.show();
        const formData = new FormData();
        formData.append('image', imageInput.files[0]);

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            loadingModal.hide();
            if (result.success) displayResults(result);
            else showAlert(result.error || 'Classification failed. Please try again.', 'danger');
        } catch (error) {
            loadingModal.hide();
            showAlert('Network error. Please check your connection and try again.', 'danger');
        }
    });

    function displayResults(result) {
        resultsContainer.innerHTML = '';
        if (result.demo_mode) {
            const demoAlert = document.createElement('div');
            demoAlert.className = 'col-12';
            demoAlert.innerHTML =
                `<div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    <strong>Demo Mode:</strong> Showing simulated predictions.
                </div>`;
            resultsContainer.appendChild(demoAlert);
        }
        result.predictions.forEach((prediction, index) => {
            const resultCard = createResultCard(prediction, index);
            resultsContainer.appendChild(resultCard);
        });
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function createResultCard(prediction, index) {
        const col = document.createElement('div');
        col.className = 'col-lg-3 col-md-6';
        const confidence = parseFloat(prediction.confidence);
        let confidenceClass = 'success';
        if (confidence < 70) confidenceClass = 'warning';
        if (confidence < 50) confidenceClass = 'danger';
        col.innerHTML =
            `<div class="result-card">
                <div class="result-header">
                    <div class="model-icon">
                        <i class="fas ${prediction.icon}"></i>
                    </div>
                    <h5 class="model-name">${prediction.model}</h5>
                </div>
                <div class="result-body">
                    <div class="prediction-result">
                        <h6>Prediction:</h6>
                        <div class="prediction-value">${prediction.prediction}</div>
                    </div>
                    <div class="confidence-score text-center">
                        <div class="confidence-label">Confidence</div>
                        <div class="confidence-value badge bg-${confidenceClass}">${prediction.confidence}%</div>
                    </div>
                    <div class="model-stats">
                        <div class="stat">
                            <span class="stat-label">Processing Time:</span>
                            <span class="stat-value">${prediction.processing_time}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Model Accuracy:</span>
                            <span class="stat-value">${prediction.accuracy}%</span>
                        </div>
                    </div>
                </div>
            </div>`;
        return col;
    }

    function showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
        alertContainer.innerHTML =
            `${message}
             <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
        document.body.appendChild(alertContainer);
        setTimeout(() => {
            if (alertContainer.parentNode) alertContainer.remove();
        }, 5000);
    }
});
