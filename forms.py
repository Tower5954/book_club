from flask_wtf import FlaskForm
from wtforms import  IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class BookForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    author = StringField("Author", validators=[InputRequired()])

    year = IntegerField("Year", validators=[InputRequired(),
                                            NumberRange(min=0, message="Please enter a year in the format YYYY.")]
                        )

    submit = SubmitField("Add Book")
