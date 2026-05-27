import threading
import app
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

# Функция для запуска Flask в фоновом потоке
def start_flask():
    app.app.run(host='127.0.0.1', port=5000)

class GalleryDLApp(App):
    def build(self):
        # Как только интерфейс построился, запрашиваем разрешения
        Clock.schedule_once(self.request_android_permissions, 0)
        
        # Запускаем Flask-сервер в фоне
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Создаем пустой контейнер, чтобы Android не закрывал приложение из-за отсутствия окон
        layout = BoxLayout()
        return layout

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
    
