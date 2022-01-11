from threading import Thread
from dotenv import load_dotenv

from bot import client, update_status
from app import run_webserver

load_dotenv()

webserver = Thread(target=run_webserver)
webserver.start()

update_status.start()

client.run(os.getenv("TOKEN"))