from app import student_db
from sqlalchemy.sql import func

class StudentPayment(student_db.Model):

    __tablename__ = "student_payments"

    payment_id = student_db.Column(
        student_db.Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("student_accounts.student_id"),
        nullable=False
    )

    amount = student_db.Column(
        student_db.Float,
        default=0.0
    )

    payment_status = student_db.Column(
        student_db.Enum(
            "Pending",
            "Success",
            "Failed",
            "Refunded"
        ),
        default="Pending"
    )

    payment_reference = student_db.Column(student_db.String(100))
    transaction_id = student_db.Column(student_db.String(100))
    gateway_name = student_db.Column(student_db.String(50))

    payment_date = student_db.Column(student_db.DateTime)

    created_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now()
    )