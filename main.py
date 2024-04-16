import ctypes
import multiprocessing
import os
import subprocess
import sys
import threading
import time

import pystray
from PIL import Image

from launcher import launch

icon_path = os.path.dirname(os.path.realpath(__file__)) + "/dwrg.ico"


class TrayApp:
    def __init__(self):
        self.icon = pystray.Icon(name="idv", title="idv助手")
        self.process = None
        image = Image.open(icon_path)
        self.icon.icon = image
        self.icon.menu = pystray.Menu(self.create_menu_items)

    def create_menu_items(self):
        return (
            pystray.MenuItem("启动", self.start_process, enabled=lambda item: self.process is None),
            pystray.MenuItem("停止", self.stop_process, enabled=lambda item: self.process is not None),
            pystray.MenuItem("退出", self.quit)
        )

    def start_process(self, _=None):
        if self.process is None or not self.process.is_alive():
            self.process = multiprocessing.Process(target=launch)
            self.process.start()
            self.icon.update_menu()

        def run_subprocess():
            success_file = os.path.join(os.path.expanduser('~'), '.mitmproxy', 'success')
            if os.path.exists(success_file):
                return

            start_time = time.time()
            cert_file = os.path.join(os.path.expanduser('~'), '.mitmproxy', 'mitmproxy-ca-cert.cer')
            while True:
                if os.path.exists(cert_file):
                    result = subprocess.run(["certutil", "-addstore", "root", cert_file])
                    if result.returncode == 0:
                        open(success_file, 'a').close()
                    break
                elif time.time() - start_time > 30:
                    break
                time.sleep(1)

        threading.Thread(target=run_subprocess).start()

    def stop_process(self, _=None):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.icon.update_menu()

    def quit(self, _=None):
        self.stop_process()
        self.icon.stop()

    def run(self):
        self.start_process()
        self.icon.run()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)

    multiprocessing.freeze_support()

    app = TrayApp()
    app.run()


if __name__ == '__main__':
    main()
