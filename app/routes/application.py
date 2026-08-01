from flask import Blueprint, request, render_template, redirect, url_for, flash, session, current_app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import re
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models.email_otp import EmailOTP
from app.models.master_gender import MasterGender
from app.models.master_category import MasterCategory
from app.models.master_religion import MasterReligion
from app.models.master_nationality import MasterNationality
from app.models.master_blood_group import MasterBloodGroup
from app.models.student_personal import StudentPersonal
from app import student_db
from app.models.student_account import StudentAccount
from services.email_service import EmailService
from app.models.student_academic import StudentAcademic
from app.models.student_address import StudentAddress
from app.models.student_family import StudentFamily
from app.models.student_documents import StudentDocuments
from app.models.student_academic_document import StudentAcademicDocument

application_bp = Blueprint("application", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_step_access(student, required_step):
    if student.is_final_submitted:
        return redirect(url_for("pages.dashboard"))
    if student.current_step + 1 < required_step:
        flash(f"Please complete Step {student.current_step} first.", "warning")
        return redirect(url_for(f"application.step{student.current_step}"))
    return None

# =========================================================================
# STEP 2
# =========================================================================

@application_bp.route("/registration/step2")
def step2():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("auth.login"))

    response = check_step_access(student, 2)
    if response: return response
    
    personal = StudentPersonal.query.filter_by(student_id=student.student_id).first()
    genders = MasterGender.query.order_by(MasterGender.gender_name).all()
    categories = MasterCategory.query.order_by(MasterCategory.category_name).all()
    religions = MasterReligion.query.order_by(MasterReligion.religion_name).all()
    nationalities = MasterNationality.query.order_by(MasterNationality.nationality_name).all()
    blood_groups = MasterBloodGroup.query.order_by(MasterBloodGroup.blood_group_name).all()

    return render_template(
        "auth/registration-step2.html",
        student=student, personal=personal, genders=genders,
        categories=categories, religions=religions,
        nationalities=nationalities, blood_groups=blood_groups
    )

@application_bp.route("/registration/step2", methods=["POST"])
def save_step2():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student: return redirect(url_for("auth.login"))

    response = check_step_access(student, 2)
    if response: return response

    # --- BACKEND VALIDATION ---
    required_fields = {
        "first_name": "First Name", "gender_id": "Gender", "date_of_birth": "Date of Birth",
        "category_id": "Category", "religion_id": "Religion", "nationality_id": "Nationality",
        "aadhaar_no": "Aadhaar Number", "father_name": "Father Name", "father_mobile": "Father Mobile"
    }

    for field, name in required_fields.items():
        val = request.form.get(field, "").strip()
        if not val:
            flash(f"{name} is required.", "danger")
            return redirect(url_for("application.step2"))

    personal = StudentPersonal.query.filter_by(student_id=student.student_id).first()
    if not personal:
        personal = StudentPersonal(student_id=student.student_id)
        student_db.session.add(personal)

    personal.first_name = request.form["first_name"].strip()
    personal.middle_name = request.form.get("middle_name", "").strip()
    personal.last_name = request.form.get("last_name", "").strip()
    personal.gender_id = request.form["gender_id"]
    dob = request.form.get("date_of_birth")

    dob = datetime.strptime(
        dob,
        "%Y-%m-%d"
    ).date()
    
    personal.date_of_birth = dob
    personal.blood_group_id = request.form.get("blood_group_id") or None
    personal.category_id = request.form["category_id"]
    personal.religion_id = request.form["religion_id"]
    personal.nationality_id = request.form["nationality_id"]
    aadhaar_no = request.form["aadhaar_no"].strip()
    existing = StudentPersonal.query.filter(
    StudentPersonal.aadhaar_no == aadhaar_no,
    StudentPersonal.student_id != student.student_id
    ).first()
    
    if existing:
       flash("This Aadhaar number is already registered.", "danger")
       return redirect(url_for("application.step2"))
        
    personal.aadhaar_no = aadhaar_no
    personal.father_name = request.form["father_name"].strip()
    personal.father_mobile = request.form["father_mobile"].strip()
    personal.mother_name = request.form.get("mother_name", "").strip()
    personal.mother_mobile = request.form.get("mother_mobile", "").strip()
    personal.alternate_email = request.form.get("alternate_email", "").strip()
    personal.alternate_mobile = request.form.get("alternate_mobile", "").strip()
    personal.guardian_name = request.form.get("guardian_name", "").strip()
    personal.guardian_mobile = request.form.get("guardian_mobile", "").strip()

    student.current_step = max(student.current_step, 2)
    student_db.session.commit()

    flash("Personal Details Saved Successfully.", "success")
    return redirect(url_for("application.step3"))


