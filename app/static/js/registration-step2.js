/* ===========================
   Elements
=========================== */

const form = document.querySelector(".form-style");

const firstName = document.getElementById("first_name");
const middleName = document.getElementById("middle_name");
const lastName = document.getElementById("last_name");

const gender = document.getElementById("gender_id");
const dob = document.getElementById("date_of_birth");

const bloodGroup = document.getElementById("blood_group_id");

const category = document.getElementById("category_id");
const religion = document.getElementById("religion_id");
const nationality = document.getElementById("nationality_id");

const aadhaar = document.getElementById("aadhaar_no");

const alternateEmail = document.getElementById("alternate_email");
const alternateMobile = document.getElementById("alternate_mobile");

const fatherName = document.getElementById("father_name");
const fatherMobile = document.getElementById("father_mobile");

const motherName = document.getElementById("mother_name");
const motherMobile = document.getElementById("mother_mobile");

const guardianName = document.getElementById("guardian_name");
const guardianMobile = document.getElementById("guardian_mobile");


const inputs = document.querySelectorAll(".form-control");
const errBlock = document.querySelectorAll(".err-block");


/* ===========================
   Error Elements
=========================== */

const firstNameErr = document.getElementById("first-name-err");
const middleNameErr = document.getElementById("middle-name-err");
const lastNameErr = document.getElementById("last-name-err");

const genderErr = document.getElementById("gender-err");
const dobErr = document.getElementById("dob-err");

const bloodGroupErr = document.getElementById("blood-group-err");

const categoryErr = document.getElementById("category-err");
const religionErr = document.getElementById("religion-err");
const nationalityErr = document.getElementById("nationality-err");

const aadhaarErr = document.getElementById("aadhaar-err");

const alternateEmailErr = document.getElementById("alternate-email-err");
const alternateMobileErr = document.getElementById("alternate-mobile-err");

const fatherNameErr = document.getElementById("father-name-err");
const fatherMobileErr = document.getElementById("father-mobile-err");

const motherNameErr = document.getElementById("mother-name-err");
const motherMobileErr = document.getElementById("mother-mobile-err");

const guardianNameErr = document.getElementById("guardian-name-err");
const guardianMobileErr = document.getElementById("guardian-mobile-err");


/* ===========================
   Common Functions
=========================== */

function showError(index, element, errorElement, message){

    errBlock[index].classList.add("failure");

    errorElement.innerText = message;

    element.classList.add("error");
    element.classList.remove("success");

}


function showSuccess(index, element){

    errBlock[index].classList.remove("failure");

    element.classList.remove("error");
    element.classList.add("success");

}


/* ===========================
   First Name
=========================== */

function validateFirstName(value){

    value = value.trim();

    if(value === ""){
        showError(0, firstName, firstNameErr, "First Name cannot be blank.");
        return false;
    }

    const letters = value.replace(/[^A-Za-z]/g,"");

    if(letters.length < 2){
        showError(0, firstName, firstNameErr, "Enter a valid First Name.");
        return false;
    }

    showSuccess(0, firstName);
    return true;

}


/* ===========================
   Middle Name (Optional)
=========================== */

function validateMiddleName(value){

    value = value.trim();

    if(value === ""){
        showSuccess(1, middleName);
        return true;
    }

    const letters = value.replace(/[^A-Za-z]/g,"");

    if(letters.length < 2){
        showError(1, middleName, middleNameErr, "Enter a valid Middle Name.");
        return false;
    }

    showSuccess(1, middleName);
    return true;

}


/* ===========================
   Last Name
=========================== */

function validateLastName(value){

    value = value.trim();

    if(value === ""){
        showSuccess(2, lastName);
        return true;
    }

    const letters = value.replace(/[^A-Za-z]/g,"");

    if(letters.length < 2){
        showError(
            2,
            lastName,
            lastNameErr,
            "Enter a valid Last Name."
        );
        return false;
    }

    showSuccess(2, lastName);
    return true;

}

/* ===========================
   Gender
=========================== */

function validateGender(value){

    if(value === ""){
        showError(3, gender, genderErr, "Please select Gender.");
        return false;
    }

    showSuccess(3, gender);
    return true;

}


/* ===========================
   Date of Birth
=========================== */

function validateDOB(value){

    if(value === ""){
        showError(4, dob, dobErr, "Date of Birth is required.");
        return false;
    }

    const birthDate = new Date(value);
    const today = new Date();

    if(birthDate > today){
        showError(4, dob, dobErr, "Date of Birth cannot be in the future.");
        return false;
    }

    showSuccess(4, dob);
    return true;

}


/* ===========================
   Blood Group (Optional)
=========================== */

