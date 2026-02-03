import os
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
Webhook_url = os.environ.get('Webhook_url', False)