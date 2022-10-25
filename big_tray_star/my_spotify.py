import time
import urllib.parse
import webbrowser

import spotipy
from spotipy import SpotifyOAuth

import json_logger
from const import scope
from discord_webhook import post_discord
from my_dynamodb import get_item, put_item
from ssm import get_parameters

logger = json_logger.get_logger(__name__)

# 機密情報取得
client_id = get_parameters(param_key="/spotify/client_id")
client_secret = get_parameters(param_key="/spotify/client_secret")
redirect_uri = get_parameters(param_key="/spotify/redirect_uri")
history_playlist_id = get_parameters(param_key="/spotify/playlist_id/history")
short_term_rank_playlist_id = get_parameters(param_key="/spotify/playlist_id/short_term_rank")
medium_term_rank_playlist_id = get_parameters(param_key="/spotify/playlist_id/medium_term_rank")
long_term_rank_playlist_id = get_parameters(param_key="/spotify/playlist_id/long_term_rank")

# クライアント作成
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope),
    language='ja')


def get_all_playlist_items(playlist_id):
    offset = 0
    next_flg = 'True'
    try:
        # 現在のプレイリストの曲ID一覧を取得する
        latest_playlist_tracks = []
        while next_flg is not None:
            playlist_tracks = sp.playlist_items(playlist_id, limit=100, offset=offset)

            for track in playlist_tracks['items']:
                latest_playlist_tracks.append(track['track']['id'])

            playlist_next = playlist_tracks['next']
            if playlist_next is None:
                break

            queries = urllib.parse.urlparse(playlist_next).query
            query_dict = urllib.parse.parse_qs(queries)
            offset = query_dict['offset'][0]
            time.sleep(10)
        return latest_playlist_tracks
    except Exception as e:
        logger.error(e)


def get_all_playlists():
    offset = 0
    next_flg = 'True'
    try:
        # 現在のプレイリストの曲ID一覧を取得する
        latest_playlists = []
        while next_flg is not None:
            playlists = sp.current_user_playlists(limit=50, offset=offset)
            for playlist in playlists['items']:
                latest_playlists.append(playlist)

            playlist_next = playlists['next']
            if playlist_next is None:
                break

            queries = urllib.parse.urlparse(playlist_next).query
            query_dict = urllib.parse.parse_qs(queries)
            offset = query_dict['offset'][0]
            time.sleep(10)
        return latest_playlists
    except Exception as e:
        logger.error(e)


def add_playlist_current_playing():
    try:
        # 現在のプレイリストの曲ID一覧を取得する
        latest_playlist_tracks = get_all_playlist_items(history_playlist_id)

        # 現在再生中の曲を取得する
        current_playing = sp.current_user_playing_track()
        if current_playing is None:
            return

        track_name = current_playing['item']['name']
        track_id = current_playing["item"]["id"]
        artist_name = current_playing['item']['artists'][0]['name']

        # 既にプレイリストに入っていたら何もしない
        if track_id in latest_playlist_tracks:
            return

        # プレイリストに追加
        sp.playlist_add_items(history_playlist_id, [track_id], position=0)
        logger.info('now playing', extra={'track_name': track_name, 'artist_name': artist_name})

    except Exception as e:
        logger.error(e)


def get_top_tracks():
    time_ranges = [{'term': 'short_term', 'playlist_id': short_term_rank_playlist_id},
                   {'term': 'medium_term', 'playlist_id': medium_term_rank_playlist_id},
                   {'term': 'long_term', 'playlist_id': long_term_rank_playlist_id}]

    for time_range in time_ranges:
        top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_range['term'])

        urls = []
        for track in top_tracks['items']:
            urls.append(track['id'])

        playlist_id = time_range['playlist_id']
        clear_playlist(playlist_id)
        sp.playlist_add_items(playlist_id, urls)

        post_discord(f'https://open.spotify.com/playlist/{playlist_id}')
        # レート対策
        time.sleep(10)


def clear_playlist(playlist_id):
    items = sp.playlist_items(playlist_id)
    remove_list = []
    for track in items['items']:
        remove_list.append(track['track']['id'])
    sp.playlist_remove_all_occurrences_of_items(playlist_id, remove_list)


def new_album_notification():
    after = new_album_notification_main()
    while after is not None:
        after = new_album_notification_main()


def new_album_notification_main():
    # フォローアーティスト取得
    response = sp.current_user_followed_artists(limit=50, after=None)
    for artist in response['artists']['items']:
        artist_new_album_notification(artist)
        # レート対策
        time.sleep(10)
    after = exists(response, ['artists', 'cursors', 'after'])
    return after


def artist_new_album_notification(artist):
    # 最新アルバム取得
    latest_album = get_latest_album(artist)

    # dynamodb上の最新アルバムを取得
    table_name = 'spotify_followed_artist_latest_album'
    db_item = get_item(table_name, {'artist_id': latest_album['artist_id']})

    if 'Item' not in db_item:
        put_item(table_name, latest_album)
        logger.info('新規追加')
        return

    if latest_album['album_id'] == db_item['Item']['album_id']:
        logger.info('変更なし')
        return

    put_item(table_name, latest_album)
    post_discord(latest_album['url'])
    logger.info('更新')


def get_latest_album(artist):
    artist_id = artist['id']
    artist_name = artist['name']
    # アルバム情報取得
    albums = sp.artist_albums(artist['uri'], limit=1)
    album = albums['items'][0]
    album_id = album['id']
    album_name = album['name']
    album_url = album['external_urls']['spotify']
    latest_item = {'artist_id': artist_id, 'artist_name': artist_name,
                   'album_id': album_id, 'album_name': album_name,
                   'album_url': album_url
                   }
    return latest_item


def exists(obj, chain):
    _key = chain.pop(0)
    if _key in obj:
        # after str or None
        return exists(obj[_key], chain) if chain else obj[_key]


def search_current_playing():
    # 現在再生中の曲を取得する
    current_playing = sp.current_user_playing_track()
    if current_playing is None:
        return

    # 検索文字列作成
    track_name = current_playing['item']['name']
    artist = current_playing['item']['artists'][0]['name']
    search_params = ' '.join([track_name, artist])

    # URL作成
    url = "https://www.google.com/search"
    params = urllib.parse.urlencode({"query": search_params})
    search_url = f'{url}?{params}'

    # ブラウザで検索する
    webbrowser.open(search_url)


def playlist_update_notification(playlist):
    playlist_id = playlist['id']
    playlist_name = playlist['name']

    # dynamodb上の最新アルバムを取得
    table_name = 'spotify_playlist_latest_album'
    db_item = get_item(table_name, {'playlist_id': playlist_id})
    latest_album = get_all_playlist_items(playlist_id)[0]
    latest_album_obj = {'playlist_id': playlist_id, 'playlist_name': playlist_name, 'latest_album': latest_album}

    if 'Item' not in db_item:
        put_item(table_name, latest_album_obj)
        logger.info('新規追加')
        return

    if latest_album == db_item['Item']['latest_album']:
        logger.info('変更なし')
        return

    put_item(table_name, latest_album_obj)
    playlist_url = playlist['external_urls']['spotify']
    post_discord(f'プレイリストが更新されました。\n{playlist_url}')
    logger.info('更新')


def playlist_update_notification_main():
    # 自分のID取得
    my_profile = sp.current_user()
    my_id = my_profile['id']

    # プレイリスト取得
    playlists = get_all_playlists()

    for playlist in playlists:
        # 自分で作成したプレイリストを除外
        if playlist['owner']['id'] == my_id:
            continue
        playlist_update_notification(playlist)
