from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time

from main import update_data

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', days=1, start_date=datetime.combine(datetime.today(), time(hour=5, minute=0)))
scheduler.start()