import datetime
import os
from pathlib import Path
from bisect import insort_left
from typing import List

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Review, User


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__tags = list()
        self.__genres = list()
        self.__users = list()
        self.__reviews = list()

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
    
    # def get_games_with_tags(self, tags: list[str]) -> List[Game]:
    #     games = []
    #     for game in self.__games:
    #         if all(tag in game.tags for tag in tags):
    #             games.append(game)
    #     return games
    
    def search_games(self, title: str = None,
                    price: float = float('inf'),
                    #  release_date: (int, str idk),
                    tags: list[str] = None,
                    genre: [Genre, str] = None,
                    recommendations: int = 0) -> list[Game]:
        title = title.lower() if title is not None else None
        genre_name = None
        if isinstance(genre, Genre):
            genre_name = genre.genre_name.lower()
        elif isinstance(genre, str):
            genre_name = genre.lower()
        games = []
        # print(f"searching for - title: {title}, price: {price}, tags: {tags}, genre: {genre_name}, recommendations: {recommendations}")
        for game in self.__games:
            if ((game.price <= price and game.recommendations >= recommendations) and
                (tags is None or all(tag in game.tags for tag in tags)) and
                (genre_name is None or genre_name in [g.genre_name.lower() for g in game.genres]) and
                (title is None or title in game.title.lower()) ):
                    
                    games.append(game)
        return games
    
    def get_user(self, username: str):
        for user in self.__users:
            if user.username == username:
                return user
        return None
    
    def add_user(self, user):
        if user not in self.__users:
            self.__users.append(user)

    def add_review(self, review: Review):
        if review not in self.__reviews:
            self.__reviews.append(review)


def populate(data_path: Path, repo: AbstractRepository):
    # dir_name = os.path.dirname(os.path.abspath(__file__))
    # games_file_name = os.path.join(dir_name, "data/games.csv")
    games_file_name = str(Path(data_path) / "games.csv")
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

    # TESTING: Add a bunch of random users to the repo
    from games.authentication.services import add_user
    add_user('test', 'test', repo)
    add_user('bob', 'Bob123', repo)
    add_user('alice', 'Alice123', repo)
    add_user('david', 'David123', repo)

    # # TESTING: Add a bunch of random reviews to each game
    import random
    rand_reviews = [
        "This game is okay, with good visuals but bad gameplay. Something to play if you want to show others your powerful PC.",
        "Best game I've ever played! I've spent over 1000 hours on this game and I'm still not bored of it.",
        "This game is terrible. I can't believe I wasted my money on this.",
        "I don't know why this game is so popular. It's just a generic shooter.",
        "This game is great, but it's a little short.",
        "This game is great, but it's a little long.",
        "It's very similar to Minecraft, but it's still a good game.",
        "This game is amazing! I love the story and the characters.",
        "This game is amazing! I love the gameplay and the graphics.",
    ]
    rand_users = [
        repo.get_user('bob'),
        repo.get_user('alice'),
        repo.get_user('david'),
    ]
    for game in repo.get_games():
        for i in range(random.randint(1, 3)):
            rand_date = datetime.date(random.randint(2010, 2023), random.randint(1, 12), random.randint(1, 28))
            rev = Review(rand_users[i], game, random.randint(0, 5), rand_reviews[random.randint(0, len(rand_reviews)-1)], rand_date)
            rand_users[i].add_review(rev)
            game.add_review(rev)

        for user in rand_users:
            if random.random() > 0.9:
                user.add_to_wishlist(game)
