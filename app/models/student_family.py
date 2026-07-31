from app import student_db
from sqlalchemy.sql import func


class StudentFamily(student_db.Model):

    __tablename__ = "student_family"


    family_id = student_db.Column(
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


    # Occupation Details

    father_occupation = student_db.Column(
        student_db.String(100)
    )


    mother_occupation = student_db.Column(
        student_db.String(100)
    )


    guardian_occupation = student_db.Column(
        student_db.String(100)
    )



    # Twin Information

    is_twin = student_db.Column(
        student_db.Boolean,
        default=False
    )


    twin_name = student_db.Column(
        student_db.String(100)
    )


    twin_relation = student_db.Column(
        student_db.String(50)
    )



    # Freedom Fighter

    is_freedom_fighter = student_db.Column(
        student_db.Boolean,
        default=False
    )


    freedom_fighter_name = student_db.Column(
        student_db.String(100)
    )


    freedom_fighter_relation = student_db.Column(
        student_db.String(100)
    )


    freedom_fighter_certificate_no = student_db.Column(
        student_db.String(100)
    )



    # NCC Details

    is_ncc_candidate = student_db.Column(
        student_db.Boolean,
        default=False
    )


    ncc_certificate_no = student_db.Column(
        student_db.String(100)
    )


    ncc_level = student_db.Column(
        student_db.String(50)
    )



    # Criminal Case

    criminal_case = student_db.Column(
        student_db.Boolean,
        default=False
    )


    criminal_case_details = student_db.Column(
        student_db.Text
    )



    # Candidate Information


    is_ex_servicemen = student_db.Column(
        student_db.Boolean,
        default=False
    )


    ex_servicemen_details = student_db.Column(
        student_db.Text
    )



    is_pwbd = student_db.Column(
        student_db.Boolean,
        default=False
    )


    pwbd_category = student_db.Column(
        student_db.String(100)
    )


    pwbd_certificate_no = student_db.Column(
        student_db.String(100)
    )



    # Residence


    domicile_status = student_db.Column(
        student_db.String(100)
    )


    domicile_state = student_db.Column(
        student_db.String(100)
    )



    # Marital Status


    marital_status = student_db.Column(
        student_db.String(50)
    )



    # Other

    created_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now()
    )


    updated_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )