from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import re

from app import student_db
from app.models.student_account import StudentAccount
from app.models.email_otp import EmailOTP
from services.email_service import EmailService

auth_bp = Blueprint("auth", __name__)


# ==========================================
# HOME 
# ==========================================
@auth_bp.route("/")
def home():
    return render_template("index.html")


# ==========================================
# REGISTRATION PAGE (GET)
# ==========================================
@auth_bp.route("/registration", methods=["GET"])
def registration(): 
    registration = session.get("registration")

    if not registration:
        return render_template("auth/registration.html", otp_sent=False)

    otp_record = EmailOTP.query.filter_by(
        email=registration["email"],
        is_verified=False
    ).first()

    if otp_record:
        remaining_seconds = int((otp_record.expires_at - datetime.now()).total_seconds())
        if remaining_seconds < 0:
            remaining_seconds = 0

        return render_template(
            "auth/registration.html",
            otp_sent=True,
            full_name=registration["full_name"],
            email=registration["email"],
            mobile=registration["mobile"],
            remaining_seconds=remaining_seconds
        )

    return render_template("auth/registration.html", otp_sent=False)


# ==========================================
# STEP 1 : SEND OTP (POST)
# ==========================================
@auth_bp.route("/registration/step1", methods=["POST"])
def step1():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip().lower()
    mobile = request.form.get("mobile", "").strip()
    password = request.form.get("password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    # --- 1. Empty Fields Validation ---
    if not full_name or not email or not mobile or not password or not confirm_password:
        flash("All fields are mandatory.", "danger")
        return render_template("auth/registration.html", otp_sent=False)

    # --- 2. Email Format Validation ---
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        flash("Please enter a valid email address.", "danger")
        return render_template("auth/registration.html", otp_sent=False)

    # --- 3. Mobile Number Validation ---
    if len(mobile) != 10 or not mobile.isdigit():
        flash("Enter a valid 10 digit mobile number.", "danger")
        return render_template("auth/registration.html", otp_sent=False)

    # --- 4. Password Validation ---
    if len(password) < 6:
        flash("Password must be at least 6 characters long.", "danger")
        return render_template("auth/registration.html", otp_sent=False)

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return render_template("auth/registration.html", otp_sent=False)

    # --- 5. Check Duplicates in DB ---
    existing_student = StudentAccount.query.filter(
        (StudentAccount.email == email) |
        (StudentAccount.mobile == mobile)
    ).first()

    if existing_student:
        flash("Email or Mobile Number already registered.", "danger")
        return render_template("auth/registration.html", otp_sent=False)

    hashed_password = generate_password_hash(password)

    # Save temporarily in session
    session["registration"] = {
        "full_name": full_name,
        "email": email,
        "mobile": mobile,
        "password": hashed_password
    }

    # Delete any previous unused OTPs for this email to prevent spam
    EmailOTP.query.filter_by(email=email).delete()
    student_db.session.commit()

    # Generate new OTP
    otp = str(random.randint(100000, 999999))

    otp_record = EmailOTP(
        email=email,
        otp=otp,
        expires_at=datetime.now() + timedelta(minutes=5),
        is_verified=False
    )

    student_db.session.add(otp_record)
    student_db.session.commit()

    # Send Email
    try:
        EmailService.send_email(
            to=email,
            subject="OTP Verification",
            template="emails/otp.html",
            otp=otp,
            name=full_name
        )
        flash("OTP sent successfully.", "success")
    except Exception as e:
        flash("Failed to send OTP. Please check your email address.", "danger")

    return redirect(url_for("auth.registration"))


# ==========================================
# VERIFY OTP
# ==========================================
@auth_bp.route("/registration/verify-otp", methods=["POST"])
def verify_otp():
    entered_otp = request.form.get("entered_otp", "").strip()
    registration = session.get("registration")

    if not entered_otp:
        flash("Please enter the OTP.", "danger")
        return redirect(url_for("auth.registration"))

    if not registration:
        flash("Registration session expired. Please start again.", "danger")
        return redirect(url_for("auth.registration"))

    otp_record = EmailOTP.query.filter_by(
        email=registration["email"],
        is_verified=False
    ).first()

    if not otp_record:
        flash("OTP not found or already verified.", "danger")
        return redirect(url_for("auth.registration"))

    if otp_record.expires_at < datetime.now():
        flash("OTP expired. Please request a new OTP.", "danger")
        return redirect(url_for("auth.registration"))

    if otp_record.otp != entered_otp:
        flash("Invalid OTP.", "danger")
        remaining_seconds = int((otp_record.expires_at - datetime.now()).total_seconds())
        return render_template(
            "auth/registration.html",
            otp_sent=True,
            full_name=registration["full_name"],
            email=registration["email"],
            mobile=registration["mobile"],
            remaining_seconds=max(remaining_seconds, 0)
        )

    # Mark OTP verified
    otp_record.is_verified = True
    student_db.session.commit()

    # Create Student
    student = StudentAccount(
        full_name=registration["full_name"],
        email=registration["email"],
        mobile=registration["mobile"],
        password=registration["password"]
    )

    student_db.session.add(student)
    student_db.session.commit()

    # Generate Application Number safely
    student.application_no = f"SMP2026{student.student_id:06d}"
    student_db.session.commit()

    # Delete OTP to clean up DB
    student_db.session.delete(otp_record)
    student_db.session.commit()
    
    # Send Welcome Email
    try:
        EmailService.send_email(
            to=student.email,
            subject="Application Created Successfully - Student Management Portal",
            template="emails/registration.html",
            name=student.full_name,
            application_no=student.application_no,
            login_url=url_for("auth.login", _external=True),
            year=datetime.now().year
        )
    except Exception as e:
        pass # Account is created, so we don't block them if the welcome email fails

    # Login User
    session.pop("registration", None)
    session["student_id"] = student.student_id
    session["application_no"] = student.application_no
    session["logged_in"] = True

    flash("Application account created successfully.", "success")
    return redirect(url_for("auth.application"))


# ==========================================
# RESEND OTP
# ==========================================
@auth_bp.route("/registration/resend-otp", methods=["POST"])
def resend_otp():
    registration = session.get("registration")

    if not registration:
        flash("Application session expired. Please start again.", "danger")
        return redirect(url_for("auth.registration"))

    email = registration["email"]

    # Delete old OTP to prevent abuse
    EmailOTP.query.filter_by(email=email).delete()
    student_db.session.commit()

    # Generate New OTP
    otp = str(random.randint(100000, 999999))

    otp_record = EmailOTP(
        email=email,
        otp=otp,
        expires_at=datetime.now() + timedelta(minutes=5),
        is_verified=False
    )

    student_db.session.add(otp_record)
    student_db.session.commit()

    # Send Email
    try:
        EmailService.send_email(
            to=email,
            subject="OTP Verification",
            template="emails/resend-otp.html",
            otp=otp,
            name=registration["full_name"],
            year=datetime.now().year
        )
        flash("A new OTP has been sent to your email.", "success")
    except Exception as e:
        flash("Failed to send OTP. Please try again.", "danger")
        
    return redirect(url_for("auth.registration"))


# ==========================================
# APPLICATION RETRIEVED / SUCCESS
# ==========================================
@auth_bp.route("/registration/application")
def application():
    student = StudentAccount.query.get(session.get("student_id"))

    if not student:
        flash("Student not found. Please log in.", "danger")
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/application.html",
        application_no=student.application_no,
        full_name=student.full_name,
        email=student.email,
        mobile=student.mobile
    )


