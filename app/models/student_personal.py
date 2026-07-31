from app import student_db


class StudentPersonal(student_db.Model):

    __tablename__ = "student_personal"

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

    # Relationship
    account = student_db.relationship(
        "StudentAccount",
        back_populates="personal"
    )

    # -----------------------
    # Name
    # -----------------------

    first_name = student_db.Column(
        student_db.String(50),
        nullable=False
    )

    middle_name = student_db.Column(
        student_db.String(50)
    )

    last_name = student_db.Column(
        student_db.String(50)
    )

    # -----------------------
    # Personal Information
    # -----------------------

    gender_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("master_gender.id"),
        nullable=False
    )

    date_of_birth = student_db.Column(
        student_db.Date,
        nullable=False
    )

    blood_group_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("master_blood_group.id")
    )

    category_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("master_category.id"),
        nullable=False
    )

    religion_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("master_religion.id"),
        nullable=False
    )

    nationality_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("master_nationality.id"),
        nullable=False
    )

    aadhaar_no = student_db.Column(
        student_db.String(12),
        unique=True,
        nullable=False
    )

    # -----------------------
    # Contact Details
    # -----------------------

    alternate_email = student_db.Column(
        student_db.String(120)
    )

    alternate_mobile = student_db.Column(
        student_db.String(10)
    )

    # -----------------------
    # Parents
    # -----------------------

    father_name = student_db.Column(
        student_db.String(100)
    )

    father_mobile = student_db.Column(
        student_db.String(10)
    )

    mother_name = student_db.Column(
        student_db.String(100)
    )

    mother_mobile = student_db.Column(
        student_db.String(10)
    )

    guardian_name = student_db.Column(
        student_db.String(100)
    )

    guardian_mobile = student_db.Column(
        student_db.String(10)
    )

    # -----------------------
    # Foreign Key Relationships
    # -----------------------

    gender = student_db.relationship(
        "MasterGender"
    )

    blood_group = student_db.relationship(
        "MasterBloodGroup"
    )

    category = student_db.relationship(
        "MasterCategory"
    )

    religion = student_db.relationship(
        "MasterReligion"
    )

    nationality = student_db.relationship(
        "MasterNationality"
    )