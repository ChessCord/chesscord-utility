from threading import Thread

from bot import client, update_status
from app import run_webserver

webserver = Thread(target=run_webserver)
webserver.start()

update_status.start()

client.run("ODc3MDE3MTA1NjIxNDc1MzM4.YRsf1A.aqAUNryGWW9vdG6horsAIbAh2qM")