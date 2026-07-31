from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import mail
from app.Protections import csrf
from flask import flash, redirect, request, url_for,render_template
from flask_wtf.csrf import CSRFProtect, CSRFError

# create instance of SQLAlchemy/database
student_db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # configure database
    app.config.from_object("app.config.Config")

    # connect db with app
    student_db.init_app(app)
    
    # connect google SMTP for email
    mail.init_app(app)
     
    csrf.init_app(app)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):

        flash(
            "Your session has expired or the form is invalid. Please try again.",
            "warning"
        )

        return redirect(request.referrer or url_for("auth.login"))

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):

        return (
            render_template(
                "errors/400.html",
                reason=e.description
            ),
            400
        )
    @app.errorhandler(400)
    def bad_request(e):

        return (
            render_template("errors/400.html"),
            400
        )

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template("errors/401.html"), 401


    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return (
                render_template("errors/404.html"),
                404
            )
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template("errors/405.html"), 405


    @app.errorhandler(500)
    def internal_server_error(e):
        student_db.session.rollback()
        return render_template("errors/500.html"), 500

    
    # register blueprints
    # Import routes AFTER creating student_db
    from app.routes.auth import auth_bp
    from app.routes.pages import pages_bp
    from app.routes.forgot_password import forgot_bp
    from app.routes.application import application_bp
    from app.routes.retrieve_application import retrieve_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(forgot_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(retrieve_bp)

    # return flask application
    return app