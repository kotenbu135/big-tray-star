import threading
import time

import schedule
from PIL import Image
from pystray import Icon, MenuItem, Menu

from big_tray_star import json_logger
from big_tray_star.my_spotify import get_top_tracks, add_playlist_current_playing, new_album_notification

logger = json_logger.get_logger(__name__)


class TaskTray:
    def __init__(self, image):
        self.status = False

        # アイコンの画像
        image = Image.open(image)
        # 右クリックで表示されるメニュー
        menu = Menu(
            MenuItem('get_top_tracks', get_top_tracks),
            MenuItem('Exit', self.stop_program),
        )

        self.icon = Icon(name='nameTray', title='BIG_TRAY_STAR', icon=image, menu=menu)

    def run_schedule_add_playlist_current_playing(self):
        # 一定間隔でタスクを実行する。
        schedule.every(60).seconds.do(add_playlist_current_playing)
        # status が True である間実行する。
        while self.status:
            schedule.run_pending()
            time.sleep(1)

    def run_schedule_new_album_notification(self):
        # 一定間隔でタスクを実行する。
        schedule.every(60).seconds.do(new_album_notification)
        # status が True である間実行する。
        while self.status:
            schedule.run_pending()
            time.sleep(1)

    def stop_program(self, icon):
        self.status = False

        # 停止
        self.icon.stop()

    def run_program(self):
        self.status = True
        # プレイリスト追加
        task_thread_1 = threading.Thread(target=self.run_schedule_add_playlist_current_playing)
        task_thread_1.start()

        # ニューアルバム通知
        task_thread_2 = threading.Thread(target=self.run_schedule_new_album_notification)
        task_thread_2.start()

        # 実行
        self.icon.run()


if __name__ == '__main__':
    system_tray = TaskTray(image="app.jpg")
    system_tray.run_program()
