import bisect
from flask import request

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre

GAMES_PER_PAGE = 15

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

# def get_games(repo: AbstractRepository):
#     games = repo.get_games()
#     game_dicts = []
#     for game in games:
#         game_dict = {
#             'game_id': game.game_id,
#             'title': game.title,
#             'game_url': game.release_date # wtf is this, I didn't write this did I?
#         }
#         game_dicts.append(game_dict)
#     return game_dicts

# def get_games_with_tags(repo: AbstractRepository, tags: list[str]):
#     return repo.get_games_with_tags(tags)

def sort_games(games: list[Game], sort: str):
    if sort == 'title':
        games.sort(key=lambda x: x.title)
    elif sort == 'popular':
        games.sort(key=lambda x: x.recommendations, reverse=True)
    elif sort == 'price':
        games.sort(key=lambda x: x.price)
    elif sort == 'recent':
        games.sort(key=lambda x: x.release_date) # kinda broken since we're using strings
    return games

def parse_subpath(subpath, repo: AbstractRepository):
    subpath = subpath.strip().split('/')
    sort = ''
    tag_str = ''
    tags_in_path = []

    if subpath[0] in ['title', 'popular', 'price', 'recent']:
        sort = subpath[0]
        tags_in_path = subpath[1:]
    else:
        tags_in_path = subpath

    all_tags = repo.get_tags()
    # tags = list(filter(lambda x: x in all_tags, tags)).sort()
    redirect = False
    tags = []
    for tag in tags_in_path:
        if tag in all_tags:
            bisect.insort_left(tags, tag)
        else:
            redirect = True
        
    tag_str = '/'.join(tags)
    
    if tags == []:
        path_str = sort
    elif sort == '':
        path_str = tag_str
    else:
        path_str = sort + '/' + tag_str
    return path_str, tag_str, sort, tags, redirect

def search_games(repo: AbstractRepository, page: int = 1, sort: str = None, *args, **kwargs):
    games = repo.search_games(*args, **kwargs)
    num_games = len(games)
    if sort:
        games = sort_games(games, sort)
    games = games[(page-1)*GAMES_PER_PAGE:page*GAMES_PER_PAGE]
    return games, num_games

def get_random_tags(repo: AbstractRepository, n: int = 5) -> list[str]:
    from random import sample
    return sample(repo.get_tags(), n)

def get_all_genres(repo: AbstractRepository) -> list[Genre]:
    return [g.genre_name for g in repo.get_genres()]

def get_random_genres(repo: AbstractRepository, n: int) -> list[Genre]:
    from random import sample
    return [g.genre_name for g in sample(repo.get_genres(), n)]

def get_genre_from_request(req: request):
    genre = req.args.get('genre', None, type=str)
    if isinstance(genre, str):
        genre = genre.lower().strip()
    if genre == '' or genre == 'null-selection':
        genre = None
    return genre

# TODO: make similar helper functions for other args.