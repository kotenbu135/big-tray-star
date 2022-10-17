import datetime
import threading
import tkinter as tk

from app import TaskTray


# ===========================
# タイマーイベント関数
# ===========================
def time_update():
    now = datetime.datetime.now()
    tm = "{:02}:{:02}:{:02}".format(now.hour, now.minute, now.second)

    canvas.delete("all")
    canvas.create_text(100, 50, text=tm, font=("", 36))

    root.after(1000, time_update)


# ===========================
# スレッド関係の関数
# ===========================
def thread_st():
    system_tray = TaskTray(image="app.jpg")
    system_tray.run_program()


def thread_quit():
    global icon
    global root

    icon.stop()
    root.destroy()  # 追加 add


# ===========================
# メイン 関数
# ===========================
def main():
    global root
    global canvas

    # フォーム表示
    root = tk.Tk()
    root.title("時計")
    root.geometry("200x100")
    root.resizable(False, False)

    canvas = tk.Canvas(master=root, width=200, height=100)
    canvas.place(x=0, y=0)

    # タイマー
    root.after(1000, time_update)

    # Xボタンを押された時の処理
    root.protocol('WM_DELETE_WINDOW', lambda: root.withdraw())

    # スレッド開始
    threading.Thread(target=thread_st).start()

    # イベント待機
    root.mainloop()
