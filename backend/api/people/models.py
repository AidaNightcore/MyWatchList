from api.common.database import db
from sqlalchemy.orm import relationship


class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))


class Franchise(db.Model):
    __tablename__ = 'Franchise'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))

    # Relationships
    books = relationship('Book', back_populates='franchise')
    movies = relationship('Movie', back_populates='franchise')
    shows = relationship('Show', back_populates='franchise')


class Publisher(db.Model):
    __tablename__ = 'Publisher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    # Relationships
    books = relationship('Book', back_populates='publisher')
    movies = relationship('Movie', back_populates='publisher')
    shows = relationship('Show', back_populates='publisher')


class Type(db.Model):
    __tablename__ = 'Type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))

    # Relationships
    books = relationship('Book', back_populates='media_type')
    movies = relationship('Movie', back_populates='media_type')
    episodes = relationship('Episode', back_populates='media_type')


class Title(db.Model):
    __tablename__ = 'Titles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    elementType = db.Column(db.Integer, db.ForeignKey('Type.id'))

    # Relationships
    media_type = relationship('Type', back_populates='titles')
    watch_elements = relationship('WatchElement', back_populates='title')
    topics = relationship('Topic', back_populates='title')
    crew = relationship('Crew', back_populates='title')


class Book(db.Model):
    __tablename__ = 'Book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    typeID = db.Column(db.Integer, db.ForeignKey('Type.id'))
    genreID = db.Column(db.Integer, db.ForeignKey('Genre.id'))
    franchiseID = db.Column(db.Integer, db.ForeignKey('Franchise.id'))
    publisherID = db.Column(db.Integer, db.ForeignKey('Publisher.id'))
    ageRating = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))
    publishDate = db.Column(db.Date)

    # Relationships
    media_type = relationship('Type', back_populates='books')
    genre = relationship('Genre', back_populates='books')
    franchise = relationship('Franchise', back_populates='books')
    publisher = relationship('Publisher', back_populates='books')


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    typeID = db.Column(db.Integer, db.ForeignKey('Type.id'))
    genreID = db.Column(db.Integer, db.ForeignKey('Genre.id'))
    franchiseID = db.Column(db.Integer, db.ForeignKey('Franchise.id'))
    publisherID = db.Column(db.Integer, db.ForeignKey('Publisher.id'))
    ageRating = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))
    publishDate = db.Column(db.Date)

    # Relationships
    media_type = relationship('Type', back_populates='movies')
    genre = relationship('Genre', back_populates='movies')
    franchise = relationship('Franchise', back_populates='movies')
    publisher = relationship('Publisher', back_populates='movies')


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    genreID = db.Column(db.Integer, db.ForeignKey('Genre.id'))
    franchiseID = db.Column(db.Integer, db.ForeignKey('Franchise.id'))
    publisherID = db.Column(db.Integer, db.ForeignKey('Publisher.id'))
    ageRating = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))

    # Relationships
    genre = relationship('Genre', back_populates='shows')
    franchise = relationship('Franchise', back_populates='shows')
    publisher = relationship('Publisher', back_populates='shows')
    seasons = relationship('Season', back_populates='show')


class Season(db.Model):
    __tablename__ = 'Season'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    showID = db.Column(db.Integer, db.ForeignKey('Show.id'))
    seasonNumber = db.Column(db.Integer)
    synopsis = db.Column(db.String(255))
    publishDate = db.Column(db.Date)
    episodeCount = db.Column(db.Integer)

    # Relationships
    show = relationship('Show', back_populates='seasons')
    episodes = relationship('Episode', back_populates='season')


class Episode(db.Model):
    __tablename__ = 'Episode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    typeID = db.Column(db.Integer, db.ForeignKey('Type.id'))
    ageRating = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))
    publishDate = db.Column(db.Date)
    seasonID = db.Column(db.Integer, db.ForeignKey('Season.id'))

    # Relationships
    media_type = relationship('Type', back_populates='episodes')
    season = relationship('Season', back_populates='episodes')