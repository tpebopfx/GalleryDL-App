import os
import subprocess
import atexit
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

# --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ---
current_process = None
stop_requested = False
DB_NAME = "history.db" # Имя файла нашей базы данных

# --- БАЗА ДАННЫХ (Инициализация) ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Создаем таблицу, если ее нет
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
    conn.close()

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
    global current_process, stop_requested
    stop_requested = True
    if current_process:
        current_process.terminate()
        return jsonify({"status": "success", "message": "Остановка..."})
    return jsonify({"status": "error", "message": "Нет активных загрузок."})

# Получение истории из базы данных
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Достаем последние 50 загрузок, сортируем от новых к старым
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

# Главный маршрут скачивания
@app.route('/api/start_download', methods=['GET'])
def start_download():
    global current_process, stop_requested
    stop_requested = False
    
    site = request.args.get('site')
    tags_input = request.args.get('tags', '')
    sort_folders = request.args.get('sort') == 'true'
    
    def generate():
        global current_process, stop_requested
        tags_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        if not tags_list:
            yield f"data: ❌ Введите теги.\n\n"
            yield f"data: [DONE]\n\n"
            return

        base_dir = "/sdcard/Download/GalleryDL_App"
        total_files, total_size = 0, 0
        summary_report = "✨ ИТОГОВЫЙ ОТЧЕТ:\n"

        for tag in tags_list:
            if stop_requested:
                summary_report += f"\n🛑 Отменено: {tag}"
                yield f"data: 🛑 Загрузка отменена пользователем!\n\n"
                break
            
            yield f"data: Подготовка: {tag}...\n\n"
            save_path = os.path.join(base_dir, site, tag) if sort_folders else os.path.join(base_dir, site)
            
            site_info = PRIORITY_SITES.get(site)
            url = site_info["url"].format(tag) if site_info and site != "Другой сайт" else tag
            
            command = ["gallery-dl", "--directory", save_path, url]
            files_before, size_before = get_dir_stats(save_path)
            
            try:
                current_process = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
                )
                
                for line in current_process.stdout:
                    if stop_requested:
                        break
                    clean_line = line.strip()[-50:] 
                    yield f"data: 📥 {clean_line}\n\n"
                
                current_process.wait()
                
                files_after, size_after = get_dir_stats(save_path)
                diff_files = files_after - files_before
                diff_size = size_after - size_before
                total_files += diff_files
                total_size += diff_size
                
                if diff_files == 0:
                    status = f"• ⚠️ {tag}: Ошибка или пусто" if files_before == 0 else f"• 🔄 {tag}: Уже скачано"
                else:
                    status = f"• ✅ {tag}: +{diff_files} шт. ({format_size(diff_size)})"
                    
                    # --- СОХРАНЕНИЕ В БАЗУ ДАННЫХ ---
                    try:
                        conn = sqlite3.connect(DB_NAME)
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
            
        current_process = None
        yield f"data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')

#if __name__ == '__main__':
    # При запуске сервера проверяем и создаем базу данных
#    init_db()
#    app.run(debug=True, host='0.0.0.0', port=5000)
