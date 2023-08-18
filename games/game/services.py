from games.adapters.repository import AbstractRepository

def get_game_data(repo: AbstractRepository, game_id):
    game = repo.get_game(game_id)
    # no, i refuse to do that weird game object to dict thing
    return game
