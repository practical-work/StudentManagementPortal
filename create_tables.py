# from app import create_app, student_db
# from sqlalchemy import inspect

# # Import Models
# from app.models.student_account import StudentAccount
# from app.models.student_personal import StudentPersonal
# from app.models.email_otp import EmailOTP

# from app.models.master_gender import MasterGender
# from app.models.master_category import MasterCategory
# from app.models.master_religion import MasterReligion
# from app.models.master_nationality import MasterNationality
# from app.models.master_blood_group import MasterBloodGroup

# app = create_app()

# with app.app_context():

#     student_db.create_all()

#     print("Tables Created Successfully.")

#     inspector = inspect(student_db.engine)
#     print(inspector.get_table_names())