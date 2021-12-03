from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)


class ReviewPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(500), nullable=False)
    game_title = db.Column(db.String(500), nullable=False)
    game_review = db.Column(db.String(2500), nullable=False)
    game_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Review' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        review_author = request.form["author"]
        review_title = request.form["gtitle"]
        review_review = request.form["greview"]
        review_score = request.form["gscore"]
        new_review = ReviewPost(author_name=review_author, game_title=review_title, game_review=review_review, game_score=review_score)
        db.session.add(new_review)
        db.session.commit()
        return redirect('/reviews')
    else:
        all_reviews = ReviewPost.query.order_by(ReviewPost.game_title).all()
        return render_template('reviews.html', reviews=all_reviews)


@app.route('/reviews/delete/<int:id>')
def delete(id):
    review = ReviewPost.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return redirect('/reviews')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
