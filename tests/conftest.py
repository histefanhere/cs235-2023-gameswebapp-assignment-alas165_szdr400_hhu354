from pathlib import Path
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games import create_app
from games.adapters import memory_repository as memory_repo

from games.adapters import database_repository as db_repo
from games.adapters.orm import metadata, map_model_to_tables


TEST_DATA_PATH = Path('games') / '..' / 'tests' / 'data'

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///games-test.db'
REPOSITORY = 'database'

@pytest.fixture
def repo():
    repo = None
    if REPOSITORY == 'database':
        clear_mappers()
        engine = create_engine(TEST_DATABASE_URI_FILE)
        metadata.create_all(engine)
        for table in reversed(metadata.sorted_tables):
            engine.execute(table.delete())
        map_model_to_tables()
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        repo = db_repo.DatabaseRepository(session_factory)
        db_repo.populate(TEST_DATA_PATH, repo)
    elif REPOSITORY == 'memory':
        repo = memory_repo.MemoryRepository()
        memory_repo.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


# Class for managing authentication in tests
# Just simplifies some of the code needed to log in and out
class AuthenticationManager:
    def __init__(self, client):
        self._client = client
        self.username = None
        self.password = None

    def login(self, username='test', password='test'):
        self.username = username
        self.password = password
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/authentication/logout')


# Gives us access to the auth class in tests
@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
