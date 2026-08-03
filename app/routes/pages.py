from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models.student_account import StudentAccount
from app.models.student_documents import StudentDocuments

pages_bp = Blueprint("pages", __name__)


# About
@pages_bp.route("/about")
def about():
    return render_template("pages/about.html")


# Notices
@pages_bp.route("/notices")
def notices():
    return render_template("pages/notices.html", initial_notices=[])


# Courses
@pages_bp.route("/courses")
def courses():
    return render_template("pages/courses.html")


# Admissions
@pages_bp.route("/admissions")
def admissions():
    return render_template("pages/admissions.html")


# Student Dashboard
# Student Dashboard
@pages_bp.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect(url_for("auth.login"))

    student = StudentAccount.query.get(session["student_id"])

    if not student:
        flash("Student not found.", "danger")
        session.clear()
        return redirect(url_for("auth.login"))

    # ----------------------------
    # Fix profile photo path
    # ----------------------------
    documents = StudentDocuments.query.filter_by(
        student_id=student.student_id
    ).first()

    if documents and documents.profile_photo:
        documents.profile_photo = documents.profile_photo.replace("\\", "/")

    # ----------------------------
    # Progress Calculation
    # ----------------------------
    progress = int((student.current_step / 7) * 100)

    # ----------------------------
    # Dashboard Steps
    # ----------------------------
    steps = [

        {
            "step": 2,
            "title": "Personal Details",
            "edit": "application.step2",
            "view": "application.view_step2"
        },

        {
            "step": 3,
            "title": "Academic Details",
            "edit": "application.step3",
            "view": "application.view_step3"
        },

        {
            "step": 4,
            "title": "Address Details",
            "edit": "application.step4",
            "view": "application.view_step4"
        },

        {
            "step": 5,
            "title": "Family Details",
            "edit": "application.step5",
            "view": "application.view_step5"
        },

        {
            "step": 6,
            "title": "Documents Upload",
            "edit": "application.step6",
            "view": "application.view_step6"
        },

        {
            "step": 7,
            "title": "Final Submission",
            "edit": "application.step7",
            "view": None
        }

    ]

    return render_template(

        "pages/dashboard.html",

        student=student,

        documents=documents,

        progress=progress,

        steps=steps,

        view_mode=True
    )

# Results
@pages_bp.route("/results")
def results():
    return render_template("pages/results.html")


# Attendance
@pages_bp.route("/attendance")
def attendance():
    return render_template("pages/attendance.html")


# Study Material
@pages_bp.route("/study-material")
def study_material():
    return render_template("pages/study_material.html")


#timetable
@pages_bp.route('/timetable')
def timetable():
    # If a student or admin searches, fetch from database. 
    # For now, setting timetable_data=True renders the grid, setting it to False triggers the Empty State.
    has_timetable = True 
    
    return render_template('pages/timetable.html', timetable_data=has_timetable)

# Fees
@pages_bp.route("/fees")
def fees():
    return render_template("pages/fees.html")


# Certificates
@pages_bp.route("/certificates")
def certificates():
    return render_template("pages/certificates.html")


# Assignments
@pages_bp.route("/assignments")
def assignments():
    return render_template("pages/assignments.html")


# Faculty
@pages_bp.route("/faculty")
def faculty():
    return render_template("pages/faculty.html")


# Contact
@pages_bp.route("/contact")
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Optional: You can save this to a database model or send an email here
        
        # Flash success message to show on the same page
        flash('Thank you! Your message has been sent successfully. We will get back to you soon.', 'success')
        return redirect(url_for('pages.contact'))
        
    return render_template('pages/contact.html')

# Help / FAQ
@pages_bp.route("/help")
def help():
    return render_template("pages/help.html")
