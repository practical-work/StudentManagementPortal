const fullName = document.getElementById("full_name");
const email = document.getElementById("email");
const mobile = document.getElementById("mobile");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");

const input = document.querySelectorAll(".mb-3 input");
const errBlock = document.querySelectorAll(".err-block");

const nameErr = document.getElementById("name-err");
const emailErr = document.getElementById("email-err");
const mobileErr = document.getElementById("mobile-err");
const passErr = document.getElementById("pass-err");
const confirmPassErr = document.getElementById("confirm-pass-err");

const form = document.querySelector(".form-style");

const faEye = document.querySelector(".fa-eye");


if (faEye) {
    faEye.addEventListener("click", () => {

        if (password.type === "password") {
            password.type = "text";
            faEye.classList.remove("fa-eye");
            faEye.classList.add("fa-eye-slash");
        } else {
            password.type = "password";
            faEye.classList.remove("fa-eye-slash");
            faEye.classList.add("fa-eye");
        }

    });
}


// Full Name
function validateName(value) {

    value = value.trim();

    if (value === "") {
        showError(0, input[0], nameErr, "Full Name cannot be blank.");
        return false;
    }

    const letters = value.replace(/[^A-Za-z]/g, "");

    if (letters.length < 3) {
        showError(0, input[0], nameErr, "Full Name must contain at least 3 letters.");
        return false;
    }

    showSuccess(0, input[0]);
    return true;
}

// Email
function validateEmail(value) {

    value = value.trim();

    if (value === "") {
        showError(1, input[1], emailErr, "Email cannot be blank.");
        return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(value)) {
        showError(1, input[1], emailErr, "Enter a valid email address.");
        return false;
    }

    showSuccess(1, input[1]);
    return true;
}

// Mobile
function validateMobile(value) {

    value = value.trim();

    if (value === "") {
        showError(2, input[2], mobileErr, "Mobile Number cannot be blank.");
        return false;
    }

    const mobileRegex = /^[6-9]\d{9}$/;

    if (!mobileRegex.test(value)) {
        showError(2, input[2], mobileErr, "Enter a valid 10-digit mobile number.");
        return false;
    }

    showSuccess(2, input[2]);
    return true;
}

// Password
function validatePassword(value) {

    if (value === "") {
        showError(3, input[3], passErr, "Password cannot be blank.");
        if (faEye) faEye.style.color = "rgb(249,116,116)";
        return false;
    }

    const passwordRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#()_\-+=])[A-Za-z\d@$!%*?&^#()_\-+=]{6,}$/;

    if (!passwordRegex.test(value)) {
        showError(
            3,
            input[3],
            passErr,
            "Password must contain Uppercase, Lowercase, Number, Special Character and be at least 6 characters."
        );
        if (faEye) faEye.style.color = "rgb(249,116,116)";
        return false;
    }

    showSuccess(3, input[3]);
    if (faEye) faEye.style.color = "rgb(42,215,88)";
    return true;
}

// Confirm Password
function validateConfirmPassword(value) {

    if (value === "") {
        showError(4, input[4], confirmPassErr, "Confirm Password cannot be blank.");
        return false;
    }

    if (value !== password.value) {
        showError(4, input[4], confirmPassErr, "Passwords do not match.");
        return false;
    }

    showSuccess(4, input[4]);
    return true;
}


function showError(index, element, errorElement, message) {

    errBlock[index].classList.add("failure");
    errorElement.innerText = message;

    element.classList.add("error");
    element.classList.remove("success");

}

function showSuccess(index, element) {

    errBlock[index].classList.remove("failure");

    element.classList.remove("error");
    element.classList.add("success");

}


if (fullName) {
    fullName.addEventListener("input", () => {
        validateName(fullName.value);
    });
}

if (email) {
    email.addEventListener("input", () => {
        validateEmail(email.value);
    });
}

if (mobile) {
    mobile.addEventListener("input", () => {
        validateMobile(mobile.value);
    });
}

if (password) {
    password.addEventListener("input", () => {
        validatePassword(password.value);

        if (confirmPassword.value !== "") {
            validateConfirmPassword(confirmPassword.value);
        }
    });
}

if (confirmPassword) {
    confirmPassword.addEventListener("input", () => {
        validateConfirmPassword(confirmPassword.value);
    });
}


form.addEventListener("submit", function (e) {

    const nameValid = validateName(fullName.value);
    const emailValid = validateEmail(email.value);
    const mobileValid = validateMobile(mobile.value);
    const passwordValid = validatePassword(password.value);
    const confirmValid = validateConfirmPassword(confirmPassword.value);

    if (!(nameValid && emailValid && mobileValid && passwordValid && confirmValid)) {
        e.preventDefault();
    }

});