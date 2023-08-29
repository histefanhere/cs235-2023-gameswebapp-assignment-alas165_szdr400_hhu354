import os
from bisect import insort_left
from typing import List

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__tags = list()
        self.__genres = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            # When inserting the game, keep the game list sorted alphabetically by the id.
            # Games will be sorted by game due to __lt__ method of the Game class.
            insort_left(self.__games, game)
            for tag in game.tags:
                self.add_tag(tag)
            for genre in game.genres:
                self.add_genre(genre)


    def get_games(self) -> List[Game]:
        return self.__games

    def get_game(self, id: int) -> Game:
        for g in self.__games:
            if g.game_id == id: return g
        return None

    def get_number_of_games(self):
        return len(self.__games)
    
    def get_genres(self) -> list[Genre]:
        return self.__genres
    
    def add_genre(self, genre: Genre):
        if (isinstance(genre, Genre) and
            genre not in self.__genres):
            insort_left(self.__genres, genre)

    def get_tags(self) -> list[str]:
        return self.__tags

    def add_tag(self, tag: str):
        if (not isinstance(tag, str) or
            tag == ''):
            return
        elif tag not in self.__tags:
            insort_left(self.__tags, tag)
        
    # def get_random_tags(self, n: int) -> list[str]: # Probably should be dealt with by services?
    #     import random
    #     return random.sample(self.__tags, n)
    
    def get_games_with_tags(self, tags: list[str]) -> List[Game]:
        games = []
        for game in self.__games:
            if all(tag in game.tags for tag in tags):
                games.append(game)
        return games
    
    def search_games(self, title: str = None,
                    price: float = float('inf'),
                    #  release_date: (int, str idk),
                    tags: list[str] = None,
                    genre: [Genre, str] = None,
                    popularity: int = 0) -> list[Game]:
        title = title.lower() if title is not None else None
        genre_name = None
        if isinstance(genre, Genre):
            genre_name = genre.genre_name.lower()
        elif isinstance(genre, str):
            genre_name = genre.lower()
        games = []
        for game in self.__games:
            if ((game.price <= price and game.popularity >= popularity) and
                (tags is None or all(tag in game.tags for tag in tags)) and
                (genre_name is None or genre_name in [g.genre_name.lower() for g in game.genres]) and
                (title is None or title in game.title.lower()) ):
                    
                    games.append(game)
        return games


def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games
    tags = reader.dataset_of_tags
    genres = reader.dataset_of_genres

    # Add games to the repo:
    for game in games:
        repo.add_game(game)
    
    # Add tags to the repo:
    for tag in tags:
        repo.add_tag(tag)
    
    # Add genres to the repo:
    for genre in genres:
        repo.add_genre(genre)
