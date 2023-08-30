"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template
import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    
    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the repository from the provided csv file.
    populate(data_path, repo.repo_instance)

    with app.app_context():
        # Register the browse blueprint to the app instance.
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .game import game
        app.register_blueprint(game.game_blueprint)

    @app.route('/')
    def home():
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        genres = repo.repo_instance.get_genres()
        print(genres)
        return render_template('main.html', all_genres = genres, heading="Discover new games")


    return app
