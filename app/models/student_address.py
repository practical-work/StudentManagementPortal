from app import student_db


class StudentAddress(student_db.Model):

    __tablename__ = "student_address"

    id = student_db.Column(
        student_db.Integer,
        primary_key=True
    )

    student_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("student_accounts.student_id"),
        nullable=False,
        unique=True
    )

    # Permanent Address

    permanent_address = student_db.Column(
        student_db.Text,
        nullable=False
    )

    permanent_state = student_db.Column(
        student_db.String(100),
        nullable=False
    )

    permanent_district = student_db.Column(
        student_db.String(100),
        nullable=False
    )

    permanent_city = student_db.Column(
        student_db.String(100),
        nullable=False
    )

    permanent_pincode = student_db.Column(
        student_db.String(6),
        nullable=False
    )

    # Correspondence Address

    correspondence_address = student_db.Column(
        student_db.Text,
        nullable=False
    )

    correspondence_state = student_db.Column(
        student_db.String(100),
        nullable=False
    )

    correspondence_district = student_db.Column(
        student_db.String(100),
        nullable=False
    )

    correspondence_city = student_db.Column(
        student_db.String(100),
        nullable=False
    )

    correspondence_pincode = student_db.Column(
        student_db.String(6),
        nullable=False
    )

    account = student_db.relationship(
        "StudentAccount"
    )