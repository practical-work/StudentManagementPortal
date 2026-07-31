from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,check_password_hash
import random

from app import student_db
from app.models.student_account import StudentAccount
from app.models.email_otp import EmailOTP
from services.email_service import EmailService

retrieve_bp = Blueprint("retrieve", __name__)


@retrieve_bp.route("/retrieve-application", methods=["GET"])
def retrieve_application():

    retrieve = session.get("retrieve_application")

    if not retrieve:
        return render_template(
            "auth/retrieve-application.html",
            otp_sent=False
        )

    otp_record = EmailOTP.query.filter_by(
        email=retrieve["email"],
        is_verified=False
    ).first()

    if otp_record:

        remaining_seconds = int(
            (otp_record.expires_at - datetime.now()).total_seconds()
        )

        if remaining_seconds < 0:
            remaining_seconds = 0

        return render_template(
            "auth/retrieve-application.html",
            otp_sent=True,
            email=retrieve["email"],
            remaining_seconds=remaining_seconds
        )

    return render_template(
        "auth/retrieve-application.html",
        otp_sent=False
    )


@retrieve_bp.route("/retrieve-application/step1", methods=["POST"])
def step1():

    search_type = request.form.get("search_type")
    value = request.form.get("value", "").strip()

    student = None

    if search_type == "email":
        student = StudentAccount.query.filter_by(
            email=value.lower()
        ).first()

    elif search_type == "mobile":
        student = StudentAccount.query.filter_by(
            mobile=value
        ).first()

    if not student:
        flash("No student found.", "danger")
        return redirect(url_for("retrieve.retrieve_application"))

    session["retrieve_application"] = {
        "student_id": student.student_id,
        "application_no": student.application_no,
        "email": student.email,
        "full_name": student.full_name
    }

    EmailOTP.query.filter_by(
        email=student.email
    ).delete()

    student_db.session.commit()

    otp = str(random.randint(100000, 999999))

    otp_record = EmailOTP(
        email=student.email,
        otp=otp,
        expires_at=datetime.now() + timedelta(minutes=5),
        is_verified=False
    )

    student_db.session.add(otp_record)
    student_db.session.commit()

    EmailService.send_email(
        to=student.email,
        subject="Retrieve Application Number OTP",
        template="emails/retrieve_otp.html",
        otp=otp,
        name=student.full_name,
        year=datetime.now().year
    )

    flash("OTP sent successfully.", "success")

    return redirect(url_for("retrieve.retrieve_application"))


@retrieve_bp.route("/retrieve-application/verify-otp", methods=["POST"])
def verify_otp():

    entered_otp = request.form.get("entered_otp", "").strip()

    retrieve = session.get("retrieve_application")

    if not retrieve:
        flash("Session expired.", "danger")
        return redirect(url_for("retrieve.retrieve_application"))

    otp_record = EmailOTP.query.filter_by(
        email=retrieve["email"],
        is_verified=False
    ).first()

    if not otp_record:
        flash("OTP not found.", "danger")
        return redirect(url_for("retrieve.retrieve_application"))

    if otp_record.expires_at < datetime.now():
        flash("OTP expired.", "danger")
        return redirect(url_for("retrieve.retrieve_application"))

    if otp_record.otp != entered_otp:

        remaining_seconds = int(
            (otp_record.expires_at - datetime.now()).total_seconds()
        )

        if remaining_seconds < 0:
            remaining_seconds = 0

        flash("Invalid OTP.", "danger")

        return render_template(
            "auth/retrieve-application.html",
            otp_sent=True,
            email=retrieve["email"],
            remaining_seconds=remaining_seconds
        )

    # OTP Verified
    otp_record.is_verified = True
    student_db.session.commit()

    return redirect(url_for("retrieve.show_application"))



@retrieve_bp.route("/retrieve-application/show")
def show_application():

    retrieve = session.get("retrieve_application")

    if not retrieve:
        flash("Session expired.", "danger")
        return redirect(url_for("retrieve.retrieve_application"))

    student = StudentAccount.query.get(
        retrieve["student_id"]
    )

    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("retrieve.retrieve_application"))

    # Delete OTP
    EmailOTP.query.filter_by(
        email=student.email
    ).delete()

    student_db.session.commit()

    # Clear Session
    session.pop("retrieve_application", None)

    return render_template(
        "auth/application-retrieved.html",
        full_name=student.full_name,
        application_no=student.application_no,
        email=student.email,
        mobile=student.mobile
    )



@retrieve_bp.route("/retrieve-application/resend-otp", methods=["POST"])
def resend_otp():

    retrieve = session.get("retrieve_application")

    if not retrieve:
        flash("Session expired.", "danger")
        return redirect(url_for("retrieve.retrieve_application"))

    email = retrieve["email"]

    # Delete old OTP
    EmailOTP.query.filter_by(email=email).delete()
    student_db.session.commit()

    # Generate New OTP
    otp = str(random.randint(100000, 999999))

    otp_record = EmailOTP(
        email=email,
        otp=otp,
        expires_at=datetime.now() + timedelta(minutes=2),   # or 5 minutes
        is_verified=False
    )

    student_db.session.add(otp_record)
    student_db.session.commit()

    remaining_seconds = int(
        (otp_record.expires_at - datetime.now()).total_seconds()
    )

    if remaining_seconds < 0:
        remaining_seconds = 0

    # Send Email
    EmailService.send_email(
        to=email,
        subject="Retrieve Application OTP",
        template="emails/retrieve_resend_otp.html",
        otp=otp,
        name=retrieve["full_name"],
        year=datetime.now().year
    )

    flash("A new OTP has been sent to your email.", "success")

    return redirect(url_for("retrieve.retrieve_application"))