from flask import Blueprint, render_template, request, flash, session,redirect,url_for
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,check_password_hash
import random

from app import student_db
from app.models.student_account import StudentAccount
from app.models.email_otp import EmailOTP
from services.email_service import EmailService


forgot_bp = Blueprint("forgot", __name__)

@forgot_bp.route("/forgot-password",methods=["GET"])
def forgot_password():
    if session.get("otp_verified"):
       return redirect(url_for("forgot.reset_password"))
    forgot_password = session.get("forgot_password")
    
    if not forgot_password:
            return render_template(
                "auth/forgot-password.html",
                otp_sent=False
            )
    
    otp_record = EmailOTP.query.filter_by(
            email=forgot_password["email"],
            is_verified=False
        ).first()
    
    if otp_record:
    
            remaining_seconds = int(
                (otp_record.expires_at - datetime.now()).total_seconds()
            )
    
            if remaining_seconds < 0:
                remaining_seconds = 0
    
            return render_template(
                "auth/forgot-password.html",
                otp_sent=True,
                application_no=forgot_password["application_no"],
                email=forgot_password["email"],
                remaining_seconds=remaining_seconds
            )
    
    return render_template(
            "auth/forgot-password.html",
            otp_sent=False
        )

@forgot_bp.route("/forgot-password/step1", methods=["POST"])
def step1():

    application_no = request.form.get("application_no", "").strip().upper()
    email = request.form.get("email", "").strip().lower()

    # Check Student
    student = StudentAccount.query.filter_by(
        application_no=application_no,
        email=email
    ).first()

    if not student:
        flash("Invalid Application Number or Email.", "danger")

        return render_template(
            "auth/forgot-password.html"
        )

    # Save Session
    session["forgot_password"] = {
        "student_id": student.student_id,
        "application_no": application_no,
        "email": email,
        "full_name" : student.full_name
    }

    # Delete Old OTP
    EmailOTP.query.filter_by(email=email).delete()
    student_db.session.commit()

    # Generate OTP
    otp = str(random.randint(100000,999999))

    otp_record = EmailOTP(
        email=email,
        otp=otp,
        expires_at=datetime.now() + timedelta(minutes=5),
        is_verified=False
    )

    student_db.session.add(otp_record)
    student_db.session.commit()

    # Remaining Time
    remaining_seconds = int(
        (otp_record.expires_at - datetime.now()).total_seconds()
    )

    if remaining_seconds < 0:
        remaining_seconds = 0

    # Send Email
    EmailService.send_email(
        to=email,
        subject="Password Reset OTP",
        template="emails/forgot_otp.html",
        otp=otp,
        name=student.full_name,
        year=datetime.now().year
    )

    flash("OTP sent successfully.", "success")
    return redirect(url_for("forgot.forgot_password"))



@forgot_bp.route("/forgot-password/verify-otp", methods=["POST"])
def verify_otp():

    entered_otp = request.form.get("entered_otp", "").strip()

    forgot = session.get("forgot_password")

    if not forgot:
        flash("Session expired.", "danger")
        return redirect(url_for("forgot.forgot_password"))

    otp_record = EmailOTP.query.filter_by(
        email=forgot["email"],
        is_verified=False
    ).first()

    if not otp_record:
        flash("OTP not found.", "danger")
        return redirect(url_for("forgot.forgot_password"))

    if otp_record.expires_at < datetime.now():
        flash("OTP expired.", "danger")
        return redirect(url_for("forgot.forgot_password"))

    if otp_record.otp != entered_otp:
        flash("Invalid OTP.", "danger")
        remaining_seconds = int((otp_record.expires_at - datetime.now()).total_seconds())
        if remaining_seconds < 0:
            remaining_seconds = 0
        return render_template(
            "auth/forgot-password.html",
            otp_sent=True,
            application_no=forgot["application_no"],
            email=forgot["email"],
            remaining_seconds=remaining_seconds
        )

    otp_record.is_verified = True
    student_db.session.commit()

    session["otp_verified"] = True

    print(session)
    
    flash("OTP Verified Successfully.", "success")
    return redirect(url_for("forgot.reset_password"))



@forgot_bp.route("/forgot-password/resend-otp", methods=["POST"])
def resend_otp():

    forgot_password = session.get("forgot_password")

    if not forgot_password:
        flash("Registration session expired.", "danger")
        return redirect(url_for("auth.registration"))

    email = forgot_password["email"]

    # Delete old OTP
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
    session["otp_sent_time"] = datetime.now().timestamp()
    student_db.session.commit()

    remaining_seconds = int(
    (otp_record.expires_at - datetime.now()).total_seconds()
)

    if remaining_seconds < 0:
        remaining_seconds = 0

    # Send Email
    EmailService.send_email(
        to=email,
        subject="OTP Verification",
        template="emails/forgot_resend_otp.html",
        otp=otp,
        name=forgot_password["full_name"],
        year=datetime.now().year
    )

    flash("A new OTP has been sent to your email.", "success")

    return redirect(url_for("forgot.forgot_password"))


@forgot_bp.route("/forgot-password/reset", methods=["GET", "POST"])
def reset_password():

    forgot = session.get("forgot_password")

    if not forgot:
        flash("Session expired.", "danger")
        return redirect(url_for("forgot.forgot_password"))

    if not session.get("otp_verified"):
        flash("Verify OTP first.", "danger")
        return redirect(url_for("forgot.forgot_password"))

    # Show page first
    if request.method == "GET":
        return render_template(
            "auth/reset-password.html",
            application_no=forgot["application_no"]
        )

    # POST starts here
    password = request.form.get("password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    if password != confirm_password:
        flash("Passwords do not match.", "danger")

        return render_template(
            "auth/reset-password.html",
            application_no=forgot["application_no"]
        )

    student = StudentAccount.query.get(forgot["student_id"])

    student.password = generate_password_hash(password)

    student_db.session.commit()

    EmailOTP.query.filter_by(email=forgot["email"]).delete()
    student_db.session.commit()

    session.pop("forgot_password", None)
    session.pop("otp_verified", None)

    flash("Password changed successfully. Please login.", "success")

    return redirect(url_for("auth.login"))