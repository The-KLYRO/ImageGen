import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
API = os.environ.get('API')
_raw = os.getenv("Webhook_url", "")


Webhook_url = _raw.strip()
if Webhook_url.lower() in ("", "false", "0", "none", "null"):
    Webhook_url = None