# =========================================================================
# STEP 3
# =========================================================================

@application_bp.route("/registration/step3")
def step3():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("auth.login"))

    response = check_step_access(student, 3)
    if response: return response

    academic_records = StudentAcademic.query.filter_by(student_id=student.student_id).all()
    return render_template("auth/registration-step3.html", student=student, academic_records=academic_records)

@application_bp.route("/registration/step3", methods=["POST"])
def save_step3():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("auth.login"))

    response = check_step_access(student, 3)
    if response: return response

    qualification = request.form.getlist("qualification[]")
    board = request.form.getlist("board[]")
    institute = request.form.getlist("institute[]")
    roll = request.form.getlist("roll[]")
    registration = request.form.getlist("registration[]")
    stream = request.form.getlist("stream[]")
    medium = request.form.getlist("medium[]")
    year = request.form.getlist("passing_year[]")
    marks_type = request.form.getlist("marks_type[]")
    percentage = request.form.getlist("percentage[]")
    cgpa = request.form.getlist("cgpa[]")
    total = request.form.getlist("total_marks[]")
    obtained = request.form.getlist("obtained_marks[]")
    subjects = request.form.getlist("subjects[]")
    exam = request.form.getlist("entrance_exam[]")
    exam_roll = request.form.getlist("entrance_roll[]")
    rank = request.form.getlist("entrance_rank[]")
    score = request.form.getlist("entrance_score[]")

    # --- BACKEND VALIDATION ---
    valid_records = 0
    for i in range(len(qualification)):
        if not qualification[i].strip():
            continue
        valid_records += 1
        # Check required fields within a submitted card
        if not board[i].strip() or not institute[i].strip() or not year[i].strip():
            flash("Board, Institute, and Passing Year are required for all qualifications.", "danger")
            return redirect(url_for("application.step3"))

    if valid_records == 0:
        flash("At least one educational qualification is required.", "danger")
        return redirect(url_for("application.step3"))

    # Delete all old qualifications and insert new ones
    StudentAcademic.query.filter_by(student_id=student.student_id).delete()

    for i in range(len(qualification)):
        if not qualification[i].strip():
            continue

        academic = StudentAcademic(
            student_id=student.student_id,
            qualification=qualification[i].strip(),
            board_university=board[i].strip(),
            institute_name=institute[i].strip(),
            roll_number=roll[i].strip() or None,
            registration_number=registration[i].strip() or None,
            stream=stream[i].strip() or None,
            medium=medium[i].strip() or None,
            passing_year=int(year[i]) if year[i] else None,
            marks_type=marks_type[i] or None,
            percentage=float(percentage[i]) if percentage[i] else None,
            cgpa=float(cgpa[i]) if cgpa[i] else None,
            total_marks=float(total[i]) if total[i] else None,
            obtained_marks=float(obtained[i]) if obtained[i] else None,
            subjects=subjects[i].strip() or None,
            entrance_exam=exam[i].strip() or None,
            entrance_roll_number=exam_roll[i].strip() or None,
            entrance_rank=rank[i].strip() or None,
            entrance_score=score[i].strip() or None
        )
        student_db.session.add(academic)

    if student.current_step < 3:
        student.current_step = 3

    student_db.session.commit()
    flash("Academic details saved successfully.", "success")
    return redirect(url_for("application.step4"))