function validateBloodGroup(){

    showSuccess(5, bloodGroup);
    return true;

}


/* ===========================
   Category
=========================== */

function validateCategory(value){

    if(value === ""){
        showError(6, category, categoryErr, "Please select Category.");
        return false;
    }

    showSuccess(6, category);
    return true;

}


/* ===========================
   Religion
=========================== */

function validateReligion(value){

    if(value === ""){
        showError(7, religion, religionErr, "Please select Religion.");
        return false;
    }

    showSuccess(7, religion);
    return true;

}


/* ===========================
   Nationality
=========================== */

function validateNationality(value){

    if(value === ""){
        showError(8, nationality, nationalityErr, "Please select Nationality.");
        return false;
    }

    showSuccess(8, nationality);
    return true;

}


/* ===========================
   Aadhaar Number
=========================== */

function validateAadhaar(value){

    value = value.trim();

    if(value === ""){
        showError(9, aadhaar, aadhaarErr, "Aadhaar Number cannot be blank.");
        return false;
    }

    const aadhaarRegex = /^[0-9]{12}$/;

    if(!aadhaarRegex.test(value)){
        showError(9, aadhaar, aadhaarErr, "Enter a valid 12-digit Aadhaar Number.");
        return false;
    }

    showSuccess(9, aadhaar);
    return true;

}

/* ===========================
   Alternate Email (Optional)
=========================== */

