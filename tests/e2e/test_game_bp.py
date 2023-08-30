import pytest

def test_game_page(client):
    response = client.get('/game/457140')
    assert response.status_code == 200
    assert b'Oxygen Not Included' in response.data
    assert b'124.99' in response.data

    response = client.get('/game/40800')
    assert response.status_code == 200
    assert b'Super Meat Boy' in response.data
    assert b'114.99' in response.data
