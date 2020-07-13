from pylineup import pylineup
from datetime import timedelta
from celery.utils.log import get_task_logger
import os

job_name = os.path.splitext(os.path.basename(__file__))[0]
logger = get_task_logger(__name__)

MY_SCHEDULE = timedelta(seconds=300)


def schedule():
    """
    Sampled schedule
    """
    from redisbeat.scheduler import RedisScheduler

    schedule = RedisScheduler(app=pylineup)
    result = schedule.add(**{
        'name': job_name,
        'task': 'jobs.' + job_name + '.task',
        'schedule': MY_SCHEDULE,
        'args': ()
    })
    print(f"Schedule of {job_name}: {result}")


@pylineup.task()
def task():
    # Make your imports here at top
    from time import sleep

    # Extract
    my_data = ['My', 'result', 'from', 'a',
               'not', 'so', 'complex', 'logic']

    my_plus_data = ' '

    # Transform
    my_beatiful_result = my_plus_data.join(my_data)
    sleep(10)

    # Load
    logger.info(my_beatiful_result)
