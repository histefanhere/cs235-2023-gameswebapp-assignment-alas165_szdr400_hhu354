import pytest

from games.game import services as game_services


def test_game_service_getting_invalid_game_data(repo):
    # Games with these IDs do not exist, so the service should return None.
    game_data = game_services.get_game_data(repo, 1)
    assert game_data is None

    game_data = game_services.get_game_data(repo, -1)
    assert game_data is None


def test_game_service_getting_vaild_game_data(repo):
    # These games exist, and the games service should be able to get their data.
    game_data = game_services.get_game_data(repo, 457140)
    assert game_data.title == "Oxygen Not Included"
    assert game_data.developer == "Klei Entertainment"

    game_data = game_services.get_game_data(repo, 40800)
    assert game_data.title == "Super Meat Boy"
    assert game_data.developer == "Team Meat"
