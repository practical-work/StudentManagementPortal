from app import student_db
from sqlalchemy.sql import func


class StudentAcademicDocument(student_db.Model):

    __tablename__ = "student_academic_documents"

    academic_document_id = student_db.Column(
        student_db.Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("student_accounts.student_id"),
        nullable=False
    )

    academic_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("student_academic.id"),
        nullable=False,
        unique=True
    )

    document_name = student_db.Column(
        student_db.String(150)
    )

    file_path = student_db.Column(
        student_db.String(255),
        nullable=False
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
        "StudentAccount"
    )

    academic = student_db.relationship(
        "StudentAcademic"
    )