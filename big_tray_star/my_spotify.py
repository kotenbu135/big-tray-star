import spotipy
from spotipy import SpotifyOAuth

from big_tray_star import json_logger
from big_tray_star.const import scope
from big_tray_star.my_dynamodb import get_item, put_item
from big_tray_star.ssm import get_parameters

logger = json_logger.get_logger(__name__)

# 機密情報取得
client_id = get_parameters(param_key="/spotify/client_id")
client_secret = get_parameters(param_key="/spotify/client_secret")
redirect_uri = get_parameters(param_key="/spotify/redirect_uri")
playlist_id = get_parameters(param_key="/spotify/playlist_id")

# クライアント作成
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope))


def add_playlist_current_playing():
    try:
        # 現在のプレイリストの曲ID一覧を取得する
        latest_playlist_tracks = []
        playlist_tracks = sp.playlist_items(playlist_id)
        for track in playlist_tracks['items']:
            latest_playlist_tracks.append(track['track']['id'])

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
        sp.playlist_add_items(playlist_id, [track_id], position=0)
        logger.info('now playing', extra={'track_name': track_name, 'artist_name': artist_name})

    except Exception as e:
        logger.error(e)


def get_top_tracks():
    # ['short_term', 'medium_term', 'long_term']
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')
    for track in top_tracks['items']:
        track['album']['available_markets'] = None
        track['available_markets'] = None
        track_name = track['name']
        artists_name = []
        for artist in track['artists']:
            artists_name.append(artist['name'])
        artist_name = ",".join(artists_name)
        score = track['popularity']

        print(f'track:{track_name} artist:{artist_name} score:{score}')


def new_album_notification():
    # フォローアーティスト取得
    response = sp.current_user_followed_artists(limit=50)
    for artist in response['artists']['items']:
        artist_id = artist['id']
        # アルバム情報取得
        albums = sp.artist_albums(artist['uri'])
        album_id = albums['items'][0]['id']
        new_item = {'artist_id': artist_id, 'album_id': album_id}

        # dynamodb上の最新アルバムを取得
        table_name = 'spotify_followed_artist_latest_album'
        db_item = get_item(table_name, {'artist_id': artist_id})
        if 'Item' in db_item:
            dynamodb_album_id = db_item['Item']['album_id']
            # apiから取得したIDとDB値が異なる場合、通知する
            if album_id != dynamodb_album_id:
                put_item(table_name, new_item)
                print('つうち')
        else:
            put_item(table_name, new_item)