# =========================================================================
# STEP 4
# =========================================================================

@application_bp.route("/registration/step4")
def step4():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("auth.login"))

    response = check_step_access(student, 4)
    if response: return response
    
    address = StudentAddress.query.filter_by(student_id=student.student_id).first()
    return render_template("auth/registration-step4.html", student=student, address=address)

@application_bp.route("/registration/step4", methods=["POST"])
def save_step4():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student: return redirect(url_for("auth.login"))

    response = check_step_access(student, 4)
    if response: return response

    # --- BACKEND VALIDATION ---
    required_fields = [
        "permanent_address", "permanent_state", "permanent_district", "permanent_city", "permanent_pincode",
        "correspondence_address", "correspondence_state", "correspondence_district", "correspondence_city", "correspondence_pincode"
    ]
    for field in required_fields:
        if not request.form.get(field, "").strip():
            flash("All address fields are required.", "danger")
            return redirect(url_for("application.step4"))

    address = StudentAddress.query.filter_by(student_id=student.student_id).first()
    if not address:
        address = StudentAddress(student_id=student.student_id)
        student_db.session.add(address)

    # Permanent Address
    address.permanent_address = request.form["permanent_address"].strip()
    address.permanent_state = request.form["permanent_state"].strip()
    address.permanent_district = request.form["permanent_district"].strip()
    address.permanent_city = request.form["permanent_city"].strip()
    address.permanent_pincode = request.form["permanent_pincode"].strip()

    # Correspondence Address
    address.correspondence_address = request.form["correspondence_address"].strip()
    address.correspondence_state = request.form["correspondence_state"].strip()
    address.correspondence_district = request.form["correspondence_district"].strip()
    address.correspondence_city = request.form["correspondence_city"].strip()
    address.correspondence_pincode = request.form["correspondence_pincode"].strip()

    if student.current_step < 4:
        student.current_step = 4

    student_db.session.commit()
    flash("Address details saved successfully.", "success")
    return redirect(url_for("application.step5"))


# =========================================================================
# STEP 5
# =========================================================================

@application_bp.route("/registration/step5")
def step5():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("auth.login"))

    response = check_step_access(student, 5)
    if response: return response

    family = StudentFamily.query.filter_by(student_id=student.student_id).first()
    return render_template("auth/registration-step5.html", student=student, family=family)

