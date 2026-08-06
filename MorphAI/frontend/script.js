// ==================================================
// MORPHAI - Frontend Interactive Scripts (FINAL)
// ==================================================

document.addEventListener('DOMContentLoaded', function() {

    console.log('✅ MorphAI frontend loaded');
    console.log('📍 Backend URL: http://127.0.0.1:5000');

    // ---- DARK MODE TOGGLE ----
    const darkToggle = document.getElementById('darkModeToggle');
    if (darkToggle) {
        darkToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('dark-mode');
            const icon = this.querySelector('i');
            if (document.body.classList.contains('dark-mode')) {
                icon.className = 'fas fa-sun';
            } else {
                icon.className = 'fas fa-moon';
            }
        });
    }

    // ---- IMAGE UPLOAD ----
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const predictBtn = document.getElementById('predictBtn');
    const resetBtn = document.getElementById('resetBtn');
    const origResult = document.getElementById('origResult');
    const genResult = document.getElementById('genResult');
    const statusBadge = document.querySelector('#predictionStatus .badge');
    const confidenceSpan = document.getElementById('confidenceVal');
    const timeSpan = document.getElementById('timeVal');
    const progressStatus = document.getElementById('progressStatus');

    let uploadedFile = null;

    // Upload button
    if (uploadBtn) {
        uploadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            fileInput.click();
        });
    }

    // Drop zone
    if (dropZone) {
        dropZone.addEventListener('click', function(e) {
            e.preventDefault();
            fileInput.click();
        });

        dropZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = '#2563EB';
            this.style.background = 'rgba(37,99,235,0.05)';
        });

        dropZone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.borderColor = '#cbd5e1';
            this.style.background = '';
        });

        dropZone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = '#cbd5e1';
            this.style.background = '';
            if (e.dataTransfer.files.length) {
                handleFile(e.dataTransfer.files[0]);
            }
        });
    }

    // File input
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length) {
                handleFile(this.files[0]);
            }
        });
    }

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            showNotification('Please upload an image file.', 'error');
            return;
        }
        uploadedFile = file;
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('d-none');
            origResult.src = e.target.result;
            if (statusBadge) {
                statusBadge.textContent = 'Image loaded';
                statusBadge.className = 'badge bg-warning text-dark';
            }
            if (confidenceSpan) confidenceSpan.textContent = '--';
            if (timeSpan) timeSpan.textContent = '--';
            if (genResult) genResult.src = 'https://placehold.co/150x150/eee/bbb?text=Generated';
            showNotification('Image uploaded successfully!', 'success');
        };
        reader.readAsDataURL(file);
    }

    // ---- PREDICT BUTTON (FIXED) ----
    if (predictBtn) {
        predictBtn.addEventListener('click', function(e) {
            // ⭐ CRITICAL: Prevent page refresh!
            e.preventDefault();
            e.stopPropagation();
            
            if (!uploadedFile) {
                showNotification('Please upload an image first.', 'error');
                return;
            }

            // Show loading
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processing...';
            if (statusBadge) {
                statusBadge.textContent = 'Processing...';
                statusBadge.className = 'badge bg-info';
            }
            if (progressStatus) {
                progressStatus.innerHTML = `
                    <div class="d-flex align-items-center gap-2">
                        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
                        <span>Sending to backend...</span>
                    </div>
                `;
            }

            // Create form data
            const formData = new FormData();
            formData.append('image', uploadedFile);

            // Send to backend
            fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error('HTTP ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                console.log('Data received:', data);
                
                if (data.success) {
                    if (genResult) {
                        genResult.src = 'data:image/jpeg;base64,' + data.generated_image;
                    }
                    if (statusBadge) {
                        statusBadge.textContent = 'Prediction Complete';
                        statusBadge.className = 'badge bg-success';
                    }
                    if (confidenceSpan) confidenceSpan.textContent = data.confidence;
                    if (timeSpan) timeSpan.textContent = data.processing_time;
                    
                    if (progressStatus) {
                        progressStatus.innerHTML = `
                            <div class="alert alert-success py-2 px-3 mb-0 rounded-pill">
                                <i class="fas fa-check-circle me-1"></i> 
                                Complete in ${data.processing_time}s | 
                                SSIM: ${data.ssim} | 
                                PSNR: ${data.psnr} | 
                                FID: ${data.fid}
                            </div>
                        `;
                    }
                    
                    showNotification('Prediction completed!', 'success');
                } else {
                    throw new Error(data.error || 'Unknown error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error: ' + error.message, 'error');
                if (statusBadge) {
                    statusBadge.textContent = 'Error';
                    statusBadge.className = 'badge bg-danger';
                }
                if (progressStatus) {
                    progressStatus.innerHTML = `
                        <div class="alert alert-danger py-2 px-3 mb-0">
                            <i class="fas fa-exclamation-triangle me-1"></i>
                            ${error.message}
                        </div>
                    `;
                }
            })
            .finally(() => {
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-wand-magic-sparkles me-1"></i>Predict';
            });
        });
    }

    // ---- RESET BUTTON ----
    if (resetBtn) {
        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            uploadedFile = null;
            if (fileInput) fileInput.value = '';
            if (previewContainer) previewContainer.classList.add('d-none');
            if (imagePreview) imagePreview.src = '#';
            if (origResult) origResult.src = 'https://placehold.co/150x150/eee/bbb?text=Original';
            if (genResult) genResult.src = 'https://placehold.co/150x150/eee/bbb?text=Generated';
            if (statusBadge) {
                statusBadge.textContent = 'Waiting for input';
                statusBadge.className = 'badge bg-secondary';
            }
            if (confidenceSpan) confidenceSpan.textContent = '--';
            if (timeSpan) timeSpan.textContent = '--';
            if (progressStatus) progressStatus.innerHTML = '';
            if (predictBtn) {
                predictBtn.disabled = false;
                predictBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles me-1"></i>Predict';
            }
            showNotification('Reset successful', 'info');
        });
    }

    // ---- NOTIFICATION SYSTEM ----
    function showNotification(message, type = 'info') {
        const colors = {
            success: '#10B981',
            error: '#EF4444',
            info: '#2563EB',
            warning: '#F59E0B'
        };
        const toast = document.createElement('div');
        toast.className = 'position-fixed bottom-0 end-0 p-3';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <div class="toast show align-items-center text-white border-0 rounded-4 shadow-lg" 
                 style="background: ${colors[type] || '#2563EB'};" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'} me-2"></i> 
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

    // ---- BACK TO TOP ----
    const backBtn = document.createElement('button');
    backBtn.className = 'btn btn-primary rounded-circle position-fixed';
    backBtn.style.bottom = '2rem';
    backBtn.style.right = '2rem';
    backBtn.style.width = '48px';
    backBtn.style.height = '48px';
    backBtn.style.display = 'none';
    backBtn.style.zIndex = '999';
    backBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    document.body.appendChild(backBtn);

    window.addEventListener('scroll', function() {
        backBtn.style.display = window.scrollY > 400 ? 'block' : 'none';
    });

    console.log('✅ MorphAI frontend ready!');
    console.log('📍 Backend URL: http://127.0.0.1:5000');
});