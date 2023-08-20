from flask import render_template, Blueprint, redirect, url_for, request
from bisect import insort_left

import games.adapters.repository as repo
from games.browse import services


browse_blueprint = Blueprint(
    'games_bp', __name__
)

@browse_blueprint.route('/browse', methods=['GET'])
def browse_games():
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    return _browse_games_render(num_games=num_games, games=all_games)

@browse_blueprint.route('/browse/<path:subpath>', methods=['GET'])
def browse_games_with_options(subpath: str):
    subpath, tag_path, sort, tags, bad_url = services.parse_subpath(subpath, repo.repo_instance)

    if bad_url: # Redirect to correct url
        return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath))
    
    games = services.get_games_with_tags(repo.repo_instance, tags)
    num_games = len(games)

    return _browse_games_render(
            cur_sort = sort,
            cur_tags = tags,
            cur_subpath = subpath,
            cur_tag_path = tag_path,
            num_games = num_games,
            games = games)

def _browse_games_render(
        cur_sort = 'title',
        cur_tags = [],
        cur_subpath = '',
        cur_tag_path = '',
        num_games = 0,
        games = []):
    random_tags = repo.repo_instance.get_random_tags(5)
    return render_template(
        'browse.html',
        # Custom page title
        title = f"Browse Games | CS235 Game Library",
        # Page heading
        heading = "Browse Games",

        # Search Options
        cur_sort = cur_sort,
        cur_tags = cur_tags,
        # Page URL
        cur_subpath = cur_subpath,
        cur_tag_path = cur_tag_path,
        
        # Tags
        random_tags = random_tags,
        all_tags = repo.repo_instance.get_tags(),

        # Search Results
        games = games,
        num_games = num_games,
    )

@browse_blueprint.route('/browse/read_form', methods=['POST'])
def browse_games_read_form():
    # Read form data
    form_tags = []
    for key, value in request.form.items():
        print(f"key: {key}, value: {value}")
        if key == 'tag-dropdown' and value != 'null-selection':
            insort_left(form_tags, value)
        else:
            insort_left(form_tags, value)

    subpath = request.args.get('subpath')
    for tag in form_tags:
        subpath += '/' + tag

    return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath))