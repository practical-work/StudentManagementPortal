from app import create_app,student_db
from sqlalchemy import inspect

# Import Models
from app.models.student_account import StudentAccount
from app.models.student_personal import StudentPersonal
from app.models.email_otp import EmailOTP
from app.models import student_account,student_personal
from app.routes.auth import auth_bp
from app.routes.pages import pages_bp
from app.routes.forgot_password import forgot_bp
from app.routes.application import application_bp
from app.routes.retrieve_application import retrieve_bp
from app.models.master_religion import MasterReligion
from app.models.master_blood_group import MasterBloodGroup
from app.models.master_category import MasterCategory
from app.models.master_gender import MasterGender
from app.models.master_nationality import MasterNationality
from app.models.student_personal import StudentPersonal


app = create_app()

def seed(model, field_name, values):

    if model.query.count() == 0:

        for value in values:
            obj = model()

            setattr(obj, field_name, value)

            student_db.session.add(obj)

        student_db.session.commit()

        print(f"{model.__tablename__} seeded.")

    else:
        print(f"{model.__tablename__} already contains data.")



with app.app_context():
    student_db.create_all()
    print("Tables Created Successfully.")

    inspector = inspect(student_db.engine)
    print(inspector.get_table_names())

    seed(
            MasterGender,
            "gender_name",
            [
                "Male",
                "Female",
                "Other"
            ]
        )
    
    seed(
            MasterCategory,
            "category_name",
            [
                "General",
                "EWS",
                "OBC",
                "SC",
                "ST"
            ]
        )
    
    seed(
            MasterReligion,
            "religion_name",
            [
                "Hindu",
                "Muslim",
                "Sikh",
                "Christian",
                "Jain",
                "Buddhist",
                "Parsi",
                "Other"
            ]
        )
    
    seed(
            MasterNationality,
            "nationality_name",
            [
                "Indian"
            ]
        )
    
    seed(
            MasterBloodGroup,
            "blood_group_name",
            [
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ]
        )
    
    print("Master data seeded successfully.")



if __name__ == "__main__":
    app.run(debug=False)