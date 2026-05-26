[app]
# Название твоего приложения (будет под иконкой на телефоне)
title = Gallery App
package.name = galleryapp
package.domain = com.tpebopfx

# АВТОМАТИЧЕСКОЕ ПРИНЯТИЕ ЛИЦЕНЗИИ GOOGLE (Решение ошибки)
android.accept_sdk_license = True

# ИКОНКА ПРИЛОЖЕНИЯ
icon.filename = icon.png

# Указываем, откуда брать файлы
source.dir = .
source.include_exts = py,png,jpg,html,css,js,sqlite3
source.include_patterns = templates/*, static/css/*, static/js/*

version = 1.1

# Самое главное: библиотеки, которые зашьются внутрь APK
requirements = python3, flask, gallery-dl

# Настройки экрана (вертикальная ориентация)
orientation = portrait
fullscreen = 0

# Разрешения для Android (Интернет и доступ к памяти)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Специальный режим для запуска веб-приложений (создает невидимый браузер внутри приложения)
p4a.bootstrap = webview
p4a.port = 5000

