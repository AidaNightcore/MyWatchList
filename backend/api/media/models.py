from api.common.database import db
from sqlalchemy.orm import relationship
from api.watchlist.models import WatchlistItem

class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    titles = db.relationship('Title', secondary='TitleGenre', back_populates='genres')

class TitleGenre(db.Model):
    __tablename__ = 'TitleGenre'
    genreID = db.Column(db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
    titleID = db.Column(db.Integer, db.ForeignKey('Titles.id'), primary_key=True)

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
    elementTypeName = db.Column('elementTypeName', db.String(255))

    # Relationships
    books = relationship('Book', back_populates='media_type')
    movies = relationship('Movie', back_populates='media_type')
    episodes = relationship('Episode', back_populates='media_type')
    titles = relationship('Title', back_populates='media_type')


class Title(db.Model):
    __tablename__ = 'Titles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    elementType = db.Column(db.Integer, db.ForeignKey('Type.id'))

    # Relationships
    media_type = relationship('Type', back_populates='titles')
    genres = relationship('Genre', secondary='TitleGenre', back_populates='titles')
    watch_elements = relationship(
        WatchlistItem,
        back_populates = 'title',
        cascade = 'all, delete-orphan'
    )
    topics = relationship('Topic', back_populates='title')
    crew = relationship('Crew', back_populates='title')

    @property
    def genre_names(self):
        return [genre.name for genre in self.genres]


class Book(db.Model):
    __tablename__ = 'Book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    typeID = db.Column(db.Integer, db.ForeignKey('Type.id'))
    franchiseID = db.Column(db.Integer, db.ForeignKey('Franchise.id'), nullable=True)
    publisherID = db.Column(db.Integer, db.ForeignKey('Publisher.id'))
    ageRating = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))
    publishDate = db.Column(db.Date)
    isbnID = db.Column(db.String(20))
    goodreadsID = db.Column(db.String(20))
    pages = db.Column(db.Integer)

    # Relationships
    media_type = relationship('Type', back_populates='books')
    franchise = relationship('Franchise', back_populates='books')
    publisher = relationship('Publisher', back_populates='books')

    @property
    def genres(self):
        return list({
            genre
            for title in self.media_type.titles
            for genre in title.genres
        })

    @property
    def crew(self):
        crew_set = set()
        for title in self.media_type.titles:
            crew_set.update(title.crew)
        return [{
            'job': member.job.title,
            'worker': member.job.worker.name
        } for member in crew_set]


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    typeID = db.Column(db.Integer, db.ForeignKey('Type.id'))
    franchiseID = db.Column(db.Integer, db.ForeignKey('Franchise.id'))
    publisherID = db.Column(db.Integer, db.ForeignKey('Publisher.id'))
    ageRating = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))
    publishDate = db.Column(db.Date)
    imdbID = db.Column(db.Integer)

    # Relationships
    media_type = relationship('Type', back_populates='movies')
    franchise = relationship('Franchise', back_populates='movies')
    publisher = relationship('Publisher', back_populates='movies')

    @property
    def genres(self):
        return list({
            genre
            for title in self.media_type.titles
            for genre in title.genres
        })

    @property
    def crew(self):
        crew_set = set()
        for title in self.media_type.titles:
            crew_set.update(title.crew)
        return [{
            'job': member.job.title,
            'worker': member.job.worker.name
        } for member in crew_set]


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    franchiseID = db.Column(db.Integer, db.ForeignKey('Franchise.id'))
    publisherID = db.Column(db.Integer, db.ForeignKey('Publisher.id'))
    ageRating = db.Column(db.String(255))
    synopsis = db.Column(db.String(255))
    imdbID = db.Column(db.Integer)

    # Relationships
    franchise = relationship('Franchise', back_populates='shows')
    publisher = relationship('Publisher', back_populates='shows')
    seasons = relationship('Season', back_populates='show')

    @property
    def genres(self):
        genre_set = set()
        for season in self.seasons:
            for episode in season.episodes:
                genre_set.update(episode.genres)
        return list(genre_set)

    @property
    def crew(self):
        crew_set = set()
        for season in self.seasons:
            for episode in season.episodes:
                crew_set.update(episode.crew)
        return list(crew_set)


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

    @property
    def genres(self):
        genre_set = set()
        for season in self.seasons:
            for episode in season.episodes:
                genre_set.update(episode.genres)
        return list(genre_set)

    @property
    def crew(self):
        crew_set = set()
        for season in self.seasons:
            for episode in season.episodes:
                crew_set.update(episode.crew)
        return list(crew_set)


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

    @property
    def genres(self):
        return list({
            genre
            for title in self.media_type.titles
            for genre in title.genres
        })

    @property
    def crew(self):
        crew_set = set()
        for title in self.media_type.titles:
            crew_set.update(title.crew)
        return [{
            'job': member.job.title,
            'worker': member.job.worker.name
        } for member in crew_set]



