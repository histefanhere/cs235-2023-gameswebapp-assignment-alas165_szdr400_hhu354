import pytest

from games.adapters import memory_repository as memory_repo

@pytest.fixture
def repo():
    repo = memory_repo.MemoryRepository()
    memory_repo.populate(repo)
    return repo
