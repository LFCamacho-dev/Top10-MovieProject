from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# import requests


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/movies.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/main_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.VARCHAR(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.VARCHAR(120), nullable=False)
    img_url = db.Column(db.VARCHAR(120), nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.title


class RateMovieForm(FlaskForm):
    rating = StringField('Your Rating Out Of 10 e.g. 7.5')
    review = StringField('Your Review')
    submit = SubmitField('Submit')

def add_to_db(): # used to add data to database manually
    new_movie = Movies(
        title="Phone Booth 2, the revenge",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by "
                    "an extortionist's sniper rifle. Unable to leave or receive outside help, "
                    "Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        rating=10,
        ranking=8,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    )
    db.session.add(new_movie)
    db.session.commit()

# add_to_db()


# --------------- ROUTES ---------------------

@app.route("/")
def home():
    all_movies = db.session.query(Movies).all()

    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movies.query.get(movie_id)
    if form.validate_on_submit() and request.method == 'POST':
        movie.rating = request.form["rating"]
        movie.review = request.form["review"]

        # UPDATE A PARTICULAR RECORD BY QUERY
        # book_to_update = Book.query.filter_by(title="Harry Potter").first()
        # book_to_update.title = "Harry Potter and the Chamber of Secrets"
        # db.session.commit()
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete", methods=["GET", "POST"])
def delete_movie():
    movie_id = request.args.get("id")
    movie_to_delete = Movies.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
