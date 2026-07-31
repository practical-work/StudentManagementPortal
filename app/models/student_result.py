from app import student_db
from sqlalchemy.sql import func

class StudentResult(student_db.Model):

    __tablename__ = "student_results"

    result_id = student_db.Column(
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

    total_marks = student_db.Column(student_db.Float)
    obtained_marks = student_db.Column(student_db.Float)
    percentage = student_db.Column(student_db.Float)
    grade = student_db.Column(student_db.String(10))
    rank = student_db.Column(student_db.Integer)

    result_status = student_db.Column(
        student_db.Enum(
            "Pass",
            "Fail",
            "Absent",
            "Withheld"
        )
    )

    published_at = student_db.Column(student_db.DateTime)

    created_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now()
    )