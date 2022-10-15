import threading
import time

import schedule
from PIL import Image
from pystray import Icon, MenuItem, Menu

from big_tray_star import json_logger
from big_tray_star.my_spotify import get_top_tracks, add_playlist_current_playing

logger = json_logger.get_logger(__name__)


def do_task():
    print('do_task')


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

        self.icon = Icon(name='nameTray', title='titleTray', icon=image, menu=menu)

    def run_schedule(self):
        # 一定間隔でタスクを実行する。
        schedule.every(60).seconds.do(add_playlist_current_playing)
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
        # スケジュールの実行
        task_thread = threading.Thread(target=self.run_schedule)
        task_thread.start()

        # 実行
        self.icon.run()


if __name__ == '__main__':
    system_tray = TaskTray(image="app.jpg")
    system_tray.run_program()
