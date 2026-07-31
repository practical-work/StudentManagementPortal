// ===========================
// Elements
// ===========================

const applicationNo = document.getElementById("application_no");
const email = document.getElementById("email");
const otp = document.getElementById("entered_otp");

const form = document.querySelector(".form-style");

const inputs = document.querySelectorAll(".mb-3 input");
const errBlocks = document.querySelectorAll(".err-block");

// ===========================
// Create Error Boxes
// ===========================

document.querySelectorAll(".mb-3").forEach(div => {

    if (!div.querySelector(".err-block")) {

        div.insertAdjacentHTML(
            "beforeend",
            `<div class="err-block">
                <p class="err"></p>
            </div>`
        );

    }

});

const newErrBlocks = document.querySelectorAll(".err-block");
const errs = document.querySelectorAll(".err");

// ===========================
// Helper Functions
// ===========================

function showError(index, input, message){

    newErrBlocks[index].classList.add("failure");

    errs[index].innerText = message;

    input.classList.add("error");
    input.classList.remove("success");

}

function showSuccess(index, input){

    newErrBlocks[index].classList.remove("failure");

    errs[index].innerText = "";

    input.classList.remove("error");
    input.classList.add("success");

}

// ===========================
// Application Number
// ===========================

function validateApplicationNumber(value){

    value = value.trim();

    if(value===""){

        showError(
            0,
            applicationNo,
            "Application Number cannot be blank."
        );

        return false;

    }

    if(value.length < 8){

        showError(
            0,
            applicationNo,
            "Enter a valid Application Number."
        );

        return false;

    }

    showSuccess(0,applicationNo);

    return true;

}

// ===========================
// Email
// ===========================

function validateEmail(value){

    value = value.trim();

    if(value===""){

        showError(
            1,
            email,
            "Email Address cannot be blank."
        );

        return false;

    }

    const regex=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(!regex.test(value)){

        showError(
            1,
            email,
            "Enter a valid Email Address."
        );

        return false;

    }

    showSuccess(1,email);

    return true;

}

// ===========================
// OTP
// ===========================

function validateOTP(value){

    value=value.trim();

    if(value===""){

        showError(
            2,
            otp,
            "OTP cannot be blank."
        );

        return false;

    }

    if(!/^\d{6}$/.test(value)){

        showError(
            2,
            otp,
            "OTP must contain exactly 6 digits."
        );

        return false;

    }

    showSuccess(2,otp);

    return true;

}

// ===========================
// Live Validation
// ===========================

if(applicationNo){

    applicationNo.addEventListener("input",()=>{

        validateApplicationNumber(applicationNo.value);

    });

}

if(email){

    email.addEventListener("input",()=>{

        validateEmail(email.value);

    });

}

if(otp){

    otp.addEventListener("input",()=>{

        validateOTP(otp.value);

    });

}

// ===========================
// Submit Validation
// ===========================

document.querySelectorAll(".form-style").forEach(form=>{

    form.addEventListener("submit",function(e){

        let valid=true;

        if(applicationNo && !applicationNo.disabled){

            valid &= validateApplicationNumber(applicationNo.value);
            valid &= validateEmail(email.value);

        }

        if(otp){

            valid &= validateOTP(otp.value);

        }

        if(!valid){

            e.preventDefault();

        }

    });

});