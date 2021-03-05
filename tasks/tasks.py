from celery import shared_task
import time


@shared_task
def celery_task(counter):
    email = "admin@example.com"
    time.sleep(5)
    return f'{counter} Done!'
