import json
import os
import tornado.ioloop
import tornado.web
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(text):
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=text)

class TelegramHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            text = data.get("text")

            if not text:
                self.set_status(400)
                self.write({"error": "Field 'text' is required."})
                return

            send_telegram_message(text)
            self.write({"status": "Message successfully sent to Telegram."})

        except json.JSONDecodeError as exception:
            self.set_status(400)
            self.write({"error": f"Invalid JSON: {str(exception)}"})
        except Exception as exception:
            from telegram.error import TelegramError
            if isinstance(exception, TelegramError):
                self.set_status(502)
                self.write({"error": f"Telegram API error: {str(exception)}"})
            else:
                self.set_status(500)
                self.write({"error": str(exception)})

def make_app():
    return tornado.web.Application([
        (r"/mensagem", TelegramHandler),
    ])

def start_telegram_service():
    app = make_app()
    app.listen(8888)
    print("Server running in http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

start_telegram_service()
