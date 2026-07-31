# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
#     MAIL_SERVER = "smtp.gmail.com"
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.getenv("MAIL_USERNAME")
#     MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
#     MAIL_DEFAULT_SENDER = ("Student Management Portal",os.getenv("MAIL_USERNAME"))


import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # Automatically grab Railway's MYSQL_URL, or fall back to a local/custom DATABASE_URL
    database_url = os.getenv("MYSQL_URL") or os.getenv("DATABASE_URL")
    
    # SQLAlchemy requires 'mysql+pymysql://' for MySQL connections
    if database_url and database_url.startswith("mysql://"):
        database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
        
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Student Management Portal", os.getenv("MAIL_USERNAME"))