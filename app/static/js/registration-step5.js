document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const toggles = document.querySelectorAll(".toggle");

    // Fields that should ALWAYS be required
    const requiredCoreFields = [
        "father_occupation", 
        "mother_occupation", 
        "domicile_status", 
        "domicile_state", 
        "marital_status"
    ];

    /* ==========================================
       1. Dynamically Inject Error Blocks
    ========================================== */
    const allFields = document.querySelectorAll("input[type='text'], select, textarea");
    
    allFields.forEach(field => {
        // Skip hidden fields like CSRF token
        if (field.type === "hidden" || field.name === "csrf_token") return;
        
        const errDiv = document.createElement("div");
        errDiv.className = "err-block";
        errDiv.innerHTML = '<p class="err"></p>';
        
        // Insert the error block directly after the input field
        field.parentNode.insertBefore(errDiv, field.nextSibling);
    });

    /* ==========================================
       2. Validation Helpers
    ========================================== */
    function showError(element, message) {
        const errBlock = element.nextElementSibling;
        if (errBlock && errBlock.classList.contains("err-block")) {
            errBlock.classList.add("failure");
            errBlock.querySelector(".err").innerText = message;
        }
        element.classList.add("error");
        element.classList.remove("success");
    }

    function showSuccess(element) {
        const errBlock = element.nextElementSibling;
        if (errBlock && errBlock.classList.contains("err-block")) {
            errBlock.classList.remove("failure");
        }
        element.classList.remove("error");
        element.classList.add("success");
    }

    function validateField(field) {
        // Don't validate if it's disabled in View Mode
        if (field.readOnly || (field.disabled && !field.classList.contains('toggle'))) {
            return true;
        }

        const value = field.value.trim();
        const hiddenParent = field.closest(".hidden-box");
        
        // Determine if this specific field is required
        // It's required IF it's in our core list OR if it's inside a visible hidden-box
        let isRequired = requiredCoreFields.includes(field.name);
        if (hiddenParent && hiddenParent.style.display === "block") {
            isRequired = true;
        }

        // If it's inside a hidden box that is currently hidden, skip validation
        if (hiddenParent && hiddenParent.style.display !== "block") {
            return true; 
        }

        // Blank Check
        if (isRequired && value === "") {
            showError(field, "This field is required.");
            return false;
        }

        // Length Check for text inputs
        if (value !== "" && field.type === "text" && value.length < 2) {
            showError(field, "Please enter valid information.");
            return false;
        }

        // If it has a value and passes checks, it's a success
        if (value !== "") {
            showSuccess(field);
        } else {
            // If it's optional (like guardian occupation) and blank, just leave it neutral
            field.classList.remove("error", "success");
            const errBlock = field.nextElementSibling;
            if (errBlock) errBlock.classList.remove("failure");
        }

        return true;
    }

    /* ==========================================
       3. Live Validation Events
    ========================================== */
    allFields.forEach(field => {
        field.addEventListener("input", () => validateField(field));
        field.addEventListener("change", () => validateField(field));
    });

    /* ==========================================
       4. Toggle Logic (Yes/No Dropdowns)
    ========================================== */
    toggles.forEach(toggle => {
        toggle.addEventListener("change", function () {
            // Find the hidden box associated with this toggle
            const hiddenBox = this.parentElement.querySelector(".hidden-box");
            
            if (hiddenBox) {
                if (this.value === "yes") {
                    hiddenBox.style.display = "block";
                } else {
                    hiddenBox.style.display = "none";
                    
                    // Clear values and remove error borders when hidden
                    const inputs = hiddenBox.querySelectorAll("input, select, textarea");
                    inputs.forEach(input => {
                        input.value = "";
                        input.classList.remove("error", "success");
                        const err = input.nextElementSibling;
                        if (err && err.classList.contains("err-block")) {
                            err.classList.remove("failure");
                        }
                    });
                }
            }
        });
    });

    /* ==========================================
       5. Form Submit Intercept
    ========================================== */
    if (form) {
        form.addEventListener("submit", function (e) {
            let valid = true;
            
            // Re-validate every field before submission
            allFields.forEach(field => {
                if (!validateField(field)) {
                    valid = false;
                }
            });

            if (!valid) {
                e.preventDefault(); // Stop submission
                
                // Scroll smoothly to the first error
                const firstError = document.querySelector(".error");
                if (firstError) {
                    firstError.scrollIntoView({ behavior: "smooth", block: "center" });
                }
            } else {
                // IMPORTANT: Browsers don't send `disabled` select fields. 
                // Enable all toggles/selects right before submit so Flask receives the data.
                const disabledSelects = document.querySelectorAll("select:disabled");
                disabledSelects.forEach(select => {
                    select.disabled = false;
                });
            }
        });
    }
});