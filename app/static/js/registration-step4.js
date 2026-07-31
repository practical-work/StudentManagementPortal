document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const checkbox = document.getElementById("sameAddress");

    // Mapping Permanent fields to Correspondence fields
    const fieldsMap = [
        { perm: "permanent_address", corr: "correspondence_address", type: "text" },
        { perm: "permanent_state", corr: "correspondence_state", type: "text" },
        { perm: "permanent_district", corr: "correspondence_district", type: "text" },
        { perm: "permanent_city", corr: "correspondence_city", type: "text" },
        { perm: "permanent_pincode", corr: "correspondence_pincode", type: "pincode" }
    ];

    /* ==========================================
       1. Dynamically Inject Error Blocks
       (Saves you from having to rewrite the HTML!)
    ========================================== */
    const allInputs = document.querySelectorAll(".grid input, .grid textarea");
    allInputs.forEach(input => {
        // Create the error block under every input
        const errDiv = document.createElement("div");
        errDiv.className = "err-block";
        errDiv.innerHTML = '<p class="err"></p>';
        input.parentNode.appendChild(errDiv);
    });

    /* ==========================================
       2. Checkbox Sync Logic
    ========================================== */
    function syncFields() {
        if (checkbox.checked) {
            fieldsMap.forEach(field => {
                const permInput = document.querySelector(`[name="${field.perm}"]`);
                const corrInput = document.querySelector(`[name="${field.corr}"]`);
                
                // Copy value and disable
                corrInput.value = permInput.value;
                corrInput.disabled = true;
                
                // Clear any validation errors visually
                showSuccess(corrInput, corrInput.nextElementSibling);
            });
        } else {
            fieldsMap.forEach(field => {
                const corrInput = document.querySelector(`[name="${field.corr}"]`);
                
                // Remove value and enable
                corrInput.disabled = false;
                corrInput.value = ""; 
                
                // Reset validation colors
                corrInput.classList.remove("success", "error");
                corrInput.nextElementSibling.classList.remove("failure");
            });
        }
    }

    // When checkbox is clicked
    if (checkbox) {
        checkbox.addEventListener("change", syncFields);
    }

    // Live update correspondence if user types in permanent while checked
    fieldsMap.forEach(field => {
        const permInput = document.querySelector(`[name="${field.perm}"]`);
        permInput.addEventListener("input", () => {
            if (checkbox && checkbox.checked) {
                const corrInput = document.querySelector(`[name="${field.corr}"]`);
                corrInput.value = permInput.value;
            }
        });
    });

    /* ==========================================
       3. Validation Helpers
    ========================================== */
    function showError(element, errBlock, message) {
        errBlock.classList.add("failure");
        errBlock.querySelector(".err").innerText = message;
        element.classList.add("error");
        element.classList.remove("success");
    }

    function showSuccess(element, errBlock) {
        errBlock.classList.remove("failure");
        element.classList.remove("error");
        element.classList.add("success");
    }

    function validateField(input, type) {
        // Do not throw visual errors if the field is disabled by the checkbox
        if (input.disabled) return true;

        const value = input.value.trim();
        const errBlock = input.nextElementSibling;

        if (value === "") {
            showError(input, errBlock, "This field cannot be blank.");
            return false;
        }

        if (type === "pincode") {
            if (!/^[0-9]{6}$/.test(value)) {
                showError(input, errBlock, "Enter a valid 6-digit Pincode.");
                return false;
            }
        } else {
            if (value.length < 2) {
                showError(input, errBlock, "Enter valid information.");
                return false;
            }
        }

        showSuccess(input, errBlock);
        return true;
    }

    /* ==========================================
       4. Attach Live Validation Events
    ========================================== */
    allInputs.forEach(input => {
        input.addEventListener("input", function () {
            const isPincode = input.name.includes("pincode");
            validateField(input, isPincode ? "pincode" : "text");
        });
    });

    /* ==========================================
       5. Form Submit Intercept
    ========================================== */
    if (form) {
        form.addEventListener("submit", function (e) {
            let valid = true;
            
            // Validate every field
            fieldsMap.forEach(field => {
                const permInput = document.querySelector(`[name="${field.perm}"]`);
                const corrInput = document.querySelector(`[name="${field.corr}"]`);

                if (!validateField(permInput, field.perm.includes("pincode") ? "pincode" : "text")) valid = false;
                if (!validateField(corrInput, field.corr.includes("pincode") ? "pincode" : "text")) valid = false;
            });

            if (!valid) {
                e.preventDefault(); // Stop submission
                
                // Scroll to the first error smoothly
                const firstError = document.querySelector(".error");
                if (firstError) {
                    firstError.scrollIntoView({ behavior: "smooth", block: "center" });
                }
            } else {
                // IMPORTANT FIX: 
                // Browsers do NOT send `disabled` inputs to the backend in POST requests.
                // We must temporarily remove the disabled attribute so Flask gets the data!
                fieldsMap.forEach(field => {
                    const corrInput = document.querySelector(`[name="${field.corr}"]`);
                    corrInput.disabled = false; 
                });
            }
        });
    }
});