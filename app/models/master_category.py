from app import student_db


class MasterCategory(student_db.Model):

    __tablename__ = "master_category"

    id = student_db.Column(
        student_db.Integer,
        primary_key=True
    )

    category_name = student_db.Column(
        student_db.String(30),
        unique=True,
        nullable=False
    )