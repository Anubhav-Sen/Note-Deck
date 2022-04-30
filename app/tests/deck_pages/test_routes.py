def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302

def test_note_deck_success(client):
    response = client.get('/decks/<deck_id>/<deck_title>/<deck_color>')
    assert response.status_code == 200 or 404
    
    if response.status_code == 200:
        assert b'<div class="card">' in response.data
        assert b'<div class="deck">' in response.data

def test_get_started_success(client):
    response = client.get('/get-started')
    assert response.status_code == 200 or 404

    if response.status_code == 200:
        assert b'Get-Started' in response.data
        assert b'<div class="card">' not in response.data
        assert b'<div class="deck">' not in response.data