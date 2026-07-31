const container = document.getElementById("qualificationContainer");
const addBtn = document.getElementById("addQualification");

function createCard() {
    return `
    <div class="qualification-card">
        <input type="hidden" name="qualification_id[]" value="">
        
        <div class="card-title">
            <span class="title-text"></span>
            <button type="button" class="remove-btn">Remove</button>
        </div>

        <div class="grid">
            <!-- Qualification -->
            <div>
                <label>Qualification <span>*</span></label>
                <input type="text" name="qualification[]" class="qualification" placeholder="Class 10 / Class 12 / Diploma">
                <div class="err-block"><p class="err qualification-err"></p></div>
            </div>

            <!-- Board -->
            <div>
                <label>Board / University <span>*</span></label>
                <input type="text" name="board[]" class="board">
                <div class="err-block"><p class="err board-err"></p></div>
            </div>

            <!-- Institute -->
            <div>
                <label>Institute <span>*</span></label>
                <input type="text" name="institute[]" class="institute">
                <div class="err-block"><p class="err institute-err"></p></div>
            </div>

            <!-- Roll Number -->
            <div>
                <label>Roll Number</label>
                <input type="text" name="roll[]" class="roll">
                <div class="err-block"><p class="err roll-err"></p></div>
            </div>

            <!-- Registration -->
            <div>
                <label>Registration Number</label>
                <input type="text" name="registration[]" class="registration">
                <div class="err-block"><p class="err registration-err"></p></div>
            </div>

            <!-- Stream -->
            <div>
                <label>Stream</label>
                <input type="text" name="stream[]" class="stream">
                <div class="err-block"><p class="err stream-err"></p></div>
            </div>

            <!-- Medium -->
            <div>
                <label>Medium</label>
                <input type="text" name="medium[]" class="medium">
                <div class="err-block"><p class="err medium-err"></p></div>
            </div>

            <!-- Passing Year -->
            <div>
                <label>Passing Year <span>*</span></label>
                <input type="text" name="passing_year[]" class="passing-year">
                <div class="err-block"><p class="err passing-year-err"></p></div>
            </div>

            <!-- Marks Type -->
            <div>
                <label>Marks Type</label>
                <select name="marks_type[]" class="marksType">
                    <option value="">Select</option>
                    <option value="Percentage">Percentage</option>
                    <option value="CGPA">CGPA</option>
                </select>
                <div class="err-block"><p class="err marks-type-err"></p></div>
            </div>

            <!-- Percentage -->
            <div class="percentageBox">
                <label>Percentage</label>
                <input type="text" name="percentage[]" class="percentage">
                <div class="err-block"><p class="err percentage-err"></p></div>
            </div>

            <!-- CGPA -->
            <div class="cgpaBox">
                <label>CGPA</label>
                <input type="text" name="cgpa[]" class="cgpa">
                <div class="err-block"><p class="err cgpa-err"></p></div>
            </div>

            <!-- Total Marks -->
            <div>
                <label>Total Marks</label>
                <input type="text" name="total_marks[]" class="total-marks">
                <div class="err-block"><p class="err total-marks-err"></p></div>
            </div>

            <!-- Obtained Marks -->
            <div>
                <label>Obtained Marks</label>
                <input type="text" name="obtained_marks[]" class="obtained-marks">
                <div class="err-block"><p class="err obtained-marks-err"></p></div>
            </div>

            <!-- Subjects -->
            <div class="full">
                <label>Subjects</label>
                <textarea name="subjects[]" class="subjects" style="resize:none;"></textarea>
                <div class="err-block"><p class="err subjects-err"></p></div>
            </div>

            <!-- Entrance Exam -->
            <div>
                <label>Entrance Exam</label>
                <input type="text" name="entrance_exam[]" class="entrance-exam">
                <div class="err-block"><p class="err entrance-exam-err"></p></div>
            </div>

            <!-- Entrance Roll -->
            <div>
                <label>Entrance Roll No.</label>
                <input type="text" name="entrance_roll[]" class="entrance-roll">
                <div class="err-block"><p class="err entrance-roll-err"></p></div>
            </div>

            <!-- Rank -->
            <div>
                <label>Rank</label>
                <input type="text" name="entrance_rank[]" class="entrance-rank">
                <div class="err-block"><p class="err entrance-rank-err"></p></div>
            </div>

            <!-- Score -->
            <div>
                <label>Score</label>
                <input type="text" name="entrance_score[]" class="entrance-score">
                <div class="err-block"><p class="err entrance-score-err"></p></div>
            </div>
        </div>
    </div>`;
}

function updateTitles() {
    document.querySelectorAll(".qualification-card").forEach((card, index) => {
        card.querySelector(".title-text").textContent = "Qualification " + (index + 1);
    });
}

function attachMarksType(card) {
    const marksType = card.querySelector(".marksType");
    const percentageBox = card.querySelector(".percentageBox");
    const cgpaBox = card.querySelector(".cgpaBox");

    function updateFields() {
        if (marksType.value === "Percentage") {
            percentageBox.style.display = "flex";
            cgpaBox.style.display = "none";
        } else if (marksType.value === "CGPA") {
            percentageBox.style.display = "none";
            cgpaBox.style.display = "flex";
        } else {
            percentageBox.style.display = "flex";
            cgpaBox.style.display = "flex";
        }
    }

    marksType.addEventListener("change", updateFields);
    updateFields();
}

function attachEvents(card) {
    const removeBtn = card.querySelector(".remove-btn");
    
    if (removeBtn) {
        removeBtn.addEventListener("click", function () {
            const hiddenId = card.querySelector('input[name="qualification_id[]"]');
            
            if (hiddenId && hiddenId.value !== "") {
                const deletedInput = document.getElementById("deleted_ids");
                if (deletedInput) {
                    if (deletedInput.value === "") {
                        deletedInput.value = hiddenId.value;
                    } else {
                        deletedInput.value += "," + hiddenId.value;
                    }
                }
            }
            
            card.remove();
            updateTitles();
            
            if (document.querySelectorAll(".qualification-card").length === 0) {
                addBtn.click();
            }
        });
    }

    attachMarksType(card);

    // *IMPORTANT*: If your registration-step3-validation.js exports a function to attach 
    // validation to a single card (e.g., `attachValidation(card)`), call it right here:
    if (typeof attachValidation === "function") {
        attachValidation(card); 
    }
}

if (addBtn) {
    addBtn.addEventListener("click", function () {
        container.insertAdjacentHTML("beforeend", createCard());
        const card = container.lastElementChild;
        attachEvents(card);
        updateTitles();
    });
}

document.querySelectorAll(".qualification-card").forEach(function (card) {
    attachEvents(card);
});

if (document.querySelectorAll(".qualification-card").length === 0) {
    if (addBtn) addBtn.click();
}

updateTitles();