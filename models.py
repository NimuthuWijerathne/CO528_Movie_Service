# models.py
class Movie:
    def __init__(self, id, title, director, year):
        self.id = id
        self.title = title
        self.director = director
        self.year = year

# In-memory movie storage
movies = {}
next_id = 1
