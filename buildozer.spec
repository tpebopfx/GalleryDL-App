[app]
title = GalleryDL
package.name = gallerydlapp
package.domain = org.tpebopfx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,sqlite3

# Версия приложения
version = 1.2

# Требования (очень важно: добавлены kivy и android)
requirements = python3, kivy, flask, gallery-dl, android

# Разрешения Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Настройки API (33 - современный стандарт)
android.api = 33
android.minapi = 24

# Ориентация экрана
orientation = portrait

# Архитектуры (arm64 - для всех современных телефонов)
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
