from flask_wtf import FlaskForm
from wtforms import  IntegerField, StringField, SubmitField, TextAreaField, URLField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo


class BookForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    author = StringField("Author", validators=[InputRequired()])

    year = IntegerField(
        "Year",
        validators=[
            InputRequired(),
            NumberRange(min=0, message="Please enter a year in the format YYYY.")
                    ]
        )

    submit = SubmitField("Add Book")


class StringListField(TextAreaField):
    def _value(self):
        if self.data:
            return "\n".join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []

class ExtendedBookForm(BookForm):
    characters = StringListField("Characters")
    series = StringListField("Series")
    tags = StringListField("Tags")
    description = StringListField("Description")
    image_link = URLField("Video link")

    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password",
    validators=[
        InputRequired(),
        Length(
            min=8,
            max=40,
            message="Your password must be between 8 and 40 characters long."
        )
    ])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo(
                "password",
                message="We are sorry. However, this password did not match the one in the password field."
            )
        ]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")