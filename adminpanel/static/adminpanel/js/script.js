/* ================================
   ADMIN PANEL - ENHANCED JAVASCRIPT
   Professional Interactions & Animations
================================ */

/* === INITIALIZATION === */
document.addEventListener("DOMContentLoaded", () => {
    initializeApp();
});

function initializeApp() {
    // Fade in page
    document.body.classList.add("fade-in");
    
    // Initialize all features
    highlightActiveNavLink();
    initializeTableSearch();
    initializeFormValidation();
    initializeTooltips();
    initializeCardAnimations();
    initializeModalHandlers();
    initializeButtonEffects();
    autoHideMessages();
    initializeTableEnhancements();
}

/* === ACTIVE NAVIGATION HIGHLIGHT === */
function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll("aside a");
    
    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
}

/* === MODAL HANDLING === */
function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    
    // Add fade-in animation
    modal.style.animation = "fadeIn 0.3s ease-out";
    
    // Prevent body scroll when modal is open
    document.body.style.overflow = "hidden";
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    
    // Add fade-out animation
    modal.style.animation = "fadeOut 0.3s ease-out";
    
    setTimeout(() => {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.style.overflow = "auto";
    }, 300);
}

function initializeModalHandlers() {
    // Close modal when clicking outside
    window.addEventListener("click", (e) => {
        document.querySelectorAll(".modal").forEach((modal) => {
            if (e.target === modal) {
                const modalId = modal.getAttribute("id");
                closeModal(modalId);
            }
        });
    });
    
    // Close modal with Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            document.querySelectorAll(".modal").forEach((modal) => {
                if (!modal.classList.contains("hidden")) {
                    const modalId = modal.getAttribute("id");
                    closeModal(modalId);
                }
            });
        }
    });
}

/* === BUTTON EFFECTS === */
function initializeButtonEffects() {
    // Ripple effect on button click
    document.querySelectorAll("button, .btn").forEach((button) => {
        button.addEventListener("click", function(e) {
            const ripple = document.createElement("span");
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + "px";
            ripple.style.left = x + "px";
            ripple.style.top = y + "px";
            ripple.classList.add("ripple");
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
        
        // Press animation
        button.addEventListener("mousedown", function() {
            this.style.transform = "scale(0.98)";
        });
        
        button.addEventListener("mouseup", function() {
            this.style.transform = "scale(1)";
        });
        
        button.addEventListener("mouseleave", function() {
            this.style.transform = "scale(1)";
        });
    });
}

/* === TABLE SEARCH FILTER === */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    const filterValue = input.value.toLowerCase().trim();
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.getElementsByTagName("tr");
    let visibleCount = 0;
    
    Array.from(rows).forEach((row, index) => {
        // Skip header row
        if (index === 0 && row.parentElement.tagName === "THEAD") return;
        
        const text = row.innerText.toLowerCase();
        const shouldShow = text.includes(filterValue);
        
        row.style.display = shouldShow ? "" : "none";
        
        if (shouldShow) {
            visibleCount++;
            // Staggered animation
            row.style.animation = `fadeIn 0.3s ease-out ${index * 0.05}s both`;
        }
    });
    
    // Show "no results" message if needed
    showNoResultsMessage(table, visibleCount, filterValue);
}

function initializeTableSearch() {
    const searchInputs = document.querySelectorAll("input[type='search'], input[data-table-search]");
    
    searchInputs.forEach(input => {
        input.addEventListener("input", debounce(() => {
            const tableId = input.getAttribute("data-table-id");
            if (tableId) {
                filterTable(input.id, tableId);
            }
        }, 300));
    });
}

function showNoResultsMessage(table, count, searchTerm) {
    const existingMessage = table.parentElement.querySelector(".no-results-message");
    
    if (count === 0 && searchTerm) {
        if (!existingMessage) {
            const message = document.createElement("div");
            message.className = "no-results-message text-center p-6 text-gray-500";
            message.innerHTML = `
                <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="font-semibold">No results found</p>
                <p class="text-sm">Try adjusting your search term</p>
            `;
            table.parentElement.appendChild(message);
        }
    } else if (existingMessage) {
        existingMessage.remove();
    }
}

/* === FORM VALIDATION === */
function initializeFormValidation() {
    const forms = document.querySelectorAll("form");
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll("input[required], select[required], textarea[required]");
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener("blur", () => validateInput(input));
            input.addEventListener("input", () => {
                if (input.classList.contains("invalid")) {
                    validateInput(input);
                }
            });
        });
        
        // Form submission validation
        form.addEventListener("submit", (e) => {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification("Please fill in all required fields correctly", "error");
            }
        });
    });
}