function validateAlternateEmail(value){

    value = value.trim();

    if(value === ""){
        showSuccess(10, alternateEmail);
        return true;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(!emailRegex.test(value)){
        showError(
            10,
            alternateEmail,
            alternateEmailErr,
            "Enter a valid Alternate Email."
        );
        return false;
    }

    showSuccess(10, alternateEmail);
    return true;

}


/* ===========================
   Alternate Mobile (Optional)
=========================== */

function validateAlternateMobile(value){

    value = value.trim();

    if(value === ""){
        showSuccess(11, alternateMobile);
        return true;
    }

    const mobileRegex = /^[6-9]\d{9}$/;

    if(!mobileRegex.test(value)){
        showError(
            11,
            alternateMobile,
            alternateMobileErr,
            "Enter a valid 10-digit Mobile Number."
        );
        return false;
    }

    showSuccess(11, alternateMobile);
    return true;

}


/* ===========================
   Father's Name
=========================== */

function validateFatherName(value){

    value = value.trim();

    if(value === ""){
        showError(
            12,
            fatherName,
            fatherNameErr,
            "Father's Name cannot be blank."
        );
        return false;
    }

    const letters = value.replace(/[^A-Za-z]/g,"");

    if(letters.length < 2){
        showError(
            12,
            fatherName,
            fatherNameErr,
            "Enter a valid Father's Name."
        );
        return false;
    }

    showSuccess(12, fatherName);
    return true;

}


/* ===========================
   Father's Mobile
=========================== */

function validateFatherMobile(value){

    value = value.trim();

    if(value === ""){
        showError(
            13,
            fatherMobile,
            fatherMobileErr,
            "Father's Mobile cannot be blank."
        );
        return false;
    }

    const mobileRegex = /^[6-9]\d{9}$/;

    if(!mobileRegex.test(value)){
        showError(
            13,
            fatherMobile,
            fatherMobileErr,
            "Enter a valid 10-digit Mobile Number."
        );
        return false;
    }

    showSuccess(13, fatherMobile);
    return true;

}


/* ===========================
   Mother's Name (Optional)
=========================== */

function validateMotherName(value){

    value = value.trim();

    if(value === ""){
        showSuccess(14, motherName);
        return true;
    }

    const letters = value.replace(/[^A-Za-z]/g,"");

    if(letters.length < 2){
        showError(
            14,
            motherName,
            motherNameErr,
            "Enter a valid Mother's Name."
        );
        return false;
    }

    showSuccess(14, motherName);
    return true;

}


/* ===========================
   Mother's Mobile (Optional)
=========================== */

function validateMotherMobile(value){

    value = value.trim();

    if(value === ""){
        showSuccess(15, motherMobile);
        return true;
    }

    const mobileRegex = /^[6-9]\d{9}$/;

    if(!mobileRegex.test(value)){
        showError(
            15,
            motherMobile,
            motherMobileErr,
            "Enter a valid 10-digit Mobile Number."
        );
        return false;
    }

    showSuccess(15, motherMobile);
    return true;

}


/* ===========================
   Guardian Name (Optional)
=========================== */

function validateGuardianName(value){

    value = value.trim();

    if(value === ""){
        showSuccess(16, guardianName);
        return true;
    }

    const letters = value.replace(/[^A-Za-z]/g,"");

    if(letters.length < 2){
        showError(
            16,
            guardianName,
            guardianNameErr,
            "Enter a valid Guardian Name."
        );
        return false;
    }

    showSuccess(16, guardianName);
    return true;

}


/* ===========================
   Guardian Mobile (Optional)
=========================== */

function validateGuardianMobile(value){

    value = value.trim();

    if(value === ""){
        showSuccess(17, guardianMobile);
        return true;
    }

    const mobileRegex = /^[6-9]\d{9}$/;

    if(!mobileRegex.test(value)){
        showError(
            17,
            guardianMobile,
            guardianMobileErr,
            "Enter a valid 10-digit Mobile Number."
        );
        return false;
    }

    showSuccess(17, guardianMobile);
    return true;

}

/* ===========================
   Live Validation
=========================== */

if(firstName){
    firstName.addEventListener("input", () => {
        validateFirstName(firstName.value);
    });
}

if(middleName){
    middleName.addEventListener("input", () => {
        validateMiddleName(middleName.value);
    });
}

if(lastName){
    lastName.addEventListener("input", () => {
        validateLastName(lastName.value);
    });
}

if(gender){
    gender.addEventListener("change", () => {
        validateGender(gender.value);
    });
}

if(dob){
    dob.addEventListener("change", () => {
        validateDOB(dob.value);
    });
}

if(bloodGroup){
    bloodGroup.addEventListener("change", () => {
        validateBloodGroup();
    });
}

if(category){
    category.addEventListener("change", () => {
        validateCategory(category.value);
    });
}

if(religion){
    religion.addEventListener("change", () => {
        validateReligion(religion.value);
    });
}

if(nationality){
    nationality.addEventListener("change", () => {
        validateNationality(nationality.value);
    });
}

if(aadhaar){
    aadhaar.addEventListener("input", () => {
        validateAadhaar(aadhaar.value);
    });
}

if(alternateEmail){
    alternateEmail.addEventListener("input", () => {
        validateAlternateEmail(alternateEmail.value);
    });
}

if(alternateMobile){
    alternateMobile.addEventListener("input", () => {
        validateAlternateMobile(alternateMobile.value);
    });
}

if(fatherName){
    fatherName.addEventListener("input", () => {
        validateFatherName(fatherName.value);
    });
}

if(fatherMobile){
    fatherMobile.addEventListener("input", () => {
        validateFatherMobile(fatherMobile.value);
    });
}

if(motherName){
    motherName.addEventListener("input", () => {
        validateMotherName(motherName.value);
    });
}

if(motherMobile){
    motherMobile.addEventListener("input", () => {
        validateMotherMobile(motherMobile.value);
    });
}

if(guardianName){
    guardianName.addEventListener("input", () => {
        validateGuardianName(guardianName.value);
    });
}

if(guardianMobile){
    guardianMobile.addEventListener("input", () => {
        validateGuardianMobile(guardianMobile.value);
    });
}


/* ===========================
   Submit Validation
=========================== */

if(form){

    form.addEventListener("submit", function(e){

        const firstNameValid = validateFirstName(firstName.value);
        const middleNameValid = validateMiddleName(middleName.value);
        const lastNameValid = validateLastName(lastName.value);

        const genderValid = validateGender(gender.value);
        const dobValid = validateDOB(dob.value);

        const bloodGroupValid = validateBloodGroup();

        const categoryValid = validateCategory(category.value);
        const religionValid = validateReligion(religion.value);
        const nationalityValid = validateNationality(nationality.value);

        const aadhaarValid = validateAadhaar(aadhaar.value);

        const alternateEmailValid =
            validateAlternateEmail(alternateEmail.value);

        const alternateMobileValid =
            validateAlternateMobile(alternateMobile.value);

        const fatherNameValid =
            validateFatherName(fatherName.value);

        const fatherMobileValid =
            validateFatherMobile(fatherMobile.value);

        const motherNameValid =
            validateMotherName(motherName.value);

        const motherMobileValid =
            validateMotherMobile(motherMobile.value);

        const guardianNameValid =
            validateGuardianName(guardianName.value);

        const guardianMobileValid =
            validateGuardianMobile(guardianMobile.value);

        if(!(

            firstNameValid &&
            middleNameValid &&
            lastNameValid &&
            genderValid &&
            dobValid &&
            bloodGroupValid &&
            categoryValid &&
            religionValid &&
            nationalityValid &&
            aadhaarValid &&
            alternateEmailValid &&
            alternateMobileValid &&
            fatherNameValid &&
            fatherMobileValid &&
            motherNameValid &&
            motherMobileValid &&
            guardianNameValid &&
            guardianMobileValid

        )){
            e.preventDefault();
        }

    });

}