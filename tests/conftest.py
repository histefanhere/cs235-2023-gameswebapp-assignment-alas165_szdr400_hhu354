from pathlib import Path
import pytest

from games import create_app
from games.adapters import memory_repository as memory_repo

TEST_DATA_PATH = Path('games') / '..' / 'tests' / 'data'


@pytest.fixture
def repo():
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
