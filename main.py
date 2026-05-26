import app

# Запрашиваем разрешения для Android ПЕРЕД запуском сервера
try:
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.INTERNET, 
        Permission.WRITE_EXTERNAL_STORAGE, 
        Permission.READ_EXTERNAL_STORAGE
    ])
except ImportError:
    print("Запуск не на Android, пропускаем запрос разрешений.")

if __name__ == '__main__':
    # Запускаем наш Flask-сервер
    app.app.run(host='127.0.0.1', port=5000)
    
