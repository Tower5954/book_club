import uuid
import datetime

from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    current_app,
    url_for )
from dataclasses import asdict
from book_club.forms import BookForm, ExtendedBookForm
from book_club.models import Book


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    book_data = current_app.db.book.find({})
    books = [Book(**book) for book in book_data]
    return render_template(
        "index.html",
        title="Livrelist",
        books_data=books
    )


@pages.route("/add", methods=["GET", "POST"])
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        book = Book(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            author=form.author.data,
            year=form.year.data
        )

        current_app.db.book.insert_one(asdict(book))

        return redirect(url_for(".index"))

    return render_template(
        "new_book.html",
        title="Livrelist - Add Book",
        form=form
    )

@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
def edit_book(_id: str):
    book = Book(**current_app.db.book.find_one({"_id": _id}))
    form = ExtendedBookForm(obj=book)
    if form.validate_on_submit():
        book.characters = form.characters.data
        book.series = form.series.data
        book.tags = form.tags.data
        book.description = form.description.data
        book.image_link = form.image_link.data

        current_app.db.book.update_one({"_id": book._id}, {"$set": asdict(book)})
        return redirect(url_for(".book", _id=book._id))
    return render_template("book_form.html", book=book, form=form)


@pages.get("/book/<string:_id>")
def book(_id: str):
    book = Book(**current_app.db.book.find_one({"_id": _id}))
    return render_template("book_details.html", book=book)


@pages.get("/book/<string:_id>/rate")
def rate_book(_id):
    rating = int(request.args.get("rating"))
    current_app.db.book.update_one({"_id": _id}, {"$set": {"rating": rating}})

    return redirect(url_for(".book", _id=_id))


@pages.get("/book/<string:_id>/read")
def read_today(_id):
    current_app.db.book.update_one(
        {"_id": _id},
        {"$set": {"last_read": datetime.datetime.today()}}
    )

    return redirect(url_for(".book", _id=_id))


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