@application_bp.route("/registration/step5", methods=["POST"])
def save_step5():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student: return redirect(url_for("auth.login"))

    response = check_step_access(student, 5)
    if response: return response

    # --- BACKEND VALIDATION ---
    core_fields = ["father_occupation", "mother_occupation", "domicile_status", "domicile_state", "marital_status"]
    for field in core_fields:
        if not request.form.get(field, "").strip():
            flash("Please complete all required base fields.", "danger")
            return redirect(url_for("application.step5"))

    # Conditional Validation
    if request.form.get("is_twin") == "yes":
        if not request.form.get("twin_name") or not request.form.get("twin_relation"):
            flash("Twin Name and Relation are required.", "danger")
            return redirect(url_for("application.step5"))
            
    if request.form.get("is_freedom_fighter") == "yes":
        if not request.form.get("freedom_fighter_name") or not request.form.get("freedom_fighter_certificate_no"):
            flash("Freedom Fighter details are required.", "danger")
            return redirect(url_for("application.step5"))

    if request.form.get("is_pwbd") == "yes":
        if not request.form.get("pwbd_category") or not request.form.get("pwbd_certificate_no"):
            flash("PwBD details and certificate number are required.", "danger")
            return redirect(url_for("application.step5"))

    family = StudentFamily.query.filter_by(student_id=student.student_id).first()
    if not family:
        family = StudentFamily(student_id=student.student_id)
        student_db.session.add(family)

    # Save logic
    family.father_occupation = request.form.get("father_occupation")
    family.mother_occupation = request.form.get("mother_occupation")
    family.guardian_occupation = request.form.get("guardian_occupation")
    
    # Twin
    family.is_twin = True if request.form.get("is_twin") == "yes" else False
    family.twin_name = request.form.get("twin_name") if family.is_twin else None
    family.twin_relation = request.form.get("twin_relation") if family.is_twin else None

    # Freedom Fighter
    family.is_freedom_fighter = True if request.form.get("is_freedom_fighter") == "yes" else False
    family.freedom_fighter_name = request.form.get("freedom_fighter_name") if family.is_freedom_fighter else None
    family.freedom_fighter_relation = request.form.get("freedom_fighter_relation") if family.is_freedom_fighter else None
    family.freedom_fighter_certificate_no = request.form.get("freedom_fighter_certificate_no") if family.is_freedom_fighter else None

    # NCC
    family.is_ncc_candidate = True if request.form.get("is_ncc_candidate") == "yes" else False
    family.ncc_certificate_no = request.form.get("ncc_certificate_no") if family.is_ncc_candidate else None
    family.ncc_level = request.form.get("ncc_level") if family.is_ncc_candidate else None

    # Criminal Case
    family.criminal_case = True if request.form.get("criminal_case") == "yes" else False
    family.criminal_case_details = request.form.get("criminal_case_details") if family.criminal_case else None

    # Ex Servicemen
    family.is_ex_servicemen = True if request.form.get("is_ex_servicemen") == "yes" else False
    family.ex_servicemen_details = request.form.get("ex_servicemen_details") if family.is_ex_servicemen else None

    # PwBD
    family.is_pwbd = True if request.form.get("is_pwbd") == "yes" else False
    family.pwbd_category = request.form.get("pwbd_category") if family.is_pwbd else None
    family.pwbd_certificate_no = request.form.get("pwbd_certificate_no") if family.is_pwbd else None

    # Residence & Marital
    family.domicile_status = request.form.get("domicile_status")
    family.domicile_state = request.form.get("domicile_state")
    family.marital_status = request.form.get("marital_status")

    if student.current_step < 5:
        student.current_step = 5

    student_db.session.commit()
    flash("Family and other details saved successfully.", "success")
    return redirect(url_for("application.step6"))


# =========================================================================
# STEP 6
# =========================================================================

@application_bp.route("/registration/step6")
def step6():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("auth.login"))

    response = check_step_access(student, 6)
    if response: return response

    personal = StudentPersonal.query.filter_by(student_id=student.student_id).first()
    family = StudentFamily.query.filter_by(student_id=student.student_id).first()
    documents = StudentDocuments.query.filter_by(student_id=student.student_id).first()

    if documents:
        document_fields = [
            "profile_photo", "signature", "aadhaar_card", "birth_certificate",
            "caste_certificate", "pwbd_certificate", "income_certificate",
            "domicile_certificate", "migration_certificate"
        ]
        for field in document_fields:
            value = getattr(documents, field)
            if value:
                setattr(documents, field, value.replace("\\", "/"))

    academic_records = StudentAcademic.query.filter_by(student_id=student.student_id).all()
    academic_documents = {}
    for record in academic_records:
        document = StudentAcademicDocument.query.filter_by(academic_id=record.id).first()
        if document and document.file_path:
            document.file_path = document.file_path.replace("\\", "/")
        academic_documents[record.id] = document

    return render_template(
        "auth/registration-step6.html",
        student=student, personal=personal, family=family,
        documents=documents, academic_records=academic_records,
        academic_documents=academic_documents
    )

