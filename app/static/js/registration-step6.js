document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const fileInputs = document.querySelectorAll(".file-input");
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB in bytes

    /* ==========================================
       1. Dynamically Setup UI for Validation
    ========================================== */
    fileInputs.forEach(input => {
        const documentItem = input.closest(".document-item");
        
        // A. Inject Error Block at the bottom of the item
        const errDiv = document.createElement("div");
        errDiv.className = "err-block";
        errDiv.innerHTML = '<p class="err"></p>';
        documentItem.appendChild(errDiv);
        
        // B. Inject File Name Display
        const fileNameDisplay = document.createElement("div");
        fileNameDisplay.className = "file-name-display";
        documentItem.appendChild(fileNameDisplay);
    });

    /* ==========================================
       2. Validation Helpers
    ========================================== */
    function showError(uploadBtn, errBlock, fileNameDisplay, message) {
        errBlock.classList.add("failure");
        errBlock.querySelector(".err").innerText = message;
        
        uploadBtn.classList.add("error");
        uploadBtn.classList.remove("success");
        
        fileNameDisplay.style.display = "none";
        fileNameDisplay.innerText = "";
    }

    function showSuccess(uploadBtn, errBlock, fileNameDisplay, fileName) {
        errBlock.classList.remove("failure");
        
        uploadBtn.classList.remove("error");
        uploadBtn.classList.add("success");
        
        // Show the name of the file they selected
        fileNameDisplay.innerText = "Ready to upload: " + fileName;
        fileNameDisplay.style.display = "block";
    }

    function resetValidation(uploadBtn, errBlock, fileNameDisplay) {
        errBlock.classList.remove("failure");
        uploadBtn.classList.remove("error", "success");
        fileNameDisplay.style.display = "none";
    }

    function validateFile(input) {
        // Skip validation if disabled
        if (input.disabled) return true;

        const documentItem = input.closest(".document-item");
        const uploadBtn = documentItem.querySelector(".upload-btn");
        const errBlock = documentItem.querySelector(".err-block");
        const fileNameDisplay = documentItem.querySelector(".file-name-display");

        // 1. Required Check
        if (input.files.length === 0) {
            if (input.hasAttribute("required")) {
                showError(uploadBtn, errBlock, fileNameDisplay, "This document is required.");
                return false;
            }
            // Optional and empty is fine
            resetValidation(uploadBtn, errBlock, fileNameDisplay);
            return true; 
        }

        const file = input.files[0];

        // 2. Size Check
        if (file.size > MAX_FILE_SIZE) {
            showError(uploadBtn, errBlock, fileNameDisplay, "File size must be less than 5MB.");
            input.value = ""; // Clear the file
            return false;
        }

        // 3. Type/Extension Check
        const acceptedTypes = input.getAttribute("accept");
        if (acceptedTypes) {
            const allowedExts = acceptedTypes.split(",").map(ext => ext.trim().toLowerCase());
            const fileExt = "." + file.name.split('.').pop().toLowerCase();
            
            if (!allowedExts.includes(fileExt)) {
                showError(uploadBtn, errBlock, fileNameDisplay, `Invalid format. Allowed: ${acceptedTypes}`);
                input.value = ""; // Clear the file
                return false;
            }
        }

        // Passes all checks
        showSuccess(uploadBtn, errBlock, fileNameDisplay, file.name);
        return true;
    }

    /* ==========================================
       3. Live Validation on File Select
    ========================================== */
    fileInputs.forEach(input => {
        input.addEventListener("change", function () {
            validateFile(this);
        });
    });

    /* ==========================================
       4. Form Submit Intercept
    ========================================== */
    if (form) {
        form.addEventListener("submit", function (e) {
            let valid = true;
            
            // Validate all file inputs
            fileInputs.forEach(input => {
                if (!validateFile(input)) {
                    valid = false;
                }
            });

            if (!valid) {
                e.preventDefault(); // Stop submission
                
                // Scroll smoothly to the first error
                const firstError = document.querySelector(".err-block.failure");
                if (firstError) {
                    firstError.scrollIntoView({ behavior: "smooth", block: "center" });
                }
            } else {
                // Ensure disabled fields are re-enabled so the form submits smoothly
                const disabledInputs = document.querySelectorAll(".file-input:disabled");
                disabledInputs.forEach(input => {
                    input.disabled = false;
                });
            }
        });
    }
});