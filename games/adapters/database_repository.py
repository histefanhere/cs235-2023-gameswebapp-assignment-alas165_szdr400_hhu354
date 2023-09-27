from pathlib import Path
from typing import List

from sqlalchemy.orm import scoped_session

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Review, User


# This manages the session to the database and lets us very simply interface with SQLAlchemy
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class DatabaseRepository(AbstractRepository):
    def __init__(self, session_factory):
        self.__scm = SessionContextManager(session_factory)

    def add_game(self, game: Game):
        """ Add a game to the repository list of games. """
        pass
    
    def get_games(self) -> List[Game]:
        """ Returns the list of games. """
        pass
    
    def get_game(self, id: int) -> Game:
        """ Returns the game with the given id from the repository. """
        pass
    
    def get_number_of_games(self):
        """ Returns the number of games that exist in the repository. """
        pass
    
    def get_genres(self) -> list[Genre]:
        """ Returns the list of genres. """
        pass

    def get_tags(self) -> list[str]:
        """ Returns the list of tags. """
        pass

    def search_games(self, price: float = float('inf'),
                    #  release_date: (int, str idk),
                    tags: list[str] = None,
                    recommendations: int = 0,
                    genre: Genre = None ) -> list[Game]:
        """ Returns the list of games that match the given criteria. """
        pass
    
    def get_user(self, username: str):
        """ Gets a user from the repository. """
        pass
    
    def add_user(self, user):
        """ Adds a user to the repository. """
        pass
    
    def add_review(self, review):
        """ Adds a review to the repository. """
        pass


def populate(data_path: Path, repo: AbstractRepository):
    pass
