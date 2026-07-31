const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");

const togglePassword = document.getElementById("togglePassword");
const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");

const passErr = document.getElementById("pass-err");
const confirmErr = document.getElementById("confirm-pass-err");

const errBlocks = document.querySelectorAll(".err-block");

const form = document.querySelector(".form-style");

// Toggle Password

function toggle(input, icon){

    if(input.type==="password"){

        input.type="text";
        icon.classList.replace("fa-eye","fa-eye-slash");

    }else{

        input.type="password";
        icon.classList.replace("fa-eye-slash","fa-eye");

    }

}

togglePassword.addEventListener("click",()=>toggle(password,togglePassword));
toggleConfirmPassword.addEventListener("click",()=>toggle(confirmPassword,toggleConfirmPassword));

// Validation

function validatePassword(){

    const value=password.value.trim();

    const regex=/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#])[A-Za-z\d@$!%*?&^#]{6,}$/;

    if(value===""){

        errBlocks[0].classList.add("failure");
        passErr.innerText="Password cannot be blank.";

        password.classList.add("error");
        password.classList.remove("success");

        return false;

    }

    if(!regex.test(value)){

        errBlocks[0].classList.add("failure");
        passErr.innerText="Minimum 6 characters with uppercase, lowercase, number and special character.";

        password.classList.add("error");
        password.classList.remove("success");

        return false;

    }

    errBlocks[0].classList.remove("failure");

    password.classList.remove("error");
    password.classList.add("success");

    return true;

}

function validateConfirmPassword(){

    const value=confirmPassword.value.trim();

    if(value===""){

        errBlocks[1].classList.add("failure");
        confirmErr.innerText="Confirm Password cannot be blank.";

        confirmPassword.classList.add("error");
        confirmPassword.classList.remove("success");

        return false;

    }

    if(value!==password.value){

        errBlocks[1].classList.add("failure");
        confirmErr.innerText="Passwords do not match.";

        confirmPassword.classList.add("error");
        confirmPassword.classList.remove("success");

        return false;

    }

    errBlocks[1].classList.remove("failure");

    confirmPassword.classList.remove("error");
    confirmPassword.classList.add("success");

    return true;

}

// Live Validation

password.addEventListener("input",validatePassword);

confirmPassword.addEventListener("input",validateConfirmPassword);

// Submit

form.addEventListener("submit",function(e){

    const p=validatePassword();
    const c=validateConfirmPassword();

    if(!(p && c)){

        e.preventDefault();

    }

});