document.addEventListener("DOMContentLoaded", function () {
    const declarationCheckbox = document.getElementById("declaration");
    const submitBtn = document.getElementById("submitBtn");
    const form = document.querySelector("form");

    // 1. Initial State: Disable the submit button until the checkbox is checked
    if (declarationCheckbox && submitBtn) {
        submitBtn.disabled = !declarationCheckbox.checked;

        // Listen for changes on the checkbox
        declarationCheckbox.addEventListener("change", function () {
            submitBtn.disabled = !this.checked;
        });
    }

    // 2. Form Submission Intercept (Final Confirmation)
    if (form) {
        form.addEventListener("submit", function (e) {
            
            // Double check that the declaration is checked just in case
            if (declarationCheckbox && !declarationCheckbox.checked) {
                e.preventDefault();
                alert("Please check the declaration box to proceed.");
                // Scroll to declaration box
                declarationCheckbox.scrollIntoView({ behavior: "smooth", block: "center" });
                return;
            }

            // Show confirmation popup
            const confirmationMessage = 
                "Are you absolutely sure you want to submit your application?\n\n" +
                "Once submitted, you will NOT be able to modify your personal details, " +
                "qualifications, or uploaded documents.";

            const userConfirmed = confirm(confirmationMessage);

            if (!userConfirmed) {
                // If user clicks "Cancel", stop the form from submitting
                e.preventDefault();
            } else {
                // Optional: Change button text to indicate processing
                if (submitBtn) {
                    submitBtn.innerText = "Submitting...";
                    submitBtn.style.pointerEvents = "none";
                }
            }
        });
    }
});