document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    // Set active nav link based on current page
    const currentPage = window.location.pathname.split('/').pop();
    
    if (navLinks) {
        const navItems = navLinks.querySelectorAll('a');
        
    navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === currentPage || 
                (currentPage === '' && item.getAttribute('href') === 'index.html')) {
                item.classList.add('active');
            }
        });
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Active navigation link based on scroll position
    const sections = document.querySelectorAll('section');
    const navLinkItems = document.querySelectorAll('.nav-links a');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinkItems.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
    
    // Initialize FAQ accordion functionality
    initFAQ();
    
    // Disease Detection Page Functionality
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const detectBtn = document.getElementById('detect-btn');
    const previewImage = document.getElementById('preview-image');
    const resultDetails = document.getElementById('result-details');
    
    if (uploadArea && fileInput) {
        // Handle drag and drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            uploadArea.classList.add('highlight');
            uploadArea.querySelector('.upload-icon i').classList.add('fa-bounce');
        }
        
        function unhighlight() {
            uploadArea.classList.remove('highlight');
            uploadArea.querySelector('.upload-icon i').classList.remove('fa-bounce');
        }
        
        uploadArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
                handleFiles(files);
        }
        
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', () => {
            handleFiles(fileInput.files);
        });
        
        function handleFiles(files) {
            if (files.length > 0) {
            const file = files[0];
                if (file.type.match('image.*')) {
                    // Show loading animation while reading the file
                    resultDetails.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i><p>Loading image...</p></div>';
            
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                        previewImage.style.display = 'block';
                    detectBtn.disabled = false;
                        
                        // Add animation to the preview image
                        previewImage.classList.add('preview-loaded');
                        
                        resultDetails.innerHTML = `
                            <div class="upload-success">
                                <i class="fas fa-check-circle"></i>
                                <p>Image loaded successfully!</p>
                                <p class="hint">Click "Detect Disease" to analyze the image</p>
                            </div>
                        `;
                    }
                
                reader.readAsDataURL(file);
            } else {
                    showError('Please upload an image file (JPG, JPEG, or PNG)');
                }
            }
        }
        
        // Handle detect button click
        if (detectBtn) {
            detectBtn.addEventListener('click', () => {
                if (fileInput.files.length > 0) {
                    detectDisease(fileInput.files[0]);
                }
            });
        }
        
        // Function to show error messages
        function showError(message) {
            resultDetails.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>${message}</p>
                </div>
            `;
        }
        
        // Function to detect disease
        function detectDisease(file) {
            const formData = new FormData();
            formData.append('image', file);
            
            // Show loading state with progress animation
            resultDetails.innerHTML = `
                <div class="detection-loading">
                    <div class="loading-spinner">
                        <i class="fas fa-microscope fa-pulse"></i>
                    </div>
                    <h4>Analyzing Image</h4>
                    <div class="loading-steps">
                        <div class="loading-step active">
                            <span class="step-number">1</span>
                            <span class="step-text">Preprocessing image</span>
                            <i class="fas fa-check"></i>
                        </div>
                        <div class="loading-step">
                            <span class="step-number">2</span>
                            <span class="step-text">Analyzing patterns</span>
                            <i class="fas fa-check"></i>
                        </div>
                        <div class="loading-step">
                            <span class="step-number">3</span>
                            <span class="step-text">Identifying disease</span>
                            <i class="fas fa-check"></i>
                        </div>
                    </div>
                    <p class="loading-message">Please wait while our AI analyzes your image...</p>
                </div>
            `;
            
            detectBtn.disabled = true;
            
            // Simulate the steps of analysis for better UX
            setTimeout(() => {
                document.querySelector('.loading-step:nth-child(2)').classList.add('active');
            }, 1000);
            
            setTimeout(() => {
                document.querySelector('.loading-step:nth-child(3)').classList.add('active');
            }, 2000);
            
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
        .then(data => {
                if (data.error) {
                    showError(data.error);
                } else {
                    // Format the disease name for display
                    let diseaseName = data.prediction.replace(/_/g, ' ');
                    let diseaseClass = data.prediction.toLowerCase().replace(/[()]/g, '').replace(/_/g, '-');
                    
                    // Determine confidence level class
                    let confidenceLevel = 'low';
                    if (data.confidence > 0.7) confidenceLevel = 'high';
                    else if (data.confidence > 0.4) confidenceLevel = 'medium';
                    
                    // Create HTML for the result
                    let resultHTML = `
                        <div class="result-header">
                            <div class="result-icon ${diseaseClass}">
                                ${data.prediction === "Healthy" ? 
                                    '<i class="fas fa-check-circle"></i>' : 
                                    '<i class="fas fa-virus"></i>'}
                            </div>
                            <div class="result-title">
                                <h4>Detected Condition:</h4>
                                <p class="disease-name">${diseaseName}</p>
                            </div>
                        </div>
                        <div class="confidence">
                            <h4>Confidence: <span class="${confidenceLevel}">${(data.confidence * 100).toFixed(2)}%</span></h4>
                            <div class="confidence-bar">
                                <div class="confidence-level ${confidenceLevel}" style="width: ${(data.confidence * 100).toFixed(2)}%"></div>
                            </div>
                        </div>
                        <div class="all-probabilities">
                            <h4>All Probabilities:</h4>
                            <ul>
                    `;
                    
                    // Sort probabilities from highest to lowest
                    const sortedProbabilities = Object.entries(data.all_probabilities)
                        .sort((a, b) => b[1] - a[1]);
                    
                    // Add all probabilities
                    for (const [disease, probability] of sortedProbabilities) {
                        const formattedDisease = disease.replace(/_/g, ' ');
                        const probabilityPercent = (probability * 100).toFixed(2);
                        const isHighest = disease === data.prediction;
                        
                        resultHTML += `
                            <li class="${isHighest ? 'highest' : ''}">
                                <span class="disease-label">${formattedDisease}:</span>
                                <div class="probability-bar-container">
                                    <div class="probability-bar" style="width: ${probabilityPercent}%"></div>
                                    <span class="probability-value">${probabilityPercent}%</span>
                                </div>
                            </li>
                        `;
                    }
                    
                    resultHTML += `
                            </ul>
                        </div>
                    `;
                    
                    // Add disease information if available
                    if (data.disease_info) {
                        const info = data.disease_info;
                        
                        resultHTML += `
                            <div class="disease-details">
                                <h4>Disease Information:</h4>
                                <div class="info-item">
                                    <span class="info-label">Scientific Name:</span>
                                    <span class="info-value">${info.scientific_name}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">Symptoms:</span>
                                    <span class="info-value">${info.symptoms}</span>
                                </div>
                            </div>
                        `;
                    }
                    
                    // Add treatment recommendations based on the detected disease
                    if (data.prediction !== "Healthy") {
                        resultHTML += `
                            <div class="treatment">
                                <h4>Recommended Treatment:</h4>
                                <p>${data.disease_info ? data.disease_info.treatment : getTreatmentRecommendation(data.prediction)}</p>
                                <a href="diseases.html#${diseaseClass}" class="btn btn-sm">Learn More</a>
                </div>
                        `;
                    } else {
                        resultHTML += `
                            <div class="treatment healthy">
                                <h4>Healthy Leaf</h4>
                                <p>Your grape leaf appears to be healthy! Continue with your current vineyard management practices.</p>
                                <div class="healthy-tips">
                                    <h5>Maintenance Tips:</h5>
                                    <ul>
                                        <li>Regular monitoring for early signs of disease</li>
                                        <li>Proper pruning for good air circulation</li>
                                        <li>Balanced irrigation and nutrition</li>
                                    </ul>
            </div>
            </div>
        `;
                    }
        
        resultDetails.innerHTML = resultHTML;
                    
                    // Add animation to the results
                    setTimeout(() => {
                        document.querySelectorAll('.probability-bar').forEach(bar => {
                            bar.classList.add('animated');
                        });
                    }, 100);
                }
                
                detectBtn.disabled = false;
            })
            .catch(error => {
                showError(`Error: ${error.message}. Please try again.`);
                detectBtn.disabled = false;
            });
        }
        
        // Function to get treatment recommendations
        function getTreatmentRecommendation(disease) {
            const recommendations = {
                "Black_rot": "Remove and destroy infected leaves and fruit. Apply fungicides containing captan, myclobutanil, or mancozeb. Improve air circulation through proper pruning.",
                
                "Esca_(Black_Measles)": "There is no cure for infected vines. Remove severely infected vines, use clean pruning tools, and protect pruning wounds with fungicides or wound sealants.",
                
                "Leaf_blight_(Isariopsis_Leaf_Spot)": "Remove and destroy fallen leaves. Apply fungicides containing copper, mancozeb, or azoxystrobin. Improve air circulation through proper pruning."
            };
            
            return recommendations[disease] || "Consult with a viticulture specialist for proper diagnosis and treatment.";
        }
    }
    
    // Contact form submission
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                subject: document.getElementById('subject') ? document.getElementById('subject').value : 'General Inquiry',
                message: document.getElementById('message').value
            };
            
            // Show loading state
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            submitBtn.disabled = true;
            
            // Simulate sending data to the server
            setTimeout(() => {
                // In a real application, you would send this data to the server
                console.log('Form data:', formData);
                
                // Show success message
                const formElements = contactForm.innerHTML;
            contactForm.innerHTML = `
                <div class="success-message">
                    <i class="fas fa-check-circle"></i>
                    <h3>Message Sent!</h3>
                        <p>Thank you, ${formData.name}. We will get back to you soon.</p>
                        <button class="btn btn-sm" id="send-another">Send Another Message</button>
                </div>
            `;
                
                // Add event listener to "Send Another Message" button
                document.getElementById('send-another').addEventListener('click', () => {
                    contactForm.innerHTML = formElements;
                    // Re-attach event listener to the form
                    document.getElementById('contact-form').addEventListener('submit', arguments.callee);
                });
            }, 1500);
        });
    }
    
    // Newsletter subscription
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = newsletterForm.querySelector('input[type="email"]').value;
            const submitBtn = newsletterForm.querySelector('button[type="submit"]');
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            submitBtn.disabled = true;
            
            // Simulate sending data to the server
            setTimeout(() => {
                // In a real application, you would send this data to the server
                console.log('Newsletter subscription:', email);
                
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.className = 'newsletter-success';
                successMessage.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <p>Thank you for subscribing to our newsletter!</p>
                `;
                
                newsletterForm.parentNode.replaceChild(successMessage, newsletterForm);
            }, 1500);
        });
    }
    
    // Testimonial slider
    const testimonialSlider = document.querySelector('.testimonial-slider');
    
    if (testimonialSlider && testimonialSlider.children.length > 1) {
        // Only initialize slider if there are multiple testimonials
        const testimonials = testimonialSlider.children;
        const totalSlides = testimonials.length;
        let currentSlide = 0;
        
        // Initially show only the first two testimonials on desktop, one on mobile
        const showInitialTestimonials = () => {
            const isMobile = window.innerWidth < 768;
            const visibleCount = isMobile ? 1 : Math.min(2, totalSlides);
            
            for (let i = 0; i < totalSlides; i++) {
                if (i < visibleCount) {
                    testimonials[i].style.display = 'flex';
                } else {
                    testimonials[i].style.display = 'none';
                }
            }
        };
        
        // Call initially and on window resize
        showInitialTestimonials();
        window.addEventListener('resize', showInitialTestimonials);
        
        // Create navigation dots
        const dotsContainer = document.createElement('div');
        dotsContainer.className = 'testimonial-dots';
        
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('span');
            dot.className = i === 0 ? 'dot active' : 'dot';
            dot.addEventListener('click', () => {
                goToSlide(i);
            });
            dotsContainer.appendChild(dot);
        }
        
        // Add dots container after the slider
        testimonialSlider.parentNode.appendChild(dotsContainer);
        
        // Create navigation arrows
        const createNavArrow = (direction) => {
            const arrow = document.createElement('button');
            arrow.className = `testimonial-nav testimonial-nav-${direction}`;
            arrow.innerHTML = direction === 'prev' ? '<i class="fas fa-chevron-left"></i>' : '<i class="fas fa-chevron-right"></i>';
            arrow.addEventListener('click', () => {
                if (direction === 'prev') {
                    goToSlide(currentSlide - 1);
                } else {
                    goToSlide(currentSlide + 1);
                }
            });
            return arrow;
        };
        
        const prevArrow = createNavArrow('prev');
        const nextArrow = createNavArrow('next');
        
        testimonialSlider.parentNode.appendChild(prevArrow);
        testimonialSlider.parentNode.appendChild(nextArrow);
        
        // Function to go to a specific slide
        function goToSlide(slideIndex) {
            // Handle wrapping around
            if (slideIndex < 0) {
                slideIndex = totalSlides - 1;
            } else if (slideIndex >= totalSlides) {
                slideIndex = 0;
            }
            
            const isMobile = window.innerWidth < 768;
            const visibleCount = isMobile ? 1 : Math.min(2, totalSlides);
            
            // Hide all testimonials
            for (let i = 0; i < totalSlides; i++) {
                testimonials[i].style.display = 'none';
                dotsContainer.children[i].classList.remove('active');
            }
            
            // Show the current slide and the next one (if not mobile)
            for (let i = 0; i < visibleCount; i++) {
                const index = (slideIndex + i) % totalSlides;
                testimonials[index].style.display = 'flex';
            }
            
            // Update active dot
            dotsContainer.children[slideIndex].classList.add('active');
            
            // Update current slide
            currentSlide = slideIndex;
        }
        
        // Auto-advance slides every 5 seconds
        let slideInterval = setInterval(() => {
            goToSlide(currentSlide + 1);
        }, 5000);
        
        // Pause auto-advance on hover
        testimonialSlider.addEventListener('mouseenter', () => {
            clearInterval(slideInterval);
        });
        
        testimonialSlider.addEventListener('mouseleave', () => {
            slideInterval = setInterval(() => {
                goToSlide(currentSlide + 1);
            }, 5000);
        });
    }
}); 

// Initialize FAQ accordion functionality
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    if (faqItems.length === 0) return;
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        
        // Set initial state
        if (!item.classList.contains('active')) {
            answer.style.maxHeight = '0';
            answer.style.opacity = '0';
        } else {
            answer.style.maxHeight = answer.scrollHeight + 'px';
            answer.style.opacity = '1';
        }
        
        question.addEventListener('click', () => {
            // Toggle active class on the clicked item
            const isActive = item.classList.contains('active');
            
            // Close all items first
            faqItems.forEach(otherItem => {
                const otherAnswer = otherItem.querySelector('.faq-answer');
                otherItem.classList.remove('active');
                otherAnswer.style.maxHeight = '0';
                otherAnswer.style.opacity = '0';
            });
            
            // If the clicked item wasn't active, open it
            if (!isActive) {
                item.classList.add('active');
                answer.style.maxHeight = answer.scrollHeight + 'px';
                answer.style.opacity = '1';
                
                // Add animation to the icon
                const icon = question.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-flip');
                    setTimeout(() => {
                        icon.classList.remove('fa-flip');
                    }, 500);
                }
            }
        });
    });
} 