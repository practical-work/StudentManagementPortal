from app import create_app, student_db

from app.models.master_gender import MasterGender
from app.models.master_category import MasterCategory
from app.models.master_religion import MasterReligion
from app.models.master_nationality import MasterNationality
from app.models.master_blood_group import MasterBloodGroup

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