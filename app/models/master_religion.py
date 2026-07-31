from app import student_db


class MasterReligion(student_db.Model):

    __tablename__ = "master_religion"

    id = student_db.Column(
        student_db.Integer,
        primary_key=True
    )

    religion_name = student_db.Column(
        student_db.String(50),
        unique=True,
        nullable=False
    )