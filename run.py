from app import create_app,student_db
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

with app.app_context():
    student_db.create_all()


if __name__ == "__main__":
    app.run(debug=False)