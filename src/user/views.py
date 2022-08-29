from flask import render_template, send_file, request, session, redirect
from user.models import User
from auth.routes import protected
from auth.auth_level import AuthLevel

@protected(AuthLevel.Student, redirect="profile")
def profile_get():
    user = User.query.filter_by(student_id=int(session["studentid"])).first()
    return render_template("user/profile.html", session=session, studentid=user.student_id , first_name=user.first_name, last_name=user.last_name)
