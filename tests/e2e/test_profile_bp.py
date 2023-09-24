

def test_profile_page(client, auth):
    auth.login()

    # Test that the profile page loads
    response = client.get('/profile')
    assert response.status_code == 200
    assert b'Welcome ' + auth.username.encode('utf-8') + b'!' in response.data
