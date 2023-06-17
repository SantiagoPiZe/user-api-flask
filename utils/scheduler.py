from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

counter = 0

def five_minute_counter():
    global counter
    counter += 1
    print(counter)

scheduler.add_job(five_minute_counter, 'interval', minutes=5)
scheduler.start()
