[app]

# --- ОСНОВНЫЕ НАСТРОЙКИ ПРИЛОЖЕНИЯ ---
title = GalleryDL
package.name = gallerydlapp
package.domain = org.tpebopfx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,sqlite3
version = 1.2

# --- ИКОНКА ПРИЛОЖЕНИЯ ---
# Если твоя иконка называется по-другому (например, logo.png), замени имя файла ниже:
icon.filename = %(source.dir)s/icon.png

# --- ЗАВИСИМОСТИ ---
requirements = python3, kivy, flask, gallery-dl, android

# --- НАСТРОЙКИ ЭКРАНА ---
orientation = portrait
fullscreen = 0

# --- НАСТРОЙКИ ANDROID ---
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.private_storage = True
android.accept_sdk_license = True

# --- НАСТРОЙКИ ДЛЯ ДРУГИХ ПЛАТФОРМ ---
osx.python_version = 3
osx.kivy_version = 1.9.1


[buildozer]
log_level = 2
warn_on_root = 1
default_config_version = 1
