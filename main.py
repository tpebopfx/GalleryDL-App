import os
import threading
import app

def request_android_permissions():
    """Запрос разрешений напрямую через Android Java API без использования Kivy"""
    try:
        from jnius import autoclass
        from android.permissions import request_permissions, Permission
        
        # Запрашиваем стандартные права Android
        request_permissions([
            Permission.INTERNET,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])
    except Exception as e:
        print("Запуск не на Android или ошибка прав:", e)

if __name__ == '__main__':
    # Сначала запрашиваем разрешения через системный Java-интерфейс
    request_android_permissions()
    
    # Запускаем Flask-сервер на локальном хосте
    app.app.run(host='127.0.0.1', port=5000)
    
