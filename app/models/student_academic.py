from app import student_db


class StudentAcademic(student_db.Model):

    __tablename__ = "student_academic"

    id = student_db.Column(
        student_db.Integer,
        primary_key=True
    )

    student_id = student_db.Column(
        student_db.Integer,
        student_db.ForeignKey("student_accounts.student_id"),
        nullable=False
    )

    account = student_db.relationship(
        "StudentAccount",
        backref="academic_details"
    )

    qualification = student_db.Column(
        student_db.String(100),
        nullable=False
    )
    # Example:
    # Class 10
    # Class 12
    # Diploma
    # Graduation
    # B.Tech
    # B.Sc
    # M.Tech
    # Other

    board_university = student_db.Column(
        student_db.String(150),
        nullable=False
    )

    institute_name = student_db.Column(
        student_db.String(200),
        nullable=False
    )

    roll_number = student_db.Column(
        student_db.String(50)
    )

    registration_number = student_db.Column(
        student_db.String(50)
    )

    stream = student_db.Column(
        student_db.String(100)
    )

    medium = student_db.Column(
        student_db.String(50)
    )

    passing_year = student_db.Column(
        student_db.Integer,
        nullable=False
    )

    marks_type = student_db.Column(
        student_db.String(20)
    )
    # Percentage / CGPA

    percentage = student_db.Column(
        student_db.Float
    )

    cgpa = student_db.Column(
        student_db.Float
    )

    total_marks = student_db.Column(
        student_db.Float
    )

    obtained_marks = student_db.Column(
        student_db.Float
    )

    subjects = student_db.Column(
        student_db.Text
    )

    entrance_exam = student_db.Column(
        student_db.String(100)
    )

    entrance_roll_number = student_db.Column(
        student_db.String(50)
    )

    entrance_rank = student_db.Column(
        student_db.String(50)
    )

    entrance_score = student_db.Column(
        student_db.String(50)
    )