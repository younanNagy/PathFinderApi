from celery import shared_task
from time import sleep
from .PathService import findPath

@shared_task(bind=True)
def slow_find_path_task(self, from_name, to_name):
    sleep(5)
    return findPath(from_name, to_name)