@application_bp.route("/registration/step6", methods=["POST"])
def save_step6():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student: return redirect(url_for("auth.login"))

    response = check_step_access(student, 6)
    if response: return response
    
    documents = StudentDocuments.query.filter_by(student_id=student.student_id).first()
    if not documents:
        documents = StudentDocuments(student_id=student.student_id)
        student_db.session.add(documents)

    # Load personal & family context to know which documents are mandatory
    personal = StudentPersonal.query.filter_by(student_id=student.student_id).first()
    family = StudentFamily.query.filter_by(student_id=student.student_id).first()

    # --- BACKEND VALIDATION & UPLOAD ---
    # Helper to check if file is provided or already in DB
    def get_or_validate_file(field_name, is_mandatory=False):
        file = request.files.get(field_name)
        has_new_file = file and file.filename != ""
        existing_file = getattr(documents, field_name, None)
        
        if is_mandatory and not has_new_file and not existing_file:
            return False, f"Missing required document: {field_name.replace('_', ' ').title()}"
            
        if has_new_file and not allowed_file(file.filename):
            return False, f"Invalid file format for {field_name.replace('_', ' ').title()}."
            
        return True, file

    # 1. Base Required Documents
    base_required = ["profile_photo", "signature", "aadhaar_card", "birth_certificate"]
    for field in base_required:
        is_valid, result = get_or_validate_file(field, is_mandatory=True)
        if not is_valid:
            flash(result, "danger")
            return redirect(url_for("application.step6"))

    # 2. Conditional Required Documents
    if personal and personal.category and personal.category.category_name.lower() != "general":
        is_valid, result = get_or_validate_file("caste_certificate", is_mandatory=True)
        if not is_valid:
            flash("Category Certificate is required for non-General candidates.", "danger")
            return redirect(url_for("application.step6"))

    if family and family.is_pwbd:
        is_valid, result = get_or_validate_file("pwbd_certificate", is_mandatory=True)
        if not is_valid:
            flash("PwBD Certificate is required because you declared PwBD status.", "danger")
            return redirect(url_for("application.step6"))

    # 3. Process Uploads
    base_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], student.application_no)
    education_folder = os.path.join(base_folder, "education")
    os.makedirs(base_folder, exist_ok=True)
    os.makedirs(education_folder, exist_ok=True)

    all_docs = [
        "profile_photo", "signature", "aadhaar_card", "birth_certificate",
        "caste_certificate", "pwbd_certificate", "income_certificate",
        "domicile_certificate", "migration_certificate"
    ]

    for field in all_docs:
        file = request.files.get(field)
        if file and file.filename != "":
            extension = os.path.splitext(file.filename)[1]
            filename = field + extension
            filepath = os.path.join(base_folder, filename)
            file.save(filepath)
            setattr(documents, field, f"uploads/{student.application_no}/{filename}")

    # 4. Academic Documents Validation & Upload
    academic_records = StudentAcademic.query.filter_by(student_id=student.student_id).all()
    for record in academic_records:
        input_name = f"academic_{record.id}"
        file = request.files.get(input_name)
        has_new_file = file and file.filename != ""
        
        academic_document = StudentAcademicDocument.query.filter_by(academic_id=record.id).first()
        has_existing = academic_document and academic_document.file_path
        
        if not has_new_file and not has_existing:
            flash(f"Missing document for Qualification: {record.qualification}", "danger")
            return redirect(url_for("application.step6"))

        if has_new_file:
            if not allowed_file(file.filename):
                flash(f"Invalid file format for {record.qualification}", "danger")
                return redirect(url_for("application.step6"))

            extension = os.path.splitext(file.filename)[1]
            safe_name = secure_filename(record.qualification)
            filename = safe_name + extension
            filepath = os.path.join(education_folder, filename)
            file.save(filepath)

            if not academic_document:
                academic_document = StudentAcademicDocument(
                    student_id=student.student_id,
                    academic_id=record.id
                )
                student_db.session.add(academic_document)

            academic_document.document_name = filename
            academic_document.file_path = f"uploads/{student.application_no}/education/{filename}"

    if student.current_step < 6:
        student.current_step = 6

    student_db.session.commit()
    flash("Documents uploaded successfully.", "success")
    return redirect(url_for("application.step7"))


