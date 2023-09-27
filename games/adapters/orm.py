from sqlalchemy import (
    Table, MetaData, Integer, Column, Text, Float, String
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game

metadata = MetaData()

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('title', Text, nullable=False),
    Column('price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('description', String(255), nullable=False),
    Column('image_url', String(255), nullable=False),
    Column('website_url', String(255), nullable=False),
    # Column('publisher', 
)

def map_model_to_tables():
    mapper(Game, games_table, properties={
        '_game_id': games_table.c.game_id,
        '_title': games_table.c.title,
        '_price': games_table.c.price,
        '_release_date': games_table.c.release_date,
        '_description': games_table.c.description,
        '_image_url': games_table.c.image_url,
        '_website_url': games_table.c.website_url
    })
