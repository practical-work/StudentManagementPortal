let application_no = document.getElementById('application_no');
let password = document.getElementById('password');
let input = document.querySelectorAll('.mb-3 input');
let faEye = document.querySelector('.fa-eye');
let errBlock = document.querySelectorAll('.err-block');
let err = document.querySelectorAll('.err');
let passErr = document.getElementById('pass-err');
let appErr = document.getElementById('app-err');
let submitBtn = document.querySelector('.btn-primary');
let form = document.querySelector('.form-style')

faEye.addEventListener("click",()=>{
  passType=password.getAttribute("type")
  if(passType === "password"){
     password.setAttribute("type","text")
     faEye.classList.remove("fa-eye")
     faEye.classList.add("fa-eye-slash")
  }else{
     password.setAttribute("type","password")
     faEye.classList.remove("fa-eye-slash")
     faEye.classList.add("fa-eye")
  }
});

// Form validation

function ValidateApplicationNo(value){
   if(!value){
      errBlock[0].classList.add("failure");
      appErr.innerText = 'Application no. cannot be blank.';
      input[0].classList.add("error");
      input[0].classList.remove("success")
      return false;
   }
   else if(value.length < 13){
      errBlock[0].classList.add("failure");
      appErr.innerText = 'Application no. must contain atleast 13 characters.';
      input[0].classList.add("error");
      input[0].classList.remove("success")
      return false;
   }
   else{
      errBlock[0].classList.remove("failure");
      input[0].classList.remove("error");
      input[0].classList.add("success");
      return true;
   }
};


function ValidatePassword(value){
   if(!value){
      errBlock[1].classList.add("failure");
      passErr.innerText = 'Password cannot be blank.';
      input[1].classList.add("error");
      input[1].classList.remove("success");
      faEye.style.color = "rgb(249, 116, 116)";
      return false;
   }else{
      errBlock[1].classList.remove("failure");
      input[1].classList.remove("error");
      input[1].classList.add("success");
      faEye.style.color = "rgb(42, 215, 88)";
      return true;
   }
};


application_no.addEventListener("input", () => {
    ValidateApplicationNo(application_no.value.trim());
});

password.addEventListener("input", () => {
    ValidatePassword(password.value.trim());
});

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const appValid = ValidateApplicationNo(application_no.value.trim());
    const passValid = ValidatePassword(password.value.trim());

    if (appValid && passValid) {
        form.submit(); 
    }
});
