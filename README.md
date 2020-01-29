# PyLineUP - A crontab on python steroids

PyLineUP is a micro-framework to do some python scripting with queued scheduling and history, it was first created to do some ETL (Extract-Transform-Load) jobs.

## Prerequisites:

1) Before anything install python v3.6, docker and docker-compose in your preferred way.

2) Now install click (if you dont do this, read manage.py to understand the helper):
   ```sh
   pip install click
   ```

## How to use:

### 1) Clone the project and configure your timezone:

```sh
git clone https://github.com/isaqueprofeta/pylineup.git
```

```sh
cp config.ini.example config.ini
vim config.ini
```

### 2) Dump your python scripts in jobs folder of this project, and then add the following "little" header for each of them:

```python
import os
from app import pylineup
from datetime import timedelta

job_name = os.path.splitext(os.path.basename(__file__))[0]

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
    print("Schedule of %s: %s"
          % (job_name, result))


@pylineup.task()
def task():
####### WROTE YOUR SCRIPT FROM HERE #######
```

Take note that there's a function that define the schedule and you shoud change the MY_SCHEDULE variable for your needs (or just comment out/remove the whole function to not schedule it):

- You can do some classic timedelta like the header above // [Python timedelta docs](https://docs.python.org/3/library/datetime.html)

  ```python
  from datetime import timedelta

  MY_SCHEDULE = timedelta(days=50)
  MY_SCHEDULE = timedelta(seconds=27)
  MY_SCHEDULE = timedelta(microseconds=10)
  MY_SCHEDULE = timedelta(milliseconds=29000)
  MY_SCHEDULE = timedelta(minutes=5)
  MY_SCHEDULE = timedelta(hours=8)
  MY_SCHEDULE = timedelta(weeks=2)
  ```

- Or you can do some really classic crontab line // [Celery scheduler docs](https://docs.celeryproject.org/en/stable/reference/celery.schedules.html):

  ```python
  from celery.schedules import crontab

  MY_SCHEDULE = crontab(minute='59', hour='17', day_of_week='mon-fri', day_of_month='1-30', month_of_year='1-12')
  ```

### 3) Manage the framework:

- Setup the docker-compose manually or with the helper:

  ```sh
  # Manually
  docker-compose up -d
  
  # Using the helper
  ./manage.py application install
  ```

- To discover new jobs/scripts that you added to jobs folder, you need to restart the docker-compose services:

  ```sh
  ./manage.py application restart
  
  Removing services without wiping log data...
  Stopping flower ... done
  Stopping beat   ... done
  Stopping worker ... done
  Stopping redis  ... done
  Removing flower ... done
  Removing beat   ... done
  Removing worker ... done
  Removing redis  ... done
  Creating redis ... done
  Creating worker ... done
  Creating beat ... done
  Creating flower ... done
  Creating worker ... done
  Creating beat ... done
  Creating flower ... done 
  ```

- Show container status

  ```sh
  ./manage.py application status
  
  Status of docker-compose structure
   Name               Command               State           Ports         
  ------------------------------------------------------------------------
  beat     celery beat --app=app:pyli ...   Up                            
  flower   celery flower --app=app:py ...   Up      0.0.0.0:80->80/tcp    
  redis    docker-entrypoint.sh redis ...   Up      0.0.0.0:6379->6379/tcp
  worker   celery worker --app=app:py ...   Up                            
  ```


### 5) Manage your jobs:

- List discovered jobs to celery:

  ```sh
  ./manage.py job list
  
  -> jobs@worker: OK
      * jobs.test_job.task
  ```

- Manually queue a job for execution:

  ```sh
  ./manage.py job execute --job test_job

  ec0d712a-7ff1-4e54-a4a1-e94270796517
  ```

- Show running jobs:

  ```sh
  ./manage.py job running

  -> jobs@worker: OK
      * {'id': '7cac6a4b-f2e4-496f-ba4b-99d115bf9755', 'name': 'jobs.test_job.task', 'args': [], 'kwargs': {}, 'type': 'jobs.test_job.task', 'hostname': 'jobs@worker', 'time_start': 1580321055.6998305, 'acknowledged': True, 'delivery_info': {'exchange': '', 'routing_key': 'celery', 'priority': 0, 'redelivered': None}, 'worker_pid': 17}
  ```

- Manually stop a job in execution:

  ```sh
  ./manage.py job terminate --job test_job
  -> jobs@worker: OK
          tasks jobs.test_job.task flagged as revoked
  ```

- Execute a job outside worker (as a classic python script):

  ```sh
  ./manage.py job script --job test_job

  Running test_job as a script...
  Starting:  test_job
  My result from a not so complex logic
  Ending: test_job
  ```

All container logs (INFO level by default) are available in logs directory:

```sh
cat logs/celeryworker.log

[2020-01-28 20:14:59,629: INFO/MainProcess] Received task: jobs.test_job.task[ec0d712a-7ff1-4e54-a4a1-e94270796517]  
[2020-01-28 20:14:59,787: WARNING/ForkPoolWorker-7] Starting:  test_job
[2020-01-28 20:14:59,893: WARNING/ForkPoolWorker-7] My result from a not so complex logic
[2020-01-28 20:14:59,894: WARNING/ForkPoolWorker-7] Ending: test_job
[2020-01-28 20:15:00,018: INFO/ForkPoolWorker-7] Task jobs.test_job.task[ec0d712a-7ff1-4e54-a4a1-e94270796517] succeeded in 0.2552589990082197s: None
```

### 5) Manage your schedule:

- Start all schedules:

  ```sh
  ./manage.py schedule start-all
  
  Starting all schedules from jobs...
  Schedule of test_job: True
  ```

- Start one schedule:

  ```sh
  ./manage.py schedule start --job test_job

  Starting schedule...
  Schedule of test_job: True
  ```

- Stop one schedule:

  ```sh
  ./manage.py schedule stop --job test_job

  Removing schedule...
  Removed schedule for job:  test_job True
  ```

- Show current schedules table:

  ```sh
  ./manage.py schedule show

  Listing current schedules...
  Job: jobs.test_job.task each 30.00 seconds last execution in 2020-01-29 10:45:14.665523-03:00
  ```

## Extending the framework to your needs:

### Python libraries

- Add your dependencies from pip on requirements.txt
- Add your dependencies from libraries on O.S. on Dockerfile (alpine based image)
