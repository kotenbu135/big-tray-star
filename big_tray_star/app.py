import threading
import time

import schedule
from PIL import Image
from pystray import Icon, MenuItem, Menu

import json_logger
from my_spotify import get_top_tracks, add_playlist_current_playing, new_album_notification, search_current_playing, \
    playlist_update_notification_main
from my_switch_bot import open_intercom

logger = json_logger.get_logger(__name__)


def run_schedule_add_playlist_current_playing():
    # 一定間隔でタスクを実行する。
    schedule.every(60).seconds.do(add_playlist_current_playing)


def run_schedule_new_album_notification():
    # 一定間隔でタスクを実行する。
    schedule.every(3).hours.do(new_album_notification)


def run_schedule_playlist_update_notification():
    # 一定間隔でタスクを実行する。
    schedule.every(3).hours.do(playlist_update_notification_main)


def run_schedule_get_top_tracks():
    # 一定間隔でタスクを実行する。
    schedule.every(3).hours.do(get_top_tracks)


class TaskTray:
    def __init__(self, image):
        self.status = False

        # アイコンの画像
        image = Image.open(image)
        # 右クリックで表示されるメニュー
        menu = Menu(
            MenuItem('再生中の曲を検索', search_current_playing),
            MenuItem('インターホン解錠', open_intercom),
            MenuItem('Exit', self.stop_program),
        )

        self.icon = Icon(name='nameTray', title='BIG_TRAY_STAR', icon=image, menu=menu)

    def run_schedule(self):
        while self.status:
            schedule.run_pending()
            time.sleep(1)

    def stop_program(self):
        self.status = False

        # 停止
        self.icon.stop()

    def run_program(self):
        self.status = True
        # プレイリスト追加
        task_thread0 = threading.Thread(target=self.run_schedule)
        # プレイリスト追加
        task_thread1 = threading.Thread(target=run_schedule_add_playlist_current_playing)
        # ニューアルバム通知
        task_thread2 = threading.Thread(target=run_schedule_new_album_notification)

        task_thread0.start()
        task_thread1.start()
        task_thread2.start()

        # 実行
        self.icon.run()
