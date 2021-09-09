class Config:
    """
    Configuration for Celery with redis backend
    """
    import configparser

    config_file = configparser.ConfigParser()
    config_file.read("config.ini")

    broker_url = config_file.get('redis', 'broker')
    broker_transport_options = {'visibility_timeout': 15000}

    timezone = config_file.get('app', 'timezone')
    result_backend = config_file.get('redis', 'backend')
    CELERY_REDIS_SCHEDULER_URL = config_file.get('redis', 'scheduler')

    beat_scheduler = 'redisbeat.RedisScheduler'

    task_time_limit = '2000'
