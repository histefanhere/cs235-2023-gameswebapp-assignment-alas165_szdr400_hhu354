from sqlalchemy import (
    Table, MetaData, Integer, Column, Text, Float, String, Boolean, PickleType, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Publisher, Game

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
    Column('description', String(255), nullable=False),
    Column('image_url', String(255), nullable=False),
    Column('website_url', String(255), nullable=False),
    Column('windows', Boolean, nullable=False),
    Column('mac', Boolean, nullable=False),
    Column('linux', Boolean, nullable=False),
    Column('categories', PickleType, nullable=False),
    Column('publisher_name', ForeignKey('publishers.name'))
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
        '_Game__windows': games_table.c.windows,
        '_Game__mac': games_table.c.mac,
        '_Game__linux': games_table.c.linux,
        '_Game__categories': games_table.c.categories,
        '_Game__publisher': relationship(Publisher)
    })
