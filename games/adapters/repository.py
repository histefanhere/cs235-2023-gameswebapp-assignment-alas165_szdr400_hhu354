import abc
from typing import List

from games.domainmodel.model import Game, Genre


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
    def get_game(self, id: int) -> Game:
        """ Returns the game with the given id from the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_games(self):
        """ Returns the number of games that exist in the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_genres(self) -> list[Genre]:
        """ Returns the list of genres. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tags(self) -> list[str]:
        """ Returns the list of tags. """
        raise NotImplementedError
    
    # @abc.abstractmethod # Should probably be dealt with by services not repo.
    # def get_random_tags(self, n: int) -> list[str]:
    #     """ Returns a list of n random tags. """
    #     raise NotImplementedError
    
    @abc.abstractmethod
    def get_games_with_tags(self, tags: list[str]) -> list[Game]:
        """ Returns the list of games that have all the given tags. """
        raise NotImplementedError

    @abc.abstractmethod
    def search_games(self, price: float = float('inf'),
                    #  release_date: (int, str idk),
                    tags: list[str] = None,
                    recommendations: int = 0,
                    genre: Genre = None ) -> list[Game]:
        """ Returns the list of games that match the given criteria. """
        raise NotImplementedError
