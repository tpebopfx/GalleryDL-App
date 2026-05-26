document.addEventListener("DOMContentLoaded", () => {
    
    const siteSelect = document.getElementById("site-select");
    const tagsInput = document.getElementById("tags-input");
    const tagsInfo = document.getElementById("tags-info");
    const settingsBtn = document.getElementById("settings-btn");
    const settingsContent = document.getElementById("settings-content");
    
    let sitesData = {};

    // 1. Настройки (Аккордеон)
    settingsBtn.addEventListener("click", () => {
        settingsContent.classList.toggle("show");
    });

    // Функция обновления подсказок
    function updateHints(selectedSite) {
        if (sitesData && sitesData[selectedSite]) {
            const hint = sitesData[selectedSite];
            tagsInput.placeholder = hint.placeholder || "Введите теги...";
            tagsInfo.textContent = hint.info || "";
        } else {
            tagsInput.placeholder = "Введите теги...";
            tagsInfo.textContent = "";
        }
    }

    siteSelect.addEventListener("change", (event) => {
        updateHints(event.target.value);
    });

    // 2. ЗАГРУЗКА САЙТОВ ИЗ БЭКЕНДА
    fetch("/api/sites")
        .then(response => {
            if (!response.ok) throw new Error(`Ошибка сервера: ${response.status}`);
            return response.json();
        })
        .then(data => {
            sitesData = data;
            siteSelect.innerHTML = "";
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    const option = document.createElement("option");
                    option.value = key;
                    option.textContent = key;
                    siteSelect.appendChild(option);
                }
            }
            if (siteSelect.value) updateHints(siteSelect.value);
        })
        .catch(error => {
            console.error("Ошибка:", error);
            tagsInput.placeholder = "Ошибка соединения";
            tagsInfo.innerHTML = `<span style="color: #EF4444;">❌ Ошибка API: ${error.message}</span>`;
        });


    // --- НОВЫЙ КОД: ЛОГИКА ДЛЯ РАБОТЫ С ИСТОРИЕЙ ЗАГРУЗОК ---
    const historyContainer = document.getElementById("history-container");
    const refreshHistoryBtn = document.getElementById("refresh-history-btn");

    function loadHistory() {
        fetch("/api/history")
            .then(response => response.json())
            .then(data => {
                historyContainer.innerHTML = ""; // Очищаем контейнер
                
                if (data.error) {
                    historyContainer.innerHTML = `<p class="hint-text" style="color: #EF4444;">Ошибка: ${data.error}</p>`;
                    return;
                }
                
                if (data.length === 0) {
                    historyContainer.innerHTML = '<p class="hint-text">История пока пуста. Скачайте что-нибудь!</p>';
                    return;
                }

                // Перебираем записи и строим карточки
                data.forEach(item => {
                    const itemDiv = document.createElement("div");
                    itemDiv.className = "history-item";
                    
                    // Подсвечиваем зеленым, если скачались новые файлы
                    const filesColor = item.files_added > 0 ? "#10B981" : "#94A3B8";
                    
                    itemDiv.innerHTML = `
                        <div class="history-item-top">
                            <span>${item.site} • ${item.tags}</span>
                            <span style="color: ${filesColor}">+${item.files_added} шт.</span>
                        </div>
                        <div class="history-item-meta">
                            <span>Объем: ${item.size_formatted}</span>
                            <span>${item.timestamp}</span>
                        </div>
                    `;
                    historyContainer.appendChild(itemDiv);
                });
            })
            .catch(err => {
                console.error("Ошибка истории:", err);
                historyContainer.innerHTML = '<p class="hint-text" style="color: #EF4444;">Не удалось загрузить историю.</p>';
            });
    }

    // Первичная загрузка истории при открытии страницы
    loadHistory();
    
    // Ручное обновление по кнопке-стрелочке
    refreshHistoryBtn.addEventListener("click", loadHistory);


    // --- ЛОГИКА ЗАГРУЗКИ И ОСТАНОВКИ ---
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    const outputConsole = document.getElementById("output-console");
    const sortCheckbox = document.getElementById("sort-checkbox");
    
    let eventSource = null;

    function logToConsole(text) {
        outputConsole.value += text + "\n";
        outputConsole.scrollTop = outputConsole.scrollHeight;
    }

    startBtn.addEventListener("click", () => {
        const site = siteSelect.value;
        const tags = tagsInput.value;
        const sort = sortCheckbox.checked;

        if (!tags || tags === "Ожидание...") {
            logToConsole("❌ Ошибка: Введите теги перед началом загрузки.");
            return;
        }

        outputConsole.value = "";
        logToConsole(`🚀 Запуск загрузки...\nСайт: ${site}\nТеги: ${tags}\n`);
        startBtn.disabled = true;
        startBtn.style.opacity = "0.5";

        const url = `/api/start_download?site=${encodeURIComponent(site)}&tags=${encodeURIComponent(tags)}&sort=${sort}`;
        eventSource = new EventSource(url);

        eventSource.onmessage = function(event) {
            if (event.data === "[DONE]") {
                eventSource.close();
                logToConsole("\n✅ Процесс полностью завершен.");
                startBtn.disabled = false;
                startBtn.style.opacity = "1";
                
                // АВТООБНОВЛЕНИЕ: Загрузка завершилась — обновляем окошко истории!
                loadHistory();
            } else {
                logToConsole(event.data);
            }
        };

        eventSource.onerror = function(err) {
            eventSource.close();
            logToConsole("❌ Подключение прервано или завершено.");
            startBtn.disabled = false;
            startBtn.style.opacity = "1";
            loadHistory(); // На всякий случай обновляем и при ошибке
        };
    });

    stopBtn.addEventListener("click", () => {
        logToConsole("🛑 Отправка сигнала остановки...");
        fetch("/api/stop", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                logToConsole(data.message);
                if (eventSource) {
                    eventSource.close();
                    startBtn.disabled = false;
                    startBtn.style.opacity = "1";
                    loadHistory();
                }
            })
            .catch(err => logToConsole("❌ Ошибка при остановке: " + err));
    });
});
                          
