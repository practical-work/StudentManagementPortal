/* ==========================================
   Elements
========================================== */

const form = document.querySelector(".form-style");

// const container = document.getElementById("qualificationContainer");

// const addBtn = document.getElementById("addQualification");

const deletedInput = document.getElementById("deleted_ids");


/* ==========================================
   Common Functions
========================================== */

function showError(element, errBlock, errElement, message){

    errBlock.classList.add("failure");

    errElement.innerText = message;

    element.classList.add("error");

    element.classList.remove("success");

}


function showSuccess(element, errBlock){

    errBlock.classList.remove("failure");

    element.classList.remove("error");

    element.classList.add("success");

}


/* ==========================================
   Helper Functions
========================================== */

function onlyLetters(value){

    return value.replace(/[^A-Za-z ]/g, "").trim();

}


function isNumber(value){

    return /^[0-9]+(\.[0-9]+)?$/.test(value.trim());

}


/* ==========================================
   Get Elements From Card
========================================== */

function getFields(card){

    return {

        qualification : card.querySelector(".qualification"),

        board : card.querySelector(".board"),

        institute : card.querySelector(".institute"),

        roll : card.querySelector(".roll"),

        registration : card.querySelector(".registration"),

        stream : card.querySelector(".stream"),

        medium : card.querySelector(".medium"),

        passingYear : card.querySelector(".passing-year"),

        marksType : card.querySelector(".marksType"),

        percentage : card.querySelector(".percentage"),

        cgpa : card.querySelector(".cgpa"),

        totalMarks : card.querySelector(".total-marks"),

        obtainedMarks : card.querySelector(".obtained-marks"),

        subjects : card.querySelector(".subjects"),

        entranceExam : card.querySelector(".entrance-exam"),

        entranceRoll : card.querySelector(".entrance-roll"),

        entranceRank : card.querySelector(".entrance-rank"),

        entranceScore : card.querySelector(".entrance-score")

    };

}


/* ==========================================
   Get Error Elements
========================================== */

function getErrors(card){

    return{

        qualification : card.querySelector(".qualification-err"),

        board : card.querySelector(".board-err"),

        institute : card.querySelector(".institute-err"),

        roll : card.querySelector(".roll-err"),

        registration : card.querySelector(".registration-err"),

        stream : card.querySelector(".stream-err"),

        medium : card.querySelector(".medium-err"),

        passingYear : card.querySelector(".passing-year-err"),

        marksType : card.querySelector(".marks-type-err"),

        percentage : card.querySelector(".percentage-err"),

        cgpa : card.querySelector(".cgpa-err"),

        totalMarks : card.querySelector(".total-marks-err"),

        obtainedMarks : card.querySelector(".obtained-marks-err"),

        subjects : card.querySelector(".subjects-err"),

        entranceExam : card.querySelector(".entrance-exam-err"),

        entranceRoll : card.querySelector(".entrance-roll-err"),

        entranceRank : card.querySelector(".entrance-rank-err"),

        entranceScore : card.querySelector(".entrance-score-err")

    };

}

/* ==========================================
   Qualification
========================================== */

function validateQualification(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.qualification.value.trim();

    const errBlock = errors.qualification.closest(".err-block");

    if(value === ""){

        showError(
            fields.qualification,
            errBlock,
            errors.qualification,
            "Qualification cannot be blank."
        );

        return false;

    }

    if(value.length < 2){

        showError(
            fields.qualification,
            errBlock,
            errors.qualification,
            "Enter a valid Qualification."
        );

        return false;

    }

    showSuccess(fields.qualification, errBlock);

    return true;

}


/* ==========================================
   Board / University
========================================== */

function validateBoard(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.board.value.trim();

    const errBlock = errors.board.closest(".err-block");

    if(value === ""){

        showError(
            fields.board,
            errBlock,
            errors.board,
            "Board / University cannot be blank."
        );

        return false;

    }

    if(value.length < 2){

        showError(
            fields.board,
            errBlock,
            errors.board,
            "Enter a valid Board / University."
        );

        return false;

    }

    showSuccess(fields.board, errBlock);

    return true;

}


/* ==========================================
   Institute
========================================== */

function validateInstitute(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.institute.value.trim();

    const errBlock = errors.institute.closest(".err-block");

    if(value === ""){

        showError(
            fields.institute,
            errBlock,
            errors.institute,
            "Institute cannot be blank."
        );

        return false;

    }

    if(value.length < 2){

        showError(
            fields.institute,
            errBlock,
            errors.institute,
            "Enter a valid Institute."
        );

        return false;

    }

    showSuccess(fields.institute, errBlock);

    return true;

}


