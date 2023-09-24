import pytest
from games.authentication import services as auth_services
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist

# Fixture to create a sample user for testing
@pytest.fixture
def sample_user():
    return User("testuser", "Test123Password")

# Test user registration
def test_register_user(sample_user):
    user = sample_user
    result = auth_services.register_user(user)
    assert result == "Registration successful"

# Test user registration with an existing username
def test_register_existing_user(sample_user):
    user = sample_user
    # Register the user once
    auth_services.register_user(user)
    # Attempt to register the same user again
    result = auth_services.register_user(user)
    assert result == "Username already exists"

# Test user login with valid credentials
def test_login_valid_user(sample_user):
    user = sample_user
    # Register the user
    auth_services.register_user(user)
    # Attempt to log in with the correct username and password
    result = auth_services.login_user(user.username, user.password)
    assert result == "Login successful"

# Test user login with invalid credentials
def test_login_invalid_user(sample_user):
    user = sample_user
    # Attempt to log in with incorrect password
    result = auth_services.login_user(user.username, "IncorrectPassword")
    assert result == "Invalid username or password"

# Test user logout
def test_logout_user(sample_user):
    user = sample_user
    # Register and log in the user
    auth_services.register_user(user)
    auth_services.login_user(user.username, user.password)
    # Attempt to log out the user
    result = auth_services.logout_user(user.username)
    assert result == "Logout successful"
