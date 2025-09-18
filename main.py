from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Question

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def index():
    # landing (sin sesión)
    if hasattr(current_user, "is_authenticated") and current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")

@main_bp.get("/dashboard")
@login_required
def dashboard():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template("dashboard.html", questions=questions)

@main_bp.post("/ask")
@login_required
def ask():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    if not title:
        flash("El título es obligatorio", "error")
        return redirect(url_for("main.dashboard"))
    q = Question(title=title, body=body, user_id=current_user.id)
    db.session.add(q)
    db.session.commit()
    flash("Pregunta publicada", "success")
    return redirect(url_for("main.dashboard"))
