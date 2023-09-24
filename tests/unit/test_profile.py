import pytest
from your_app import create_app
from your_app.games.domainmodel.model import User
from your_app.games.adapters.memory_repository import MemoryRepository
from your_app.profile import services as profile_services

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def repo():
    return MemoryRepository()

@pytest.fixture
def logged_in_user(client, repo):
    # Create and log in a test user for the profile page tests
    user = User('testuser', 'password')
    repo.add_user(user)
    with client.session_transaction() as session:
        session['username'] = 'testuser'
    return user

def test_profile_page_access(client, logged_in_user):
    # Test accessing the profile page when logged in
    response = client.get('/profile')
    assert response.status_code == 200  # Check if the page loads successfully

def test_profile_page_access_when_not_logged_in(client):
    # Test accessing the profile page when not logged in
    response = client.get('/profile')
    assert response.status_code == 302  # Check if the page redirects (to login)

def test_profile_page_content(client, logged_in_user):
    # Test if the profile page displays the username
    response = client.get('/profile')
    assert b'Welcome testuser' in response.data  # Check if 'Welcome testuser' is in the page content
