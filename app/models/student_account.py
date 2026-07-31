from app import student_db
from sqlalchemy.sql import func

class StudentAccount(student_db.Model):

    __tablename__ = "student_accounts"

    student_id = student_db.Column(
        student_db.Integer,
        primary_key=True,
        autoincrement=True
    )

    application_no = student_db.Column(
        student_db.String(20),
        unique=True,
        nullable=True
    )

    full_name = student_db.Column(
        student_db.String(150),
        nullable=False
    )

    # Primary Email (Never Editable)
    email = student_db.Column(
        student_db.String(120),
        unique=True,
        nullable=False
    )

    # Primary Mobile (Never Editable)
    mobile = student_db.Column(
        student_db.String(10),
        unique=True,
        nullable=False
    )

    password = student_db.Column(
        student_db.String(255),
        nullable=False
    )

    # Profile Photo Path
    profile_photo = student_db.Column(
        student_db.String(255)
    )

    is_email_verified = student_db.Column(
        student_db.Boolean,
        default=False
    )

    is_mobile_verified = student_db.Column(
        student_db.Boolean,
        default=False
    )

    current_step = student_db.Column(
        student_db.Integer,
        default=1
    )

    profile_completed = student_db.Column(
        student_db.Boolean,
        default=False
    )

    is_final_submitted = student_db.Column(
        student_db.Boolean,
        default=False
    )

    is_active = student_db.Column(
        student_db.Boolean,
        default=True
    )
    
    payment_status = student_db.Column(student_db.String(50), default="Pending")

    created_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now()
    )

    updated_at = student_db.Column(
        student_db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    personal = student_db.relationship(
        "StudentPersonal",
        back_populates="account",
        uselist=False,
        cascade="all, delete-orphan"
    )