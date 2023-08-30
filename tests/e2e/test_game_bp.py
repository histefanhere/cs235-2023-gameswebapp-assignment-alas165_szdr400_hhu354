import pytest

def test_game_page(client):
    # Test that the game page returns the correct games
    response = client.get('/game/457140')
    assert response.status_code == 200
    assert b'Oxygen Not Included' in response.data
    assert b'124.99' in response.data

    response = client.get('/game/40800')
    assert response.status_code == 200
    assert b'Super Meat Boy' in response.data
    assert b'114.99' in response.data

def test_invaild_game_page(client):
    # The web app should show a 404 page when the game doesn't exist/isn't found
    response = client.get('/game/1')
    assert response.status_code == 404

    response = client.get('/game/-1')
    assert response.status_code == 404
