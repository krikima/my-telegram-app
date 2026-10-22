from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel  # Библиотека для проверки данных

app = FastAPI()

# 1. Создаём "модель" данных, которые мы ждём от телефона
class UserData(BaseModel):
    user_id: int
    first_name: str

# 2. Главная страница с кнопкой и скриптом
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Мой Mini App</title>
            <!-- Подключаем скрипт Telegram, чтобы знать, кто зашел -->
            <script src="https://telegram.org/js/telegram-web-app.js"></script>
            <style>
                body { font-family: sans-serif; padding: 20px; text-align: center; }
                button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
                #result { margin-top: 20px; font-weight: bold; color: #2e8b57; }
            </style>
        </head>
        <body>
            <h1>Привет, это мой Mini App!</h1>
            <p>Нажми на кнопку, чтобы отправить данные на сервер.</p>
            
            <button onclick="sendData()">Поздороваться с сервером</button>
            <div id="result"></div>

            <script>
                // Инициализируем Telegram WebApp
                let tg = window.Telegram.WebApp;
                tg.ready();
                tg.expand();

                // Функция, которая сработает при нажатии на кнопку
                async function sendData() {
                    // Берем данные пользователя прямо из Telegram
                    let user = tg.initDataUnsafe.user;
                    
                    if (!user) {
                        document.getElementById('result').innerText = "Ошибка: не удалось получить данные из Telegram.";
                        return;
                    }

                    // Отправляем POST-запрос на наш же сервер (по адресу /api/hello)
                    let response = await fetch('/api/hello', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            user_id: user.id,
                            first_name: user.first_name
                        })
                    });

                    // Ждем ответ от сервера и показываем его на экране
                    let data = await response.json();
                    document.getElementById('result').innerText = data.message;
                }
            </script>
        </body>
    </html>
    """

# 3. Наш API-эндпоинт (куда стучится кнопка)
@app.post("/api/hello")
async def say_hello(data: UserData):
    # Здесь мы принимаем данные и возвращаем ответ
    return {"message": f"Привет, {data.first_name}! Твой ID: {data.user_id}. Сервер тебя услышал!"}
