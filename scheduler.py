import schedule
import time
import asyncio
from main import main_async

def run_crawler():
    asyncio.run(main_async())

schedule.every().day.at("09:00").do(run_crawler)

while True:
    schedule.run_pending()
    time.sleep(1)
