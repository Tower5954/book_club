from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    current_app,
    url_for )
from book_club.forms import BookForm
import uuid

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
        book = {
            "_id": uuid.uuid4().hex,
            "title": form.title.data,
            "author": form.author.data,
            "year": form.year.data
        }

        current_app.db.book.insert_one(book)

        return redirect(url_for(".index"))

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
