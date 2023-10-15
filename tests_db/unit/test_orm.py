import datetime
import pickle
import pytest
from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import User, Game, Tag, Review


def add_user(sess, account=None):
    new_name = "Bob"
    new_password = "avodaco"
    if account is not None:
        new_name = account[0]
        new_password = account[1]

    sess.execute(
        'INSERT INTO users (username, password) VALUES (:username, :password)',
        {'username': new_name, 'password': new_password}
    )
    return sess.execute(
        'SELECT id from users where username = :username',
        {'username': new_name}
    ).fetchone()[0]


def add_users(sess, accounts):
    for value in accounts:
        sess.execute(
            'INSERT INTO users (username, password) VALUES (:username, :password)',
            {'username': value[0], 'password': value[1]}
        )
    return tuple(row[0] for row in list(sess.execute('SELECT id from users')))


def add_game(sess):
    sess.execute(
        'INSERT INTO games (game_id, game_title, price, release_date, description, image_url, website_url, recommendations, windows, mac, linux, categories, achievements, developer, screenshots, movies) VALUES (:game_id, :game_title, :price, :release_date, :description, :image_url, :website_url, :recommendations, :windows, :mac, :linux, :categories, :achievements, :developer, :screenshots, :movies)',
        {
            'game_id': 1,
            'game_title': "Test Game",
            'price': 9.99,
            'release_date': "Jun 1, 2010",
            'description': "This is a test game",
            'image_url': "https://example.com",
            'website_url': "https://example.com",
            'recommendations': 100,
            'windows': True,
            'mac': True,
            'linux': False,
            'categories': pickle.dumps(['Action']),
            'achievements': 10,
            'developer': "Test Developer",
            'screenshots': pickle.dumps(['https://example.com']),
            'movies': pickle.dumps(['https://example.com'])
        }
    )
    return sess.execute(
        'SELECT game_id from games where game_title = :game_title',
        {'game_title': "Test Game"}
    ).fetchone()[0]


def add_tags(sess):
    sess.execute(
        'INSERT INTO tags (tag_name) VALUES ("Action"), ("Adventure")'
    )
    return tuple(row[0] for row in list(sess.execute('SELECT tag_name from tags')))


def add_game_tag_associations(sess, game_id, tag_names):
    for tag_name in tag_names:
        sess.execute(
            'INSERT INTO game_tags (game_id, tag_name) VALUES (:game_id, :tag_name)',
            {
                'game_id': game_id,
                'tag_name': tag_name
            }
        )


def add_reviewed_game(sess):
    sess.execute(
        'INSERT INTO reviews (user_id, game_id, rating, comment, date) VALUES (:user_id, :game_id, :rating, :comment, :date)',
        {
            'user_id': add_game(sess),
            'game_id': add_user(sess),
            'rating': 5,
            'comment': "This is a test review",
            'date': datetime.date(2020, 10, 10)
        }
    )

    return sess.execute('SELECT game_id from games').fetchone()[0]


def test_loading_of_users(empty_session):
    add_users(empty_session, [
        ("Andrew", "Avocado101"),
        ("Cindy", "Cinderella99")
    ])

    assert empty_session.query(User).all() == [
        User("Andrew", "Avocado101"),
        User("Cindy", "Cinderella99")
    ]


def test_saving_of_users(empty_session):
    user = User("Andrew", "Avocado101")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "Avocado101")]


def test_loading_of_game(empty_session):
    add_game(empty_session)

    rows = empty_session.query(Game).all()
    game = rows[0]
    
    expected_game = Game(1, "Test Game")
    assert game == expected_game

    assert game.game_id == 1
    assert game.title == "Test Game"
    assert game.price == 9.99
    assert game.release_date == "Jun 1, 2010"
    assert game.description == "This is a test game"
    assert game.image_url == "https://example.com"
    assert game.website_url == "https://example.com"
    assert game.recommendations == 100
    assert game.windows == 1
    assert game.mac == 1
    assert game.linux == 0
    assert game.categories == ['Action']
    assert game.achievements == 10
    assert game.developer == "Test Developer"
    assert game.screenshots == ["https://example.com"]
    assert game.movies == ["https://example.com"]


def test_loading_of_tagged_game(empty_session):
    game_id = add_game(empty_session)
    tag_names = add_tags(empty_session)
    add_game_tag_associations(empty_session, game_id, tag_names)

    game = empty_session.query(Game).get(game_id)
    tags = [empty_session.query(Tag).get(key) for key in tag_names]

    for tag in tags:
        assert tag in game.tags    


def test_loading_of_reviewed_game(empty_session):
    add_reviewed_game(empty_session)
    
    game = empty_session.query(Game).all()[0]
    
    for review in game.reviews:
        assert review.game is game


def test_saving_of_review(empty_session):
    game_id = add_game(empty_session)
    user_id = add_user(empty_session)
    
    game = empty_session.query(Game).all()[0]
    user = empty_session.query(User).all()[0]
    
    review = Review(user, game, 5, "This is a test review", datetime.date(2020, 10, 10))
    user.add_review(review)
    game.add_review(review)
    
    empty_session.add(review)
    empty_session.commit()
    
    rows = list(empty_session.execute('SELECT user_id, game_id, rating, comment, date FROM reviews'))
    assert rows == [
        (user_id, game_id, 5, "This is a test review", datetime.date(2020, 10, 10).isoformat())
    ]


def test_saving_of_game(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title, price FROM games'))
    assert rows == [
        (1, "Test Game", 2.99)
    ]


def test_saving_tagged_game(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]
    tag = Tag("Action")
    game.add_tag(tag)
    
    empty_session.add(game)
    empty_session.commit()
    
    # Test already exists for this
    game_id = list(empty_session.execute('SELECT game_id FROM games'))[0][0]
    
    # Check that the tags table has a new record
    tag_name = list(empty_session.execute('SELECT tag_name FROM game_tags'))[0][0]
    assert tag_name == "Action"
    
    # Check that the game_tags table has a new record
    rows = list(empty_session.execute('SELECT game_id, tag_name FROM game_tags'))
    game_foreign_key = rows[0][0]
    tag_foreign_key = rows[0][1]
    
    assert game_id == game_foreign_key
    assert tag_name == tag_foreign_key
    

def test_saving_reviewed_game(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]
    
    user = User("Andrew", "Avocado101")
    
    review = Review(user, game, 5, "This is a test review", datetime.date(2020, 10, 10))
    user.add_review(review)
    game.add_review(review)
    
    empty_session.add(game)
    empty_session.commit()
    
    # Test already exists for this
    game_id = list(empty_session.execute('SELECT game_id FROM games'))[0][0]
    
    # Test already exists for this
    user_id = list(empty_session.execute('SELECT id FROM users'))[0][0]
    
    # Check that the reviews table has a new record
    rows = list(empty_session.execute('SELECT user_id, game_id, rating, comment, date FROM reviews'))
    assert rows == [
        (user_id, game_id, 5, "This is a test review", datetime.date(2020, 10, 10).isoformat())
    ]