function validateInput(input) {
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = "";
    
    // Check if required field is empty
    if (input.hasAttribute("required") && !value) {
        isValid = false;
        errorMessage = "This field is required";
    }
    
    // Email validation
    if (input.type === "email" && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = "Please enter a valid email address";
        }
    }
    
    // Password validation
    if (input.type === "password" && value && value.length < 6) {
        isValid = false;
        errorMessage = "Password must be at least 6 characters";
    }
    
    // Update UI
    if (isValid) {
        input.classList.remove("invalid");
        input.style.borderColor = "#10b981";
        removeErrorMessage(input);
    } else {
        input.classList.add("invalid");
        input.style.borderColor = "#ef4444";
        showErrorMessage(input, errorMessage);
    }
    
    return isValid;
}

function showErrorMessage(input, message) {
    removeErrorMessage(input);
    
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message text-sm text-red-600 mt-1";
    errorDiv.textContent = message;
    errorDiv.style.animation = "slideIn 0.3s ease-out";
    
    input.parentElement.appendChild(errorDiv);
}

function removeErrorMessage(input) {
    const existingError = input.parentElement.querySelector(".error-message");
    if (existingError) {
        existingError.remove();
    }
}

/* === TOOLTIPS === */
function initializeTooltips() {
    const elementsWithTooltip = document.querySelectorAll("[data-tooltip]");
    
    elementsWithTooltip.forEach(element => {
        element.addEventListener("mouseenter", (e) => {
            const tooltip = createTooltip(element.getAttribute("data-tooltip"));
            document.body.appendChild(tooltip);
            positionTooltip(tooltip, e.target);
        });
        
        element.addEventListener("mouseleave", () => {
            const tooltip = document.querySelector(".tooltip");
            if (tooltip) tooltip.remove();
        });
    });
}

function createTooltip(text) {
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(14, 77, 146, 0.95);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 13px;
        z-index: 10000;
        pointer-events: none;
        animation: fadeIn 0.2s ease-out;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    `;
    return tooltip;
}

function positionTooltip(tooltip, target) {
    const rect = target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + "px";
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + "px";
}

/* === CARD ANIMATIONS === */
function initializeCardAnimations() {
    const cards = document.querySelectorAll(".glass, .stat-card");
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.animation = `fadeIn 0.6s ease-out forwards`;
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => {
        card.style.opacity = "0";
        observer.observe(card);
    });
}

/* === AUTO-HIDE MESSAGES === */
function autoHideMessages() {
    const messages = document.querySelectorAll(".message, .alert");
    
    messages.forEach(message => {
        setTimeout(() => {
            message.style.animation = "fadeOut 0.5s ease-out forwards";
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
}

/* === NOTIFICATION SYSTEM === */
function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification message message-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        z-index: 10000;
        min-width: 300px;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = "fadeOut 0.3s ease-out";
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/* === TABLE ENHANCEMENTS === */
function initializeTableEnhancements() {
    const tables = document.querySelectorAll("table");
    
    tables.forEach(table => {
        // Add hover effect class
        const rows = table.querySelectorAll("tbody tr");
        rows.forEach(row => {
            row.addEventListener("mouseenter", function() {
                this.style.transform = "scale(1.01)";
            });
            row.addEventListener("mouseleave", function() {
                this.style.transform = "scale(1)";
            });
        });
        
        // Make table responsive
        if (!table.parentElement.classList.contains("overflow-x-auto")) {
            const wrapper = document.createElement("div");
            wrapper.className = "overflow-x-auto";
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
}

/* === UTILITY FUNCTIONS === */

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Smooth scroll to element
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification("Copied to clipboard!", "success");
    }).catch(() => {
        showNotification("Failed to copy", "error");
    });
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Confirm action
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/* === LOADING SPINNER === */
function showLoadingSpinner() {
    const spinner = document.createElement("div");
    spinner.id = "loading-spinner";
    spinner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;
    spinner.innerHTML = `
        <div style="
            width: 50px;
            height: 50px;
            border: 4px solid #e2e8f0;
            border-top-color: #1e88e5;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        "></div>
    `;
    document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
    const spinner = document.getElementById("loading-spinner");
    if (spinner) spinner.remove();
}

/* === KEYBOARD SHORTCUTS === */
document.addEventListener("keydown", (e) => {
    // Ctrl/Cmd + K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        const searchInput = document.querySelector("input[type='search']");
        if (searchInput) searchInput.focus();
    }
    
    // Ctrl/Cmd + /: Show keyboard shortcuts
    if ((e.ctrlKey || e.metaKey) && e.key === "/") {
        e.preventDefault();
        showKeyboardShortcuts();
    }
});

function showKeyboardShortcuts() {
    showNotification("Ctrl+K: Search | Esc: Close modals", "info");
}

/* === ADD RIPPLE ANIMATION STYLES === */
const style = document.createElement("style");
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
    
    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
    
    .invalid {
        border-color: #ef4444 !important;
    }
`;
document.head.appendChild(style);

/* === EXPORT FUNCTIONS FOR GLOBAL USE === */
window.openModal = openModal;
window.closeModal = closeModal;
window.filterTable = filterTable;
window.showNotification = showNotification;
window.copyToClipboard = copyToClipboard;
window.confirmAction = confirmAction;
window.showLoadingSpinner = showLoadingSpinner;
window.hideLoadingSpinner = hideLoadingSpinner;