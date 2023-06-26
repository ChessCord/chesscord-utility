from threading import Thread
from dotenv import load_dotenv
import os

from bot import client, update_status, heartbeat
from app import run_webserver

load_dotenv()

webserver = Thread(target=run_webserver)
webserver.start()

update_status.start()
heartbeat.start()

client.run(os.getenv("TOKEN"))
