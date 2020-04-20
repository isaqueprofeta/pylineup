class Config:
    """
    Configuration for Celery with redis backend
    """
    import configparser

    config_file = configparser.ConfigParser()
    config_file.read("config.ini")

    BROKER_URL = config_file.get('redis', 'broker')
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 15000}

    CELERY_TIMEZONE = config_file.get('app', 'timezone')
    CELERY_RESULT_BACKEND = config_file.get('redis', 'backend')
    CELERY_REDIS_SCHEDULER_URL = config_file.get('redis', 'scheduler')

    CELERYBEAT_SCHEDULER = 'redisbeat.RedisScheduler'

    CELERYD_TASK_TIME_LIMIT = '2000'
