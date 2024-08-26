import rumps
import threading
import subprocess
import webbrowser
import requests
import time

ping_time = None  # 全局变量


class StatusBarApp(rumps.App):
    def __init__(self):
        super(StatusBarApp, self).__init__("SeeVPN", icon=None, quit_button=None)
        self.menu = ["🐱开关Shadowrocket",
                     "----------------------------",
                     "👇使用开关请下载快捷指令👇",
                     "⏬下载快捷指令",
                     "----------------------------",
                     "🌐关于Github",
                     "⏏️退出"]

    @rumps.clicked("🐱开关Shadowrocket")
    def toggle_shadowrocket(self, sender):
        run_shortcut()

    @rumps.clicked("⏬下载快捷指令")
    def download_shortcut(self, _):
        webbrowser.open("https://www.icloud.com/shortcuts/492fc4cdeb1b4c7b8db3c9b9858778fc")

    @rumps.clicked("🌐关于Github")
    def particulars_text(self, _):
        webbrowser.open("https://github.com/KKingwang/SeeVPN")

    @rumps.clicked('⏏️退出')
    def clean_up_before_quit(self, _):
        rumps.quit_application()


def check_vpn_status():
    # 使用scutil命令来检查特定VPN服务的状态
    command = f"scutil --nc status 'Shadowrocket'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        output = result.stdout.strip().split('\n')[0]
        if "Connected" in output:
            return "ON"
        else:
            return "Off"
    else:
        return "None"


def ping_url(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        if response.status_code == 200:
            return end_time - start_time  # 转换为毫秒
        else:
            return None
    except Exception as e:
        return None


def update_ping_time():
    global ping_time
    url = "https://www.google.com.hk"
    while True:
        ping_time = ping_url(url)
        time.sleep(10)  # 每10s更新一次


def update_title(app):
    while True:
        # 这里可以添加更新标题的逻辑
        if ping_time is not None:
            app.title = f"{check_vpn_status()}|{ping_time:.1f}s"
        else:
            app.title = f"{check_vpn_status()}|无链接"

        time.sleep(3)


def run_shortcut():
    try:
        result = subprocess.run(
            ['osascript', '-e', f'tell application "Shortcuts Events" to run the shortcut named "开关Shadowrocket"'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    app = StatusBarApp()
    threading.Thread(target=update_ping_time, daemon=True).start()
    threading.Thread(target=update_title, args=(app,), daemon=True).start()
    app.run()
