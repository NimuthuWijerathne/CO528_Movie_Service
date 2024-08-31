from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return{
            'id': self.id,
            'title': self.title,
            'director': self.director,
            'year': self.year
        }
with app.app_context():
    db.create_all()


@app.route('/movies', methods=['POST'])
def create_movie():
    if not request.json or not 'title' in request.json:
        abort(400)
    new_movie = Movie(
        title=request.json['title'],
        director=request.json.get('director', ""),
        year=request.json.get('year', None)
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'movie': new_movie.to_dict()}), 201


@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({'movie': movie.to_dict()})

@app.route('/movies', methods=['GET'])
def list_movies():
    movies = Movie.query.all()
    return jsonify({'movies': [movie.to_dict() for movie in movies]})

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if not request.json:
        abort(400)
    movie.title = request.json.get('title', movie.title)
    movie.director = request.json.get('director', movie.director)
    movie.year = request.json.get('year', movie.year)
    db.session.commit()
    return jsonify({'movie': movie.to_dict()})


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
    
