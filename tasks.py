from celery_config import make_celery
from flask import Flask

app = Flask(__name__)

app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"

celery = make_celery(app)

@celery.task
def fivemin(task_name):
    print(f"You have only 5 minutes for completing your Task:{task_name}.")

@celery.task
def alarm_task(task_name):
    print(f"Time is up!! Your {task_name} is due")