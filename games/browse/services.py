from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game


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

def parse_subpath(subpath, repo: AbstractRepository):
    subpath = subpath.strip().split('/')
    sort = ''
    tag_str = ''
    tags = []
    if subpath[0] in ['title', 'popular', 'price', 'recent']:
        sort = subpath[0]
        tags = subpath[1:]
    else:
        tags = subpath
    all_tags = repo.get_tags()
    tags = list(filter(lambda x: x in all_tags, tags))
    tag_str = '/'.join(tags)
    if tags == []:
        path_str = sort
    elif sort == '':
        path_str = tag_str
    else:
        path_str = sort + '/' + tag_str
    return path_str, tag_str, sort, tags
