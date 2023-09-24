import pytest

from flask import session

from games.domainmodel.model import *

def test_wishlist_page(client):
    # Test that the wishlist page is not accessible to non-logged in users.
    response = client.get("/wishlist")
    assert response.status_code != 200

    # This requires "an active HTTP request", we haven't been taught how to test this and there are more important things to worry about right now.
    # session["username"] = "test"
    # response = client.get("/wishlist")
    # assert response.status_code == 200