# =========================================================================
# STEP 7
# =========================================================================

@application_bp.route("/registration/step7")
def step7():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("auth.login"))

    response = check_step_access(student, 7)
    if response: return response
    
    personal = StudentPersonal.query.filter_by(student_id=student.student_id).first()
    address = StudentAddress.query.filter_by(student_id=student.student_id).first()
    family = StudentFamily.query.filter_by(student_id=student.student_id).first()
    documents = StudentDocuments.query.filter_by(student_id=student.student_id).first()

    if not documents:
        documents = StudentDocuments()

    document_fields = [
        "profile_photo", "signature", "aadhaar_card", "birth_certificate",
        "caste_certificate", "pwbd_certificate", "income_certificate",
        "domicile_certificate", "migration_certificate"
    ]
    for field in document_fields:
        value = getattr(documents, field, None)
        if value:
            setattr(documents, field, value.replace("\\", "/"))

    academic_records = StudentAcademic.query.filter_by(student_id=student.student_id).all()
    academic_documents = {}
    for record in academic_records:
        document = StudentAcademicDocument.query.filter_by(academic_id=record.id).first()
        if document and document.file_path:
            document.file_path = document.file_path.replace("\\", "/")
        academic_documents[record.id] = document

    return render_template(
        "auth/registration-step7.html",
        student=student, personal=personal, address=address, family=family,
        documents=documents, academic_records=academic_records,
        academic_documents=academic_documents
    )

@application_bp.route("/registration/step7", methods=["POST"])
def save_step7():
    student = StudentAccount.query.get(session.get("student_id"))
    if not student: return redirect(url_for("auth.login"))

    response = check_step_access(student, 7)
    if response: return response
    
    # --- BACKEND VALIDATION ---
    if "declaration" not in request.form:
        flash("Please accept the declaration before final submission.", "danger")
        return redirect(url_for("application.step7"))

    # Final sweep to ensure they haven't bypassed earlier steps
    if student.current_step < 6:
        flash("Application is incomplete. Please complete all previous steps.", "danger")
        return redirect(url_for("application.step6"))

    student.current_step = 7
    student.profile_completed = True
    student.is_final_submitted = True
    student_db.session.commit()

    if student.is_final_submitted:
        EmailService.send_email(
            to=student.email,
            subject="Registration Successful - Student Management Portal",
            template="emails/registration_success.html",
            name=student.full_name,
            application_no=student.application_no,
            login_url=url_for("auth.login", _external=True),
            year=datetime.now().year
        )
        flash("Application submitted successfully. You can now proceed to payment.", "success")
        return redirect(url_for("pages.dashboard"))

@application_bp.route("/view/step2")
def view_step2():

    student = StudentAccount.query.get(
        session.get("student_id")
    )

    if not student:
        return redirect(url_for("auth.login"))


    personal = StudentPersonal.query.filter_by(
        student_id=student.student_id
    ).first()


    genders = MasterGender.query.all()

    categories = MasterCategory.query.all()

    religions = MasterReligion.query.all()

    nationalities = MasterNationality.query.all()

    blood_groups = MasterBloodGroup.query.all()


    return render_template(
        "auth/registration-step2.html",
        student=student,
        personal=personal,
        genders=genders,
        categories=categories,
        religions=religions,
        nationalities=nationalities,
        blood_groups=blood_groups,
        view_mode=True
    )

@application_bp.route("/view/step3")
def view_step3():

    student = StudentAccount.query.get(
        session.get("student_id")
    )

    if not student:
        return redirect(url_for("auth.login"))


    academic_records = StudentAcademic.query.filter_by(
        student_id=student.student_id
    ).all()


    return render_template(
        "auth/registration-step3.html",
        student=student,
        academic_records=academic_records,
        view_mode=True
    )


