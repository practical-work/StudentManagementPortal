from app import student_db
from sqlalchemy.sql import func


class StudentDocuments(student_db.Model):

    __tablename__ = "student_documents"

    document_id = student_db.Column(
        student_db.Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("student_accounts.student_id"),
        nullable=False,
        unique=True
    )

    # Personal Documents

    profile_photo = student_db.Column(
        student_db.String(255)
    )

    signature = student_db.Column(
        student_db.String(255)
    )

    aadhaar_card = student_db.Column(
        student_db.String(255)
    )

    birth_certificate = student_db.Column(
        student_db.String(255)
    )

    # Category / Reservation

    caste_certificate = student_db.Column(
        student_db.String(255)
    )

    pwbd_certificate = student_db.Column(
        student_db.String(255)
    )

    income_certificate = student_db.Column(
        student_db.String(255)
    )

    domicile_certificate = student_db.Column(
        student_db.String(255)
    )

    migration_certificate = student_db.Column(
        student_db.String(255)
    )

    created_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now()
    )

    updated_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    student = student_db.relationship(
        "StudentAccount",
        backref="documents"
    )