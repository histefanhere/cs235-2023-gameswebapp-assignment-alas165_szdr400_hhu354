from flask import render_template, Blueprint

import games.adapters.repository as repo
from games.game import services


game_blueprint = Blueprint(
    'game_bp', __name__
)

@game_blueprint.route('/game/<int:game_id>', methods=['GET'])
def game_view(game_id):
    game_data = services.get_game_data(repo.repo_instance, game_id)
    return render_template(
        'game.html',
        title=f"My Title",
        heading="My Heading",
        game = game_data
    )
