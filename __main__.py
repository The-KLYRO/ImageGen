from telegram import Update, Bot
from telegram.ext import (Application,ContextTypes)
import warnings

from src.Config import (TOKEN,PORT,Webhook_url)
import src.Commands as commands 

warnings.filterwarnings(action="ignore", category=DeprecationWarning)


async def post_init(app: Application):
    me = await app.bot.get_me()
    mode = "webhook" if (Webhook_url and Webhook_url != "False") else "polling"
    print(f"Bot started ✅ @{me.username} ({mode})")

async def post_shutdown(app: Application):
    print("Stopping bot... 🛑")

async def post_stop(app: Application):
    print("Bot stopped ✅")

def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .post_stop(post_stop)
        .build()
    )
    for h in commands.list:app.add_handler(h)
    app.add_error_handler(error)

    try:
        if Webhook_url and Webhook_url != "False":
            print('webhook : ', Webhook_url)
            app.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                webhook_url=Webhook_url,
            )
        else:
            app.run_polling(poll_interval=0)
    except Exception as e:
        print(e)