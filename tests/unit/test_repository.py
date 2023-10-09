import sys
sys.path.append("/Users/hamsu/Desktop/Compsci_235/Assignment/cs235-2023-gameswebapp-assignment-alas165_szdr400_hhu354")

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from games.domainmodel.model import User, Review
from games.adapters.database_repository import DatabaseRepository
from games.adapters.orm import map_model_to_tables

# Call the mapping function to establish ORM mappings
map_model_to_tables()

class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        # Create the engine
        DATABASE_URL = 'sqlite:///site.db'  # Use your actual database path
        engine = create_engine(DATABASE_URL, echo=True)

        # Create a session factory
        SessionFactory = sessionmaker(bind=engine)
        
        # This is a setup method. It's run before each test.
        # Here, you can do any setup required for your tests.
        self.repo = DatabaseRepository(SessionFactory)

    def test_add_and_get_user(self):
        # Add a user
        test_user = User("testuser", "TestPassword123")
        self.repo.add_user(test_user)
        
        # Retrieve the user and check if it's correctly stored
        retrieved_user = self.repo.get_user("testuser")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.password, "TestPassword123")

if __name__ == "__main__":
    unittest.main()