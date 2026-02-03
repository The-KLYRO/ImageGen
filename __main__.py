from telegram import Update, Bot
from telegram.ext import (Application,ContextTypes)
import warnings

from src.Config import (TOKEN,PORT,Webhook_url)
import src.Commands as commands 

warnings.filterwarnings(action="ignore", category=DeprecationWarning)

print("Starting up bot...")

async def post_init(application: Application):
    # Runs once after the app is initialized (and inside a running event loop)
    if Webhook_url and Webhook_url != "False":
        try:
            await application.bot.set_webhook(Webhook_url + TOKEN)
            print("Webhook set ✅")
        except Exception as e:
            print("Failed to set webhook:", e)
    else:
        print("Webhook url not found, running normal polling....")

def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)   # ✅ proper place for async startup work
        .build()
    )
    for h in commands.list:app.add_handler(h)
    app.add_error_handler(error_handler)

    print("Running...")
    if Webhook_url and Webhook_url != "False":
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=Webhook_url,
        )
    else:
        app.run_polling(poll_interval=0)
