import schedule
import time
from main import update_data

schedule.every().day.at("05:00:00").do(update_data)

print("Starting server...")

while True:
    schedule.run_pending()
    time.sleep(3600)