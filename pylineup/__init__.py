from celery import Celery
from .config import Config
from importlib import import_module
from os import listdir

# Create celery instance and aplly the config
pylineup = Celery('pylineup')
pylineup.config_from_object(Config())

# Discover all jobs on jobs folder
jobs = [
    'jobs.' + job.split(".")[0]
    for job in listdir('./jobs')
    if (job.endswith('.py') and
        not job.startswith('_'))
]

# Load the jobs
if len(jobs) > 0:
    for job in jobs:
        try:
            job_module = import_module(job)
            job_module.task.signature()
        except Exception as e:
            print(f'Error loading job: {job} because: {e}')
else:
    print('No jobs found!')
