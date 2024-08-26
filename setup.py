from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['rumps', 'requests'],
    'plist': {
        'CFBundleIdentifier': 'top.kongbaixx.seevpn',  # 替换为你的应用ID
        'LSUIElement': True,  # 这个选项会隐藏Dock栏图标
        'CFBundleIconFile': 'seevpn.icns',  # 图标文件名
        'CFBundleName': 'SeeVPN',  # 应用程序名称
        'CFBundleDisplayName': 'SeeVPN',  # 显示名称（可选）
    },
}

setup(
    app=APP,
    data_files=[('', ['seevpn.icns'])],  # 确保图标文件路径正确
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
