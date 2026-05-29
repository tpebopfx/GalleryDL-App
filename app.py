import os
import sys
import atexit
import sqlite3
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response

import gallery_dl.config as gdl_config
import gallery_dl.job as gdl_job

app = Flask(__name__)

# --- БАЗА ДАННЫХ И ПУТИ ---
BASE_DIR = "/sdcard/Download/GalleryDL_App"
DB_NAME = os.path.join(BASE_DIR, "history.db")
stop_requested = False

def get_db_connection():
    """Безопасное подключение к БД. Создает папку и файл, только если они нужны."""
    if not os.path.exists(BASE_DIR):
        try:
            os.makedirs(BASE_DIR)
        except Exception as e:
            print(f"Ошибка создания папки: {e}")
            
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT,
            tags TEXT,
            files_added INTEGER,
            size_bytes INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    return conn

# --- СПИСОК ПРИОРИТЕТНЫХ САЙТОВ ---
PRIORITY_SITES = {
    "Danbooru": {"url": "https://danbooru.donmai.us/posts?tags={}", "placeholder": "Например: hatsune_miku", "info": "Пробелы заменяйте на _"},
    "Pixiv": {"url": "https://www.pixiv.net/en/users/{}", "placeholder": "Например: 112233", "info": "Числовой ID автора"},
    "Twitter": {"url": "https://twitter.com/{}", "placeholder": "Например: elonmusk", "info": "Юзернейм из ссылки профиля"},
    "Reddit": {"url": "https://www.reddit.com/r/{}/", "placeholder": "Например: wallpapers", "info": "Название без r/"},
    "Gelbooru": {"url": "https://gelbooru.com/index.php?page=post&s=list&tags={}", "placeholder": "Например: genshin_impact", "info": "Теги через подчеркивание"},
    "DeviantArt": {"url": "https://www.deviantart.com/{}/gallery", "placeholder": "Например: wlop", "info": "Точный никнейм"},
    "Instagram": {"url": "https://www.instagram.com/{}/", "placeholder": "Например: zuck", "info": "Юзернейм без @"},
    "Другой сайт": {"url": "{}", "placeholder": "https://site.com/gallery", "info": "Полный URL-адрес"}
}

# --- ФУНКЦИИ ЛОГИКИ ---
def get_dir_stats(path):
    if not os.path.exists(path): return 0, 0
    total_size = 0
    total_files = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                total_files += 1
    return total_files, total_size

def format_size(size_bytes):
    if size_bytes == 0: return "0 KB"
    if size_bytes < 1024 * 1024: return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"

# --- МАРШРУТЫ СЕРВЕРА ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sites', methods=['GET'])
def get_sites():
    return jsonify(PRIORITY_SITES)

@app.route('/api/stop', methods=['POST'])
def stop_download():
    global stop_requested
    stop_requested = True
    return jsonify({"status": "success", "message": "Остановка следующего файла..."})

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT site, tags, files_added, size_bytes, timestamp FROM downloads ORDER BY id DESC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        
        history_list = []
        for row in rows:
            history_list.append({
                "site": row[0],
                "tags": row[1],
                "files_added": row[2],
                "size_formatted": format_size(row[3]),
                "timestamp": row[4]
            })
        return jsonify(history_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/start_download', methods=['GET'])
def start_download():
    global stop_requested
    stop_requested = False
    
    site = request.args.get('site')
    tags_input = request.args.get('tags', '')
    sort_folders = request.args.get('sort') == 'true'
    
    def generate():
        global stop_requested
        tags_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        if not tags_list:
            yield f"data: ❌ Введите теги.\n\n"
            yield f"data: [DONE]\n\n"
            return

        total_files, total_size = 0, 0
        summary_report = "✨ ИТОГОВЫЙ ОТЧЕТ:\n"

        for tag in tags_list:
            if stop_requested:
                summary_report += f"\n🛑 Отменено: {tag}"
                yield f"data: 🛑 Загрузка отменена пользователем!\n\n"
                break
            
            yield f"data: Подготовка: {tag}...\n\n"
            save_path = os.path.join(BASE_DIR, site, tag) if sort_folders else os.path.join(BASE_DIR, site)
            
            site_info = PRIORITY_SITES.get(site)
            url = site_info["url"].format(tag) if site_info and site != "Другой сайт" else tag
            
            files_before, size_before = get_dir_stats(save_path)
            
            try:
                # Устанавливаем директорию напрямую
                gdl_config.set(("extractor",), "base-directory", save_path)
                
                job = gdl_job.DownloadJob(url)
                
                def run_job():
                    try:
                        job.run()
                    except Exception as e:
                        print(f"Job error: {e}")
                
                dl_thread = threading.Thread(target=run_job)
                dl_thread.start()
                
                while dl_thread.is_alive():
                    if stop_requested:
                        yield f"data: 🛑 Останавливаем загрузку текущего тега...\n\n"
                        break
                    yield f"data: 📥 Скачивание в процессе...\n\n"
                    dl_thread.join(1.0)

                files_after, size_after = get_dir_stats(save_path)
                diff_files = files_after - files_before
                diff_size = size_after - size_before
                total_files += diff_files
                total_size += diff_size
                
                if diff_files == 0:
                    status = f"• ⚠️ {tag}: Ошибка или пусто" if files_before == 0 else f"• 🔄 {tag}: Уже скачано"
                else:
                    status = f"• ✅ {tag}: +{diff_files} шт. ({format_size(diff_size)})"
                    
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            "INSERT INTO downloads (site, tags, files_added, size_bytes, timestamp) VALUES (?, ?, ?, ?, ?)",
                            (site, tag, diff_files, diff_size, timestamp)
                        )
                        conn.commit()
                        conn.close()
                    except Exception as db_err:
                        yield f"data: ⚠️ Ошибка БД: {db_err}\n\n"
                
                summary_report += status + "\n"
                yield f"data: {status}\n\n"
                    
            except Exception as e:
                summary_report += f"• ❌ {tag}: Ошибка ({e})\n"
                yield f"data: ❌ Ошибка: {e}\n\n"
                
        summary_report += "━" * 20 + f"\nВсего новых: {total_files}\nОбъем: {format_size(total_size)}"
        for line in summary_report.split('\n'):
            yield f"data: {line}\n\n"
            
        yield f"data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')
                        
