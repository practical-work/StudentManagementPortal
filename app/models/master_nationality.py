from app import student_db


class MasterNationality(student_db.Model):

    __tablename__ = "master_nationality"

    id = student_db.Column(
        student_db.Integer,
        primary_key=True
    )

    nationality_name = student_db.Column(
        student_db.String(50),
        unique=True,
        nullable=False
    )