/* ==========================================
   Passing Year
========================================== */

function validatePassingYear(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.passingYear.value.trim();

    const errBlock = errors.passingYear.closest(".err-block");

    if(value === ""){

        showError(
            fields.passingYear,
            errBlock,
            errors.passingYear,
            "Passing Year cannot be blank."
        );

        return false;

    }

    if(!/^\d{4}$/.test(value)){

        showError(
            fields.passingYear,
            errBlock,
            errors.passingYear,
            "Enter a valid Passing Year."
        );

        return false;

    }

    const year = Number(value);

    const currentYear = new Date().getFullYear();

    if(year < 1950 || year > currentYear){

        showError(
            fields.passingYear,
            errBlock,
            errors.passingYear,
            "Passing Year is not valid."
        );

        return false;

    }

    showSuccess(fields.passingYear, errBlock);

    return true;

}


/* ==========================================
   Marks Type
========================================== */

function validateMarksType(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const errBlock = errors.marksType.closest(".err-block");

    showSuccess(fields.marksType, errBlock);

    return true;

}


/* ==========================================
   Percentage
========================================== */

function validatePercentage(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.percentage.value.trim();

    const errBlock = errors.percentage.closest(".err-block");

    if(fields.marksType.value !== "Percentage"){

        showSuccess(fields.percentage, errBlock);

        return true;

    }

    if(value === ""){

        showError(
            fields.percentage,
            errBlock,
            errors.percentage,
            "Percentage cannot be blank."
        );

        return false;

    }

    if(!isNumber(value)){

        showError(
            fields.percentage,
            errBlock,
            errors.percentage,
            "Enter a valid Percentage."
        );

        return false;

    }

    const percentage = Number(value);

    if(percentage < 0 || percentage > 100){

        showError(
            fields.percentage,
            errBlock,
            errors.percentage,
            "Percentage must be between 0 and 100."
        );

        return false;

    }

    showSuccess(fields.percentage, errBlock);

    return true;

}


/* ==========================================
   CGPA
========================================== */

function validateCGPA(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.cgpa.value.trim();

    const errBlock = errors.cgpa.closest(".err-block");

    if(fields.marksType.value !== "CGPA"){

        showSuccess(fields.cgpa, errBlock);

        return true;

    }

    if(value === ""){

        showError(
            fields.cgpa,
            errBlock,
            errors.cgpa,
            "CGPA cannot be blank."
        );

        return false;

    }

    if(!isNumber(value)){

        showError(
            fields.cgpa,
            errBlock,
            errors.cgpa,
            "Enter a valid CGPA."
        );

        return false;

    }

    const cgpa = Number(value);

    if(cgpa < 0 || cgpa > 10){

        showError(
            fields.cgpa,
            errBlock,
            errors.cgpa,
            "CGPA must be between 0 and 10."
        );

        return false;

    }

    showSuccess(fields.cgpa, errBlock);

    return true;

}

/* ==========================================
   Total Marks (Optional)
========================================== */

function validateTotalMarks(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.totalMarks.value.trim();

    const errBlock = errors.totalMarks.closest(".err-block");

    if(value === ""){

        showSuccess(fields.totalMarks, errBlock);

        return true;

    }

    if(!isNumber(value)){

        showError(
            fields.totalMarks,
            errBlock,
            errors.totalMarks,
            "Enter valid Total Marks."
        );

        return false;

    }

    showSuccess(fields.totalMarks, errBlock);

    return true;

}


/* ==========================================
   Obtained Marks (Optional)
========================================== */

function validateObtainedMarks(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.obtainedMarks.value.trim();

    const errBlock = errors.obtainedMarks.closest(".err-block");

    if(value === ""){

        showSuccess(fields.obtainedMarks, errBlock);

        return true;

    }

    if(!isNumber(value)){

        showError(
            fields.obtainedMarks,
            errBlock,
            errors.obtainedMarks,
            "Enter valid Obtained Marks."
        );

        return false;

    }

    if(fields.totalMarks.value.trim() !== ""){

        if(Number(value) > Number(fields.totalMarks.value)){

            showError(
                fields.obtainedMarks,
                errBlock,
                errors.obtainedMarks,
                "Obtained Marks cannot exceed Total Marks."
            );

            return false;

        }

    }

    showSuccess(fields.obtainedMarks, errBlock);

    return true;

}


