import app

if __name__ == '__main__':
    # Запрашиваем разрешения прямо перед стартом сервера, когда приложение уже "проснулось"
    try:
        from android.permissions import request_permissions, Permission
        
        def permission_callback(permissions, results):
            print("Результат выдачи разрешений:", results)
            
        request_permissions([
            Permission.INTERNET, 
            Permission.WRITE_EXTERNAL_STORAGE, 
            Permission.READ_EXTERNAL_STORAGE
        ], permission_callback)
    except ImportError:
        print("Запуск не на Android, пропускаем запрос разрешений.")

    # Запускаем наш Flask-сервер
    app.app.run(host='127.0.0.1', port=5000)
    
