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

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

    @app.route('/profile')
    def profile():
        # Sample user data (replace with actual user data)
        user_data = {
            'username': 'Hamsu Test',
            'wishlist': [
                {'title': 'Game Title 1', 'added_by': 'User1'},
                {'title': 'Game Title 2', 'added_by': 'User2'},
                {'title': 'Game Title 3', 'added_by': 'User3'}
            ]
        }
        return render_template('profile.html', session=user_data)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.context_processor
    def inject_genres():
        genres = repo.repo_instance.get_genres()
        return dict(all_genres = [g.genre_name for g in genres])

    @app.route('/')
    def home():
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('main.html', heading="Discover new games")

    return app
