from celery import Celery
from .config import Config


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
pylineup.autodiscover_tasks(
    discover_jobs(),
    force=True
)
