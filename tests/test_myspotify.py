def test_exists_true():
    response_after = '06F1MiFx0dHLHEPQBIrcr9'
    response = {'artists': {'cursors': {'after': response_after},
                            'href': 'https://api.spotify.com/v1/me/following?type=artist&limit=1',
                            'items': [
                                {'external_urls': {'spotify': 'https://open.spotify.com/artist/06F1MiFx0dHLHEPQBIrcr9'},
                                 'followers': {'href': None, 'total': 95738},
                                 'genres': ['anime', 'j-pixie', 'j-poprock'],
                                 'href': 'https://api.spotify.com/v1/artists/06F1MiFx0dHLHEPQBIrcr9',
                                 'id': '06F1MiFx0dHLHEPQBIrcr9',
                                 'images': [{'height': 640,
                                             'url': 'https://i.scdn.co/image/ab67616d0000b273bc192514b9c60de32aab6f0f',
                                             'width': 640},
                                            {'height': 300,
                                             'url': 'https://i.scdn.co/image/ab67616d00001e02bc192514b9c60de32aab6f0f',
                                             'width': 300},
                                            {'height': 64,
                                             'url': 'https://i.scdn.co/image/ab67616d00004851bc192514b9c60de32aab6f0f',
                                             'width': 64}],
                                 'name': 'KOTOKO',
                                 'popularity': 41,
                                 'type': 'artist',
                                 'uri': 'spotify:artist:06F1MiFx0dHLHEPQBIrcr9'}],
                            'limit': 1,
                            'next': 'https://api.spotify.com/v1/me/following?type=artist&after=06F1MiFx0dHLHEPQBIrcr9&limit=1',
                            'total': 33}}
    from big_tray_star.my_spotify import exists
    after = exists(response, ['artists', 'cursors', 'after'])
    assert after == response_after


def test_exists_false():
    response_after = None
    response = {'artists': {'cursors': {'after': response_after},
                            'href': 'https://api.spotify.com/v1/me/following?type=artist&limit=1',
                            'items': [
                                {'external_urls': {'spotify': 'https://open.spotify.com/artist/06F1MiFx0dHLHEPQBIrcr9'},
                                 'followers': {'href': None, 'total': 95738},
                                 'genres': ['anime', 'j-pixie', 'j-poprock'],
                                 'href': 'https://api.spotify.com/v1/artists/06F1MiFx0dHLHEPQBIrcr9',
                                 'id': '06F1MiFx0dHLHEPQBIrcr9',
                                 'images': [{'height': 640,
                                             'url': 'https://i.scdn.co/image/ab67616d0000b273bc192514b9c60de32aab6f0f',
                                             'width': 640},
                                            {'height': 300,
                                             'url': 'https://i.scdn.co/image/ab67616d00001e02bc192514b9c60de32aab6f0f',
                                             'width': 300},
                                            {'height': 64,
                                             'url': 'https://i.scdn.co/image/ab67616d00004851bc192514b9c60de32aab6f0f',
                                             'width': 64}],
                                 'name': 'KOTOKO',
                                 'popularity': 41,
                                 'type': 'artist',
                                 'uri': 'spotify:artist:06F1MiFx0dHLHEPQBIrcr9'}],
                            'limit': 1,
                            'next': 'https://api.spotify.com/v1/me/following?type=artist&after=06F1MiFx0dHLHEPQBIrcr9&limit=1',
                            'total': 33}}
    from big_tray_star.my_spotify import exists
    after = exists(response, ['artists', 'cursors', 'after'])
    assert after == response_after
