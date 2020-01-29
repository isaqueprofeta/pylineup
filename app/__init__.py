import configparser
from celery import Celery
from os import listdir

config_file = configparser.ConfigParser()
config_file.read("config.ini")


class Config:
    """Configuration for Celery with redis backend"""

    BROKER_URL = config_file.get('redis', 'broker')
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 15000}

    CELERY_TIMEZONE = config_file.get('app', 'timezone')
    CELERY_RESULT_BACKEND = config_file.get('redis', 'backend')
    CELERY_REDIS_SCHEDULER_URL = config_file.get('redis', 'scheduler')

    CELERYBEAT_SCHEDULER = 'redisbeat.RedisScheduler'

    CELERYD_TASK_TIME_LIMIT = '2000'


# Create celery instance and aplly the config
pylineup = Celery('pylineup')
pylineup.config_from_object(Config)

# Discover all jobs on jobs folder
job_list = [
    'jobs.' + job.split(".")[0]
    for job in listdir('./jobs')
    if not job.startswith('_')
]
pylineup.autodiscover_tasks(
    job_list, force=True)


# Bunch of support functions
def start_an_schedule(job_name):
    """
    Start the schedule for a specific job
    """
    exec("""import jobs; jobs.%s.schedule()"""
         % job_name)


def stop_an_schedule(job_name, app=pylineup):
    """
    Stop the schedule for a specific job
    """
    from redisbeat.scheduler import RedisScheduler

    schduler = RedisScheduler(app=app)

    result = schduler.remove(job_name)

    print("Removed schedule for job: ", job_name, result)


def start_all_schedules():
    """
    Start all schedules from schedule function
    on each job inside jobs folder
    """
    for carga in listdir('./jobs'):
        if not carga.startswith('_'):
            nome_carga = carga.split(".")[0]
            exec("""import jobs; jobs.%s.schedule()"""
                 % nome_carga)


def show_all_schedules():
    """
    Display all running schedules
    """
    from redisbeat.scheduler import RedisScheduler
    import jsonpickle
    import celery.schedules

    scheduler = RedisScheduler(app=pylineup)
    data = [
        jsonpickle.decode(entry)
        for entry in scheduler.rdb.zrange(scheduler.key, 0, -1)
    ]

    for task in data:
        if isinstance(task.schedule, celery.schedules.schedule):
            print("""Job: %s each %s last execution in %s"""
                  % (task.task,
                      task.schedule.human_seconds,
                      task.last_run_at))
        elif isinstance(task.schedule, celery.schedules.crontab):
            print("""Job: %s crontab %s %s %s %s %s last execution in %s"""
                  % (task.task,
                      task.schedule._orig_minute,
                      task.schedule._orig_hour,
                      task.schedule._orig_day_of_month,
                      task.schedule._orig_month_of_year,
                      task.schedule._orig_day_of_week,
                      task.last_run_at))
