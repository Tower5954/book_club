import uuid
import datetime
import functools
from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    current_app,
    url_for,
    flash
)
from dataclasses import asdict
from book_club.forms import (
    BookForm,
    ExtendedBookForm,
    RegisterForm,
    LoginForm
)
from book_club.models import Book, Bookworm
from passlib.hash import pbkdf2_sha256

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper


@pages.route("/")
@login_required
def index():
    bookworm_data = current_app.db.user.find_one({"email": session["email"]})
    bookworm = Bookworm(**bookworm_data)

    book_data = current_app.db.book.find({"_id": {"$in": bookworm.books} })
    books = [Book(**book) for book in book_data]
    return render_template(
        "index.html",
        title="Livrelist",
        books_data=books
    )

@pages.route("/register", methods=["GET", "POST"])
def register():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = RegisterForm()

    if form.validate_on_submit():
        bookworm = Bookworm(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )

        current_app.db.user.insert_one(asdict(bookworm))

        flash("Bookworm registered successfully", "success")

        return redirect(url_for(".login"))

    return render_template(
        "register.html",
        title="Livrelist - Register",
        form=form
    )

@pages.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = LoginForm()

    if form.validate_on_submit():
        bookworm_data = current_app.db.user.find_one({"email": form.email.data})
        if not bookworm_data:
            flash("Login credentials not correct :( ", category="danger")
            return redirect(url_for(".login"))
        bookworm = Bookworm(**bookworm_data)

        if bookworm and pbkdf2_sha256.verify(form.password.data, bookworm.password):
            session["bookworm_id"] = bookworm._id
            session["email"] = bookworm.email

            return redirect(url_for(".index"))

        flash("Login credentials not correct :( ", category="danger")

    return render_template("login.html", title="Livrelist - Login", form=form)

@pages.route("/logout")
def logout():
    # del session["bookworm_id"]
    # del session["email"]

    # session.clear()

    current_theme = session.get("theme")
    session.clear()
    session["theme"] = current_theme

    return redirect(url_for(".login"))


@pages.route("/add", methods=["GET", "POST"])
@login_required
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
        current_app.db.user.update_one(
            {"_id": session["bookworm_id"]}, {"$push": {"books": book._id }}
        )
        return redirect(url_for(".index"))

    return render_template(
        "new_book.html",
        title="Livrelist - Add Book",
        form=form
    )

@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
@login_required
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
@login_required
def rate_book(_id):
    rating = int(request.args.get("rating"))
    current_app.db.book.update_one({"_id": _id}, {"$set": {"rating": rating}})

    return redirect(url_for(".book", _id=_id))


@pages.get("/book/<string:_id>/read")
@login_required
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
