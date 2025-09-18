from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("login.html")

@auth_bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Credenciales incorrectas", "error")
        return redirect(url_for("auth.login"))
    login_user(user, remember=True)
    return redirect(url_for("main.dashboard"))

@auth_bp.get("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("register.html")

@auth_bp.post("/register")
def register_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if not name or not email or not password:
        flash("Completa todos los campos", "error")
        return redirect(url_for("auth.register"))
    if User.query.filter_by(email=email).first():
        flash("El correo ya está registrado", "error")
        return redirect(url_for("auth.register"))

    user = User(name=name, email=email, role="standard")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash("Registro exitoso. Inicia sesión.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
