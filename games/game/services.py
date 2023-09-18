import datetime
from flask import session

from games.domainmodel.model import Game, Review, User
from games.adapters.repository import AbstractRepository

def get_game_data(repo: AbstractRepository, game_id):
    game = repo.get_game(game_id)
    # no, i refuse to do that weird game object to dict thing
    return game

def add_review(repo: AbstractRepository, game_id: int, rating: int, comment: str):
    user = repo.get_user(session['username'])
    game = repo.get_game(game_id)

    rev = Review(user, game, rating, comment, datetime.date.today())
    user.add_review(rev)
    game.add_review(rev)
    repo.add_review(rev)
