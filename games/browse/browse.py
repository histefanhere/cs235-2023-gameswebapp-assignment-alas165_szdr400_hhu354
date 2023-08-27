from flask import render_template, Blueprint, redirect, url_for, request
from bisect import insort_left

import games.adapters.repository as repo
from games.browse import services


browse_blueprint = Blueprint(
    'games_bp', __name__
)

@browse_blueprint.route('/browse', methods=['GET', 'POST'])
def browse_games():
    # print(f"url1 {list(request.args.items())}")
    search_string = request.args.get('search') if 'search' in request.args else None
    genre = request.args.get('genre') if 'genre' in request.args else None
    games = services.search_games(repo.repo_instance, title=search_string, genre=genre)
    return _browse_games_render(games=games, cur_search=search_string, cur_genre=genre)

@browse_blueprint.route('/browse/', methods=['GET', 'POST'])
def browse_games_with_slash():
    # print(f"url2 {list(request.args.items())}")
    search_string = request.args.get('search') if 'search' in request.args else None
    genre = request.args.get('genre') if 'genre' in request.args else None
    return redirect(url_for('games_bp.browse_games', search=search_string, genre=genre))

@browse_blueprint.route('/browse/<path:subpath>', methods=['GET', 'POST'])
def browse_games_with_options(subpath: str):
    # print(f"url3 {list(request.args.items())}")
    subpath, tag_path, sort, tags, bad_url = services.parse_subpath(subpath, repo.repo_instance)

    search_string = request.args.get('search') if 'search' in request.args else None
    genre = request.args.get('genre') if 'genre' in request.args else None

    if bad_url: # Redirect to correct url
        return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath, search = search_string, genre=genre))

    games = services.search_games(repo.repo_instance, title=search_string, tags=tags, genre=genre)
    games = services.sort_games(games, sort)

    return _browse_games_render(
            cur_sort = sort,
            cur_tags = tags,
            cur_subpath = subpath,
            cur_tag_path = tag_path,
            cur_search = search_string,
            cur_genre = genre,
            games = games)

def _browse_games_render(
        cur_sort = '',
        cur_tags = [],
        cur_subpath = '',
        cur_tag_path = '',
        cur_search = None,
        cur_genre = None,
        games = []):
    random_tags = services.get_random_tags(repo.repo_instance, 5)
    random_genres = services.get_random_genres(repo.repo_instance, 5)
    return render_template(
        'browse.html',
        # Custom page title
        title = f"Browse Games | CS235 Game Library",
        # Page heading
        heading = "Browse Games",

        # Search Options
        cur_sort = cur_sort,
        cur_tags = cur_tags,
        cur_search = cur_search,
        cur_genre = cur_genre,
        # Page URL
        cur_subpath = cur_subpath,
        cur_tag_path = cur_tag_path,
        
        # Tags
        random_tags = random_tags,
        all_tags = repo.repo_instance.get_tags(),

        # Genres
        random_genres = random_genres,
        all_genres = services.get_all_genres(repo.repo_instance),

        # Search Results
        games = games,
        num_games = len(games),
    )

@browse_blueprint.route('/browse/read_form', methods=['POST'])
def browse_games_read_form():
    
    # Read form data
    form_tags = []
    for key, value in request.form.items():
        if key == 'tag-dropdown' and value != 'null-selection':
            insort_left(form_tags, value)
        else:
            insort_left(form_tags, value)

    subpath = request.args.get('subpath') if 'subpath' in request.args else ''
    for tag in form_tags:
        subpath += '/' + tag

    search_string = request.args.get('search') if 'search' in request.args else None

    return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath, search=search_string))