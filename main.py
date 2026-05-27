import threading
import app
from kivy.app import App
from kivy.clock import Clock

# Функция для запуска Flask в отдельном фоновом потоке
def start_flask():
    app.app.run(host='127.0.0.1', port=5000)

class GalleryDLApp(App):
    def build(self):
        # Как только приложение построилось, запрашиваем разрешения
        Clock.schedule_once(self.request_android_permissions, 0)
        
        # Запускаем Flask-сервер в фоне, чтобы он не "вешал" Android
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Kivy-окно оставляем пустым, так как у нас веб-интерфейс
        return None 

    def request_android_permissions(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            
            def permission_callback(permissions, results):
                print("Разрешения получены:", results)
                
            request_permissions([
                Permission.INTERNET, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.READ_EXTERNAL_STORAGE
            ], permission_callback)
        except ImportError:
            print("Запуск не на Android, пропускаем запрос.")

if __name__ == '__main__':
    GalleryDLApp().run()
    