/* ==========================================
   Roll Number (Optional)
========================================== */

function validateRoll(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.roll.value.trim();

    const errBlock = errors.roll.closest(".err-block");

    if(value === ""){

        showSuccess(fields.roll, errBlock);

        return true;

    }

    if(value.length < 2){

        showError(
            fields.roll,
            errBlock,
            errors.roll,
            "Enter a valid Roll Number."
        );

        return false;

    }

    showSuccess(fields.roll, errBlock);

    return true;

}


/* ==========================================
   Registration Number (Optional)
========================================== */

function validateRegistration(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.registration.value.trim();

    const errBlock = errors.registration.closest(".err-block");

    if(value === ""){

        showSuccess(fields.registration, errBlock);

        return true;

    }

    if(value.length < 2){

        showError(
            fields.registration,
            errBlock,
            errors.registration,
            "Enter a valid Registration Number."
        );

        return false;

    }

    showSuccess(fields.registration, errBlock);

    return true;

}


/* ==========================================
   Stream (Optional)
========================================== */

function validateStream(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.stream.value.trim();

    const errBlock = errors.stream.closest(".err-block");

    if(value === ""){

        showSuccess(fields.stream, errBlock);

        return true;

    }

    if(value.length < 2){

        showError(
            fields.stream,
            errBlock,
            errors.stream,
            "Enter a valid Stream."
        );

        return false;

    }

    showSuccess(fields.stream, errBlock);

    return true;

}


/* ==========================================
   Medium (Optional)
========================================== */

function validateMedium(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.medium.value.trim();

    const errBlock = errors.medium.closest(".err-block");

    if(value === ""){

        showSuccess(fields.medium, errBlock);

        return true;

    }

    if(value.length < 2){

        showError(
            fields.medium,
            errBlock,
            errors.medium,
            "Enter a valid Medium."
        );

        return false;

    }

    showSuccess(fields.medium, errBlock);

    return true;

}


/* ==========================================
   Subjects (Optional)
========================================== */

function validateSubjects(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const errBlock = errors.subjects.closest(".err-block");

    showSuccess(fields.subjects, errBlock);

    return true;

}


/* ==========================================
   Entrance Exam (Optional)
========================================== */

function validateEntranceExam(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.entranceExam.value.trim();

    const errBlock = errors.entranceExam.closest(".err-block");

    if(value === ""){

        showSuccess(fields.entranceExam, errBlock);

        return true;

    }

    if(value.length < 2){

        showError(
            fields.entranceExam,
            errBlock,
            errors.entranceExam,
            "Enter a valid Entrance Exam."
        );

        return false;

    }

    showSuccess(fields.entranceExam, errBlock);

    return true;

}


/* ==========================================
   Entrance Roll (Optional)
========================================== */

function validateEntranceRoll(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.entranceRoll.value.trim();

    const errBlock = errors.entranceRoll.closest(".err-block");

    if(value === ""){

        showSuccess(fields.entranceRoll, errBlock);

        return true;

    }

    if(value.length < 2){

        showError(
            fields.entranceRoll,
            errBlock,
            errors.entranceRoll,
            "Enter a valid Entrance Roll Number."
        );

        return false;

    }

    showSuccess(fields.entranceRoll, errBlock);

    return true;

}


/* ==========================================
   Entrance Rank (Optional)
========================================== */

function validateEntranceRank(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.entranceRank.value.trim();

    const errBlock = errors.entranceRank.closest(".err-block");

    if(value === ""){

        showSuccess(fields.entranceRank, errBlock);

        return true;

    }

    if(value.length < 1){

        showError(
            fields.entranceRank,
            errBlock,
            errors.entranceRank,
            "Enter a valid Rank."
        );

        return false;

    }

    showSuccess(fields.entranceRank, errBlock);

    return true;

}


/* ==========================================
   Entrance Score (Optional)
========================================== */

function validateEntranceScore(card){

    const fields = getFields(card);
    const errors = getErrors(card);

    const value = fields.entranceScore.value.trim();

    const errBlock = errors.entranceScore.closest(".err-block");

    if(value === ""){

        showSuccess(fields.entranceScore, errBlock);

        return true;

    }

    if(!isNumber(value)){

        showError(
            fields.entranceScore,
            errBlock,
            errors.entranceScore,
            "Enter a valid Score."
        );

        return false;

    }

    showSuccess(fields.entranceScore, errBlock);

    return true;

}


