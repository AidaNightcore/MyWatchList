from sqlalchemy.orm import relationship

from api import db


class Worker(db.Model):
    __tablename__ = 'Worker'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    # Relationships
    jobs = relationship('Job', back_populates='worker')


class Job(db.Model):
    __tablename__ = 'Job'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    workerID = db.Column(db.Integer, db.ForeignKey('Worker.id'))

    # Relationships
    worker = relationship('Worker', back_populates='jobs')
    crew = relationship('Crew', back_populates='job')


class Crew(db.Model):
    __tablename__ = 'Crew'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titleID = db.Column(db.Integer, db.ForeignKey('Titles.id'))
    jobID = db.Column(db.Integer, db.ForeignKey('Job.id'))

    # Relationships
    title = relationship('Title', back_populates='crew')
    job = relationship('Job', back_populates='crew')