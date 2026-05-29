[app]
title = GalleryDL
package.name = gallerydlapp
package.domain = org.tpebopfx
source.dir = .

# Добавили json в список, чтобы файл доехал до телефона
source.include_exts = py,png,jpg,html,css,js,sqlite3,json

version = 1.2
icon.filename = %(source.dir)s/icon.png

# Сохраняем Webview для интерфейса
p4a.bootstrap = webview
p4a.port = 5000

requirements = python3, flask, gallery-dl, android

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# КРИТИЧЕСКИ ВАЖНО: Разрешаем запись в память для Android 10+
android.manifest.application_attributes = android:requestLegacyExternalStorage="true"

android.api = 29
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
default_config_version = 1
