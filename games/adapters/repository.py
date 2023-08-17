import abc
from typing import List

from games.domainmodel.model import Game


repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f"RepositoryException: {message}")


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        """ Add a game to the repository list of games. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """ Returns the list of games. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_games(self):
        """ Returns the number of games that exist in the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_tags(self) -> list[str]:
        """ Returns the list of tags. """
        raise NotImplementedError
