import pytest
from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import User


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
