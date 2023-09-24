def get_user_data(username):
    return {
        'username': username,
        'wishlist': [
            {'title': 'Game Title 1', 'added_by': username},
            {'title': 'Game Title 2', 'added_by': username},
            {'title': 'Game Title 3', 'added_by': username}
        ],
        'game_reviews': [
            {'title': 'Game Review 1', 'reviewer': username, 'score': 8.5, 'date': '2023-09-01'},
            {'title': 'Game Review 2', 'reviewer': username, 'score': 9.0, 'date': '2023-09-05'},
            {'title': 'Game Review 3', 'reviewer': username, 'score': 7.8, 'date': '2023-09-10'}
        ]
    }
