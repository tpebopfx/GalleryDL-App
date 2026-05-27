[app]

# (str) Title of your application
title = GalleryDL

# (str) Package name
package.name = gallerydlapp

# (str) Package domain (needed for android packaging)
package.domain = org.tpebopfx

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,html,css,js,sqlite3

# (str) Application version
version = 1.2

# (list) Application requirements
# Здесь мы добавили kivy и android для работы окон и разрешений
requirements = python3, kivy, flask, gallery-dl, android

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# Раскомментировали и добавили права на чтение/запись
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (list) The Android architectures to build for
android.archs = arm64-v8a

# (bool) Use --private data directory for prevents app to be readable by other apps
android.private_storage = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# --- ВОТ ЭТИ СТРОКИ КРИТИЧЕСКИ ВАЖНЫ ДЛЯ GITHUB ACTIONS ---
# Они говорят системе использовать стандартные пути окружения
default_config_version = 1
