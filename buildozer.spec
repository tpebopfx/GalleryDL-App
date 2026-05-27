[app]

# --- ОСНОВНЫЕ НАСТРОЙКИ ПРИЛОЖЕНИЯ ---
title = GalleryDL
package.name = gallerydlapp
package.domain = org.tpebopfx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,sqlite3
version = 1.2

# --- ЗАВИСИМОСТИ ---
# Python 3, интерфейс Kivy, сервер Flask, движок скачивания и модуль для разрешений
requirements = python3, kivy, flask, gallery-dl, android

# --- НАСТРОЙКИ ЭКРАНА ---
orientation = portrait
fullscreen = 0

# --- НАСТРОЙКИ ANDROID ---
# Критически важно: раскомментированы и добавлены нужные права
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Современные версии API (33 - стандарт для Android 13, 24 - минимум для Android 7.0)
android.api = 33
android.minapi = 24

# Архитектуры: добавлены обе основные для максимальной совместимости со смартфонами
android.archs = arm64-v8a, armeabi-v7a

# Разрешаем бэкап приложения в системе Android
android.allow_backup = True

# Изолированное хранилище (True - стандарт безопасности Android)
android.private_storage = True

# --- ПАРАМЕТРЫ ДЛЯ GITHUB ACTIONS (КРИТИЧНО) ---
# Автоматическое принятие лицензий SDK, чтобы сборка не зависала с просьбой нажать "Y"
android.accept_sdk_license = True

# --- НАСТРОЙКИ ДЛЯ ДРУГИХ ПЛАТФОРМ (НЕ УДАЛЯТЬ) ---
# Buildozer может упасть, если этих строк нет, даже если мы собираем под Android
osx.python_version = 3
osx.kivy_version = 1.9.1


[buildozer]

# --- СИСТЕМНЫЕ НАСТРОЙКИ СБОРЩИКА ---
# Уровень логирования (2 = детальный вывод в консоль, помогает при ошибках)
log_level = 2

# Предупреждение при запуске от root (в GitHub Actions всегда 1 или 0)
warn_on_root = 1

# Версия профиля конфигурации (GitHub Actions ищет этот параметр)
default_config_version = 1
