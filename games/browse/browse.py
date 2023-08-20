from flask import render_template, Blueprint, redirect, url_for

import games.adapters.repository as repo
from games.browse import services


browse_blueprint = Blueprint(
    'games_bp', __name__
)

@browse_blueprint.route('/browse', methods=['GET'])
def browse_games():
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    return render_template(
        'browse.html',
        # Custom page title
        title=f"Browse Games | CS235 Game Library",
        # Page heading
        heading="Browse Games",
        games=all_games,
        num_games=num_games,
        cur_subpath='',
        cur_tag_path = '',
        cur_sort = '',
        cur_tags = []
    )

@browse_blueprint.route('/browse/<path:subpath>', methods=['GET'])
def browse_games_with_options(subpath: str):
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    
    subpath, tag_path, sort, tags, bad_url = services.parse_subpath(subpath, repo.repo_instance)

    if bad_url: # Redirect to correct url
        return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath))
    
    return render_template(
        'browse.html',
        # Custom page title
        title=f"Browse Games | CS235 Game Library",
        # Page heading
        heading="Browse Games",
        games=all_games,
        num_games=num_games,
        cur_subpath=subpath,
        cur_tag_path = tag_path,
        cur_sort = sort,
        cur_tags = tags,
    )