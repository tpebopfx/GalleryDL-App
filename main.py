import app

def ask_permissions():
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.INTERNET, 
            Permission.WRITE_EXTERNAL_STORAGE, 
            Permission.READ_EXTERNAL_STORAGE
        ])
    except ImportError:
        pass

if __name__ == '__main__':
    # Запрашиваем права
    ask_permissions()
    
    # Запускаем Flask
    app.app.run(host='127.0.0.1', port=5000, debug=False)
    
