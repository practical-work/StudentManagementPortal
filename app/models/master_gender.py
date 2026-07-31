from app import student_db


class MasterGender(student_db.Model):

    __tablename__ = "master_gender"

    id = student_db.Column(
        student_db.Integer,
        primary_key=True
    )

    gender_name = student_db.Column(
        student_db.String(20),
        unique=True,
        nullable=False
    )