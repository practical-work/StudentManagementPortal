from app import student_db
from sqlalchemy.sql import func

class StudentAdmitCard(student_db.Model):

    __tablename__ = "student_admit_cards"

    admit_card_id = student_db.Column(
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

    admit_card_no = student_db.Column(
        student_db.String(50),
        unique=True
    )

    exam_name = student_db.Column(student_db.String(100))
    exam_center = student_db.Column(student_db.String(255))
    center_code = student_db.Column(student_db.String(30))
    room_no = student_db.Column(student_db.String(30))
    seat_no = student_db.Column(student_db.String(30))

    exam_date = student_db.Column(student_db.Date)
    reporting_time = student_db.Column(student_db.Time)
    exam_time = student_db.Column(student_db.Time)

    download_count = student_db.Column(
        student_db.Integer,
        default=0
    )

    created_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now()
    )