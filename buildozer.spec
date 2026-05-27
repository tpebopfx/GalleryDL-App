[app]
title = GalleryDL
package.name = gallerydlapp
package.domain = org.tpebopfx
source.dir = .
source.include_exts = py,png,jpg,html,css,js,sqlite3
version = 1.1
icon.filename = %(source.dir)s/icon.png

# --- ВОТ ЭТО ВЕРНЕТ ТВОЙ ИНТЕРФЕЙС ---
p4a.bootstrap = webview
p4a.port = 5000

# Kivy нам больше не нужен, минус лишний вес
requirements = python3, flask, gallery-dl, android

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# --- КРИТИЧНО ДЛЯ ПРАВ ДОСТУПА ---
# Откатываем API до 29, чтобы обойти жесткие блокировки Android 11+
android.api = 29
android.minapi = 24

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
default_config_version = 1
