from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from app.models import Todo, db

view_bp = Blueprint("view", __name__)


@view_bp.route("", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        title = request.form.get("title") or ""
        content = request.form.get("content") or ""
        is_done = request.form.get("is-done") or False

        if len(content.strip()) == 0:
            flash("Please add some content.", category="error")

        else:
            new_todo = Todo(title=title, content=content, is_done=is_done, user_id=current_user.id)  # type: ignore

            db.session.add(new_todo)
            db.session.commit()

    return render_template("home.html", user=current_user), 200


@view_bp.route("/create")
@login_required
def create_todo():
    return render_template("create.html", user=current_user)


@view_bp.route("/update-todo/<int:id>", methods=["GET", "POST"])
@login_required
def update_todo(id):
    todo = Todo.query.get(int(id))

    if request.method == "POST" and todo is not None:
        todo.title = request.form.get("title")
        todo.content = request.form.get("content")
        todo.is_done = request.form.get("is-done")

        db.session.commit()

    return render_template("update.html", todo=todo, user=current_user), 200


@view_bp.route("/delete-todo", methods=["DELETE"])
@login_required
def delete_todo():
    data = request.json

    if data and "id" in data:
        todo = Todo.query.get(data["id"])

        if todo:
            if todo.user_id == current_user.id:
                db.session.delete(todo)
                db.session.commit()

                flash("Todo deleted successfully!", "success")
                return redirect(url_for("view.home")), 200

            else:
                flash("You are not authorized to delete this todo.", "error")
                return jsonify({"message": "Unauthorized"}), 403
        else:
            flash("Todo item not found!", "error")
            return jsonify({"message": "Todo not found"}), 404

    flash("Invalid request data.", "error")
    return jsonify({"message": "Invalid request data"}), 400
