def get_user_data(username):
    return {
        'username': username,
        'wishlist': [
            {'title': 'Game Title 1', 'added_by': 'User1'},
            {'title': 'Game Title 2', 'added_by': 'User2'},
            {'title': 'Game Title 3', 'added_by': 'User3'}
        ],
        'game_reviews': [
            {'title': 'Game Review 1', 'reviewer': 'User1', 'score': 8.5, 'date': '2023-09-01'},
            {'title': 'Game Review 2', 'reviewer': 'User2', 'score': 9.0, 'date': '2023-09-05'},
            {'title': 'Game Review 3', 'reviewer': 'User3', 'score': 7.8, 'date': '2023-09-10'}
        ]
    }
