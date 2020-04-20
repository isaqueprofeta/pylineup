from pylineup import pylineup
import os

job_name = os.path.splitext(os.path.basename(__file__))[0]


def schedule():
    """
    Sampled schedule
    """
    from datetime import timedelta
    from redisbeat.scheduler import RedisScheduler

    schedule = RedisScheduler(app=pylineup)
    result = schedule.add(**{
        'name': job_name,
        'task': 'jobs.' + job_name + '.task',
        'schedule': timedelta(seconds=30),
        'args': ()
    })
    print("Schedule of %s: %s"
          % (job_name, result))


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
    print(my_beatiful_result)
