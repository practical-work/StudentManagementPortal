from app import student_db
from sqlalchemy.sql import func


class EmailOTP(student_db.Model):
    __tablename__ = "email_otps"

    otp_id = student_db.Column(student_db.Integer, primary_key=True)

    email = student_db.Column(student_db.String(100), nullable=False)

    otp = student_db.Column(student_db.String(6), nullable=False)

    expires_at = student_db.Column(student_db.DateTime, nullable=False)

    is_verified = student_db.Column(student_db.Boolean, default=False)

    created_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now()
    )