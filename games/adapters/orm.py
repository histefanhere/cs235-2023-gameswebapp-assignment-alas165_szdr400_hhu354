from sqlalchemy import (
    Table, MetaData, Integer, Column, Text, Float, String, Boolean, PickleType, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Publisher, Game, Genre, Tag

metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True, nullable=False)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('description', String(255), nullable=True),
    Column('image_url', String(255), nullable=False),
    Column('website_url', String(255), nullable=True),
    Column('recommendations', Integer, nullable=False),
    Column('windows', Boolean, nullable=False),
    Column('mac', Boolean, nullable=False),
    Column('linux', Boolean, nullable=False),
    Column('categories', PickleType, nullable=False),
    Column('achievements', Integer, nullable=False),
    Column('developer', String(255), nullable=False),
    Column('screenshots', PickleType, nullable=False),
    Column('movies', PickleType, nullable=False),
    Column('publisher_name', ForeignKey('publishers.name'))
)

genres_table = Table(
    'genres', metadata,
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

tags_table = Table(
    'tags', metadata,
    Column('tag_name', String(64), primary_key=True, nullable=False)
)

game_tags_table = Table(
    'game_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('tag_name', ForeignKey('tags.tag_name'))
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(64), nullable=False),
    Column('password', String(64), nullable=False),
    Column('wishlist', ForeignKey('games.game_id'))
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('game_id', ForeignKey('games.game_id'), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('comment', String(255), nullable=False),
    Column('timestamp', PickleType, nullable=False)    
)

wishlists_table = Table(
    'wishlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False)
)

wishlist_games_table = Table(
    'wishlist_games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('wishlist_id', ForeignKey('wishlists.id'), nullable=False),
    Column('game_id', ForeignKey('games.game_id'), nullable=False)
)


def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__recommendations': games_table.c.recommendations,
        '_Game__windows': games_table.c.windows,
        '_Game__mac': games_table.c.mac,
        '_Game__linux': games_table.c.linux,
        '_Game__categories': games_table.c.categories,
        '_Game__achievements': games_table.c.achievements,
        '_Game__developer': games_table.c.developer,
        '_Game__screenshots': games_table.c.screenshots,
        '_Game__movies': games_table.c.movies,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__tags': relationship(Tag, secondary=game_tags_table)
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name
    })

    mapper(Tag, tags_table, properties={
        '_Tag__tag_name': tags_table.c.tag_name
    })

    # Mapper needs to be done for User, review and wishlist.
