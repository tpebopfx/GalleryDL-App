[app]

# --- ОСНОВНЫЕ НАСТРОЙКИ ---
title = GalleryDL
package.name = gallerydlapp
package.domain = org.tpebopfx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,sqlite3
version = 1.2

# --- ИКОНКА (убедись, что файл icon.png лежит в папке) ---
icon.filename = %(source.dir)s/icon.png

# --- ВЕБ-ИНТЕРФЕЙС (ВОТ ЭТО ВЕРНЕТ ТВОЙ САЙТ ВМЕСТО ЧЕРНОГО ЭКРАНА) ---
# Говорим сборщику, что наше приложение — это локальный веб-сайт
p4a.html_app = True

# --- ЗАВИСИМОСТИ ---
# Убрали Kivy, оставили только Flask, движок и системные модули Android
requirements = python3, flask, gallery-dl, android, pyjnius

# --- НАСТРОЙКИ ANDROID ---
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.private_storage = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
default_config_version = 1
