from app import student_db


class MasterBloodGroup(student_db.Model):

    __tablename__ = "master_blood_group"

    id = student_db.Column(
        student_db.Integer,
        primary_key=True
    )

    blood_group_name = student_db.Column(
        student_db.String(5),
        unique=True,
        nullable=False
    )