from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym
from capitulo.domain import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()


users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=True),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('publisher', String(255), nullable=False),
    Column('release_year', Integer, nullable=False),
    Column('num_pages', Integer, nullable=False),
    Column('image_hyperlink', String(255), nullable=False),
    Column('language', String(255), nullable=False),
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', Integer, nullable=False),
    Column('author_full_name', String(255), nullable=False)
)


def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user'),
        #'_User__reading_list': relationship(model.User, backref='_User__reading_list')
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review': reviews_table.c.review,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(model.Book, books_table, properties={
        '_Book__id': books_table.c.id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__publisher': books_table.c.publisher,
        '_Book__release_year': books_table.c.release_year,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__image_hyperlink': books_table.c.image_hyperlink,
        '_Book__language': books_table.c.language,
        '_Book__reviews': relationship(model.Review, backref='_Review__book'),
    })
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__id': publishers_table.c.id,
        '_Publisher__name': publishers_table.c.name
    })
    mapper(model.Author, authors_table, properties={
        '_Author__author_id': authors_table.c.author_id,
        '_Author__author_full_name': authors_table.c.author_full_name
    })