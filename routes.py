from flask import Blueprint, render_template, session, request, redirect
from book_club.forms import BookForm

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    return render_template(
        "index.html",
        title="Livrelist",
    )


@pages.route("/add", methods=["GET", "POST"])
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        pass

    return render_template(
        "new_book.html",
        title="Livrelist - Add Book",
        form=form
    )


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