# ==========================================
# CONTINUE APPLICATION (ROUTER)
# ==========================================
@auth_bp.route("/continue")
def continue_application():
    if "student_id" not in session:
        return redirect(url_for("auth.login"))

    student = StudentAccount.query.get(session["student_id"])

    if not student:
        session.clear() # Clear bad session
        flash("Session invalid. Please log in again.", "danger")
        return redirect(url_for("auth.login"))

    # Safely route to the correct step based on DB state
    if student.current_step == 1: return redirect(url_for("application.step2"))
    elif student.current_step == 2: return redirect(url_for("application.step3"))
    elif student.current_step == 3: return redirect(url_for("application.step4"))
    elif student.current_step == 4: return redirect(url_for("application.step5"))
    elif student.current_step == 5: return redirect(url_for("application.step6"))
    elif student.current_step == 6: return redirect(url_for("application.step7"))
    
    return redirect(url_for("pages.dashboard"))


# ==========================================
# LOGIN
# ==========================================
@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    
    if request.method == "POST":
        application_no = request.form.get("application_no", "").strip().upper()
        password = request.form.get("password", "").strip()

        # Validate empty inputs
        if not application_no or not password:
            flash("Application Number and Password are required.", "danger")
            return redirect(url_for("auth.login"))

        student = StudentAccount.query.filter_by(application_no=application_no).first()

        # Check if student exists AND password is correct
        if not student or not check_password_hash(student.password, password):
            # Use a generic error message for BOTH wrong username and wrong password
            # This prevents attackers from "guessing" valid Application Numbers.
            flash("Invalid Application Number or Password.", "danger")
            return redirect(url_for("auth.login"))

        # Setup Secure Session
        session.permanent = True  # Enable session expiration
        session["student_id"] = student.student_id
        session["application_no"] = student.application_no
        session["logged_in"] = True

        flash("Login Successful.", "success")
        return redirect(url_for("pages.dashboard"))


# ==========================================
# LOGOUT
# ==========================================
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))