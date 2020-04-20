from celery import Celery
from .config import Config
from importlib import import_module


def discover_jobs():
    """
    Discover all jobs on jobs folder
    """
    from os import listdir

    job_list = [
        'jobs.' + job.split(".")[0]
        for job in listdir('./jobs')
        if (job.endswith('.py') and
            not job.startswith('_'))
    ]

    return job_list


# Create celery instance and aplly the config
pylineup = Celery('pylineup')
pylineup.config_from_object(Config())

# Load the jobs
for job in discover_jobs():
    try:
        job_module = import_module(job)
        job_module.task.signature()
    except Exception as e:
        print(f'Error loading job: {job} because: {e}')
