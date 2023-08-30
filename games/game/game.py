from flask import abort, render_template, Blueprint

import games.adapters.repository as repo
from games.game import services


game_blueprint = Blueprint(
    'game_bp', __name__
)

@game_blueprint.route('/game/<int:game_id>', methods=['GET'])
def game_view(game_id):
    game_data = services.get_game_data(repo.repo_instance, game_id)

    if game_data is None:
        abort(404)

    platform_support = []
    if game_data.windows: platform_support.append('Windows')
    if game_data.mac: platform_support.append('Mac')
    if game_data.linux: platform_support.append('Linux')
    platform_support = ', '.join(platform_support)

    print(game_data.categories)
    if 'Full controller support' in game_data.categories:
        controller_support = 'Full Support'
    elif 'Partial Controller Support' in game_data.categories:
        controller_support = 'Partial Support'
    else:
        controller_support = 'No Support'

    if 'Steam Cloud' in game_data.categories:
        cloud_support = 'Supported'
    else:
        cloud_support = 'Not Supported'
    all_genres = repo.repo_instance.get_genres()

    return render_template(
        'game.html',
        title=f"My Title",
        heading="My Heading",
        game = game_data,
        controller_support = controller_support,
        platform_support = platform_support,
        cloud_support = cloud_support,
        all_genres = [g.genre_name for g in all_genres]
    )