@application_bp.route("/view/step4")
def view_step4():

    student = StudentAccount.query.get(
        session.get("student_id")
    )

    if not student:
        return redirect(url_for("auth.login"))


    address = StudentAddress.query.filter_by(
        student_id=student.student_id
    ).first()


    return render_template(
        "auth/registration-step4.html",
        student=student,
        address=address,
        view_mode=True
    )

@application_bp.route("/view/step5")
def view_step5():

    student = StudentAccount.query.get(
        session.get("student_id")
    )

    if not student:
        return redirect(url_for("auth.login"))


    family = StudentFamily.query.filter_by(
        student_id=student.student_id
    ).first()


    return render_template(
        "auth/registration-step5.html",
        student=student,
        family=family,
        view_mode=True
    )

@application_bp.route("/view/step6")
def view_step6():

    student = StudentAccount.query.get(
        session.get("student_id")
    )

    if not student:
        return redirect(url_for("auth.login"))

    documents = StudentDocuments.query.filter_by(
        student_id=student.student_id
    ).first()

    # Fix Windows paths
    if documents:

        document_fields = [

            "profile_photo",
            "signature",
            "aadhaar_card",
            "birth_certificate",
            "caste_certificate",
            "pwbd_certificate",
            "income_certificate",
            "domicile_certificate",
            "migration_certificate"

        ]

        for field in document_fields:

            value = getattr(documents, field, None)

            if value:

                setattr(
                    documents,
                    field,
                    value.replace("\\", "/")
                )

    academic_records = StudentAcademic.query.filter_by(
        student_id=student.student_id
    ).all()

    academic_documents = {}

    for record in academic_records:

        doc = StudentAcademicDocument.query.filter_by(
            academic_id=record.id
        ).first()

        if doc and doc.file_path:

            doc.file_path = doc.file_path.replace(
                "\\",
                "/"
            )

        academic_documents[record.id] = doc

    return render_template(
        "auth/registration-step6.html",
        student=student,
        documents=documents,
        academic_records=academic_records,
        academic_documents=academic_documents,
        view_mode=True
    )



@application_bp.route("/process-payment", methods=["POST"])
def process_payment():
    student = StudentAccount.query.get(session.get("student_id"))
    
    if not student:
        return redirect(url_for("auth.login"))
        
    if not student.is_final_submitted:
        flash("Please submit your application before proceeding to payment.", "danger")
        return redirect(url_for("pages.dashboard"))

    # ==========================================
    # FUTURE PAYMENT GATEWAY INTEGRATION HERE
    # ==========================================
    # Right now, fees are exempted (0 Rupees). 
    # Later, you will generate an order ID from Razorpay/Stripe here 
    # and redirect to a checkout page.
    
    student.payment_status = "Exempted" # Or "Completed"
    student_db.session.commit()
    
    flash("Payment processed successfully. Fees are currently exempted.", "success")
    return redirect(url_for("pages.dashboard"))


@application_bp.route("/download-application")
def download_application():
    student = StudentAccount.query.get(session.get("student_id"))
    
    if not student:
        return redirect(url_for("auth.login"))

    # Fetch all data to display on the form
    personal = StudentPersonal.query.filter_by(student_id=student.student_id).first()
    address = StudentAddress.query.filter_by(student_id=student.student_id).first()
    family = StudentFamily.query.filter_by(student_id=student.student_id).first()
    academic_records = StudentAcademic.query.filter_by(student_id=student.student_id).all()
    documents = StudentDocuments.query.filter_by(student_id=student.student_id).first()

    return render_template(
        "auth/print_application.html",
        student=student,
        personal=personal,
        address=address,
        family=family,
        academic_records=academic_records,
        documents=documents,
        now=datetime.now
    )
