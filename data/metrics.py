import sqlalchemy
from .db_session import SqlAlchemyBase


class Metrics(SqlAlchemyBase):
    __tablename__ = 'metrics'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    start = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    close = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    stop = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    posts = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    events = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    site = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    help = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
