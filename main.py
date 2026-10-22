from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Мой Mini App</title>
            <script src="https://telegram.org/js/telegram-web-app.js"></script>
        </head>
        <body>
            <h1>Привет, это мой Mini App!</h1>
            <p>Скоро здесь будет что-то крутое.</p>
            <script>
                // Инициализация Telegram WebApp (пока просто чтобы не было ошибок)
                let tg = window.Telegram.WebApp;
                tg.ready();
                tg.expand();
            </script>
        </body>
    </html>
    """