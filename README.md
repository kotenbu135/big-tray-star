# big-tray-star

windowsのタスクトレイに常駐するアプリケーションです。  
一定間隔毎にタスクを実行します。

## 動作検証済み環境

* Python: 3.10.7

## 機能
### 自動実行
1. spotifyでフォロー中しているアーティストの新曲を通知する
1. spotifyで現在再生している曲をプレイリストに登録する（履歴用）
1. 他人が作成したプレイリストが更新されたら通知する

### 手動実行
1. spotifyで再生回数上位の曲をプレイリストに登録する
1. 再生中の曲をブラウザでGoogle検索する
1. インターホンを解錠する

## 利用方法

1. <a href="https://spotipy.readthedocs.io/en/master/">Windows環境にAWS認証情報を設定する</a>
1. 後述のAWS Systems Manager パラメータストアを設定する
1. `python init-switch-bot`を実行しコンソールログからインターホン解錠用BotのデバイスIDを取得する
1. `python init-dynamodb`を実行しAWS上にdynamodbテーブルを作成する
1. `pip install -r requirements.txt` を実行
1. `big-tray-star.bat` を実行

## AWS Systems Manager パラメータストア

| 用途                           | 名前                                    |
|------------------------------|---------------------------------------|
| discord webhook url          | /discord/webhook/spotify_new_release  |
| spotify client_id            | /spotify/client_id                    |
| spotify client_secret        | /spotify/client_secret                |
| spotify redirect_uri         | /spotify/redirect_uri                 |
| spotify プレイリストID（履歴）         | /spotify/playlist_id/history          |
| spotify プレイリストID（再生回数上位（短期）） | /spotify/playlist_id/short_term_rank  |
| spotify プレイリストID（再生回数上位（中期）） | /spotify/playlist_id/medium_term_rank |
| spotify プレイリストID（再生回数上位（長期）） | /spotify/playlist_id/long_term_rank   |
| switch bot トークン              | /switch_bot/token                     |
| インターホン解錠用BotのデバイスID          | /switch_bot/device_id/bot_1           |
