from flask import Blueprint, render_template, g, request, url_for, redirect, flash
from decorators import login_required
from .form import QuestionForm
from models import QuestionModel
from exts import db

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/question/public", methods=["GET", "POST"])
@login_required
def public_question():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误!")
            return redirect(url_for("qa.public_question"))