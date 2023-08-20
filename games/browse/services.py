from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game
import bisect


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        game_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'game_url': game.release_date
        }
        game_dicts.append(game_dict)
    return game_dicts

def get_games_with_tags(repo: AbstractRepository, tags: list[str]):
    return repo.get_games_with_tags(tags)

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