/* ==========================================
   Validate Complete Card
========================================== */

function validateCard(card){

    return (

        validateQualification(card) &&
        validateBoard(card) &&
        validateInstitute(card) &&
        validateRoll(card) &&
        validateRegistration(card) &&
        validateStream(card) &&
        validateMedium(card) &&
        validatePassingYear(card) &&
        validateMarksType(card) &&
        validatePercentage(card) &&
        validateCGPA(card) &&
        validateTotalMarks(card) &&
        validateObtainedMarks(card) &&
        validateSubjects(card) &&
        validateEntranceExam(card) &&
        validateEntranceRoll(card) &&
        validateEntranceRank(card) &&
        validateEntranceScore(card)

    );

}


/* ==========================================
   Attach Live Validation
========================================== */

function attachValidation(card){

    const fields = getFields(card);

    fields.qualification.addEventListener("input",()=>validateQualification(card));

    fields.board.addEventListener("input",()=>validateBoard(card));

    fields.institute.addEventListener("input",()=>validateInstitute(card));

    fields.roll.addEventListener("input",()=>validateRoll(card));

    fields.registration.addEventListener("input",()=>validateRegistration(card));

    fields.stream.addEventListener("input",()=>validateStream(card));

    fields.medium.addEventListener("input",()=>validateMedium(card));

    fields.passingYear.addEventListener("input",()=>validatePassingYear(card));

    fields.marksType.addEventListener("change",()=>{

        validateMarksType(card);

        validatePercentage(card);

        validateCGPA(card);

    });

    fields.percentage.addEventListener("input",()=>validatePercentage(card));

    fields.cgpa.addEventListener("input",()=>validateCGPA(card));

    fields.totalMarks.addEventListener("input",()=>{

        validateTotalMarks(card);

        validateObtainedMarks(card);

    });

    fields.obtainedMarks.addEventListener("input",()=>validateObtainedMarks(card));

    fields.subjects.addEventListener("input",()=>validateSubjects(card));

    fields.entranceExam.addEventListener("input",()=>validateEntranceExam(card));

    fields.entranceRoll.addEventListener("input",()=>validateEntranceRoll(card));

    fields.entranceRank.addEventListener("input",()=>validateEntranceRank(card));

    fields.entranceScore.addEventListener("input",()=>validateEntranceScore(card));

}


// /* ==========================================
//    Card Titles
// ========================================== */

// function updateTitles(){

//     document.querySelectorAll(".qualification-card").forEach((card,index)=>{

//         card.querySelector(".title-text").textContent =
//         "Qualification " + (index+1);

//     });

// }


// /* ==========================================
//    Attach Events
// ========================================== */

// function attachEvents(card){

//     attachMarksType(card);

//     attachValidation(card);

//     const removeBtn = card.querySelector(".remove-btn");

//     if(removeBtn){

//         removeBtn.addEventListener("click",function(){

//             const hiddenId = card.querySelector(
//                 'input[name="qualification_id[]"]'
//             );

//             if(hiddenId && hiddenId.value !== ""){

//                 if(deletedInput.value === ""){

//                     deletedInput.value = hiddenId.value;

//                 }

//                 else{

//                     deletedInput.value += "," + hiddenId.value;

//                 }

//             }

//             card.remove();

//             updateTitles();

//             if(document.querySelectorAll(".qualification-card").length===0){

//                 addBtn.click();

//             }

//         });

//     }

// }


// /* ==========================================
//    Existing Cards
// ========================================== */

// document.querySelectorAll(".qualification-card").forEach(card=>{

//     attachEvents(card);

// });


// /* ==========================================
//    Add New Card
// ========================================== */

// if(addBtn){

//     addBtn.addEventListener("click",function(){

//         container.insertAdjacentHTML("beforeend",createCard());

//         const card = container.lastElementChild;

//         attachEvents(card);

//         updateTitles();

//     });

// }


// /* ==========================================
//    First Card
// ========================================== */

// if(document.querySelectorAll(".qualification-card").length===0){

//     addBtn.click();

// }

// updateTitles();


/* ==========================================
   Submit Validation
========================================== */

if(form){

    form.addEventListener("submit",function(e){

        let valid = true;

        document.querySelectorAll(".qualification-card").forEach(card=>{

            if(!validateCard(card)){

                valid = false;

            }

        });

        if(!valid){

            e.preventDefault();

        }

    });

}