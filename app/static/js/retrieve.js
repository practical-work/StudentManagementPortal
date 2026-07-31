// ==========================
// Elements
// ==========================

const searchType = document.getElementById("searchType");
const searchValue = document.getElementById("searchValue");
const otp = document.getElementById("entered_otp");

const forms = document.querySelectorAll(".form-style");

const errBlocks = document.querySelectorAll(".err-block");
const valueErr = document.getElementById("value-err");
const otpErr = document.getElementById("otp-err");

// ==========================
// Helper Functions
// ==========================

function showError(index, input, errElement, message){

    errBlocks[index].classList.add("failure");

    errElement.innerText = message;

    input.classList.add("error");
    input.classList.remove("success");

}

function showSuccess(index, input, errElement){

    errBlocks[index].classList.remove("failure");

    errElement.innerText = "";

    input.classList.remove("error");
    input.classList.add("success");

}

// ==========================
// Email Validation
// ==========================

function validateEmail(value){

    value = value.trim();

    if(value === ""){

        showError(
            0,
            searchValue,
            valueErr,
            "Email Address cannot be blank."
        );

        return false;

    }

    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(!regex.test(value)){

        showError(
            0,
            searchValue,
            valueErr,
            "Enter a valid Email Address."
        );

        return false;

    }

    showSuccess(0,searchValue,valueErr);

    return true;

}

// ==========================
// Mobile Validation
// ==========================

function validateMobile(value){

    value = value.trim();

    if(value === ""){

        showError(
            0,
            searchValue,
            valueErr,
            "Mobile Number cannot be blank."
        );

        return false;

    }

    const regex = /^[6-9]\d{9}$/;

    if(!regex.test(value)){

        showError(
            0,
            searchValue,
            valueErr,
            "Enter a valid 10-digit Mobile Number."
        );

        return false;

    }

    showSuccess(0,searchValue,valueErr);

    return true;

}

// ==========================
// OTP Validation
// ==========================

function validateOTP(value){

    value = value.trim();

    if(value === ""){

        showError(
            1,
            otp,
            otpErr,
            "OTP cannot be blank."
        );

        return false;

    }

    if(!/^\d{6}$/.test(value)){

        showError(
            1,
            otp,
            otpErr,
            "OTP must contain exactly 6 digits."
        );

        return false;

    }

    showSuccess(1,otp,otpErr);

    return true;

}

// ==========================
// Live Validation
// ==========================

if(searchValue){

    searchValue.addEventListener("input",()=>{

        if(searchType.value==="email"){

            validateEmail(searchValue.value);

        }else{

            validateMobile(searchValue.value);

        }

    });

}

if(searchType){

    searchType.addEventListener("change",()=>{

        searchValue.value = "";

        searchValue.classList.remove("error","success");

        if(valueErr){

            valueErr.innerText = "";

        }

        if(errBlocks[0]){

            errBlocks[0].classList.remove("failure");

        }

    });

}

if(otp){

    otp.addEventListener("input",()=>{

        validateOTP(otp.value);

    });

}

// ==========================
// Form Submit Validation
// ==========================

forms.forEach(form=>{

    form.addEventListener("submit",function(e){

        let valid = true;

        // Search Form
        if(searchValue){

            if(searchType.value==="email"){

                valid = validateEmail(searchValue.value);

            }else{

                valid = validateMobile(searchValue.value);

            }

        }

        // OTP Form
        if(otp){

            valid = validateOTP(otp.value) && valid;

        }

        if(!valid){

            e.preventDefault();

        }

    });

});