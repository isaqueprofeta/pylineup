class Scheduler():
    """
    Suport functions for beat scheduler
    """
    def start_an_schedule(job_name):
        """
        Start the schedule for a specific job
        """
        import importlib
        job_module = importlib.import_module(
                                    f'jobs.{job_name.split(".")[0]}')
        try:
            job_module.schedule()
        except Exception as e:
            print(f"Failed to create schedule for {job_name}: {e} ")

    def stop_an_schedule(job_name):
        """
        Stop the schedule for a specific job
        """
        from pylineup import pylineup
        from redisbeat.scheduler import RedisScheduler

        try:
            schduler = RedisScheduler(app=pylineup)
            schduler.remove(job_name)
        except Exception as e:
            print(f"Failed to remove schedule for {job_name}: {e} ")

    def start_all_schedules():
        """
        Start all schedules from schedule function
        on each job inside jobs folder
        """
        from os import listdir
        import importlib

        # Discover all schedule for jobs on jobs folder
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
                    job_module = importlib.import_module(job)
                    job_module.schedule()
                except Exception as e:
                    print(f'Error creating schedule for {job}: {e}')
        else:
            print('No jobs found!')

    def show_all_schedules():
        """
        Display all running schedules
        """
        from pylineup import pylineup
        from redisbeat.scheduler import RedisScheduler
        import jsonpickle
        import celery.schedules

        scheduler = RedisScheduler(app=pylineup)
        data = [
            jsonpickle.decode(entry)
            for entry in scheduler.rdb.zrange(scheduler.key, 0, -1)
        ]

        if len(data) > 0:
            for task in data:
                if isinstance(task.schedule, celery.schedules.schedule):
                    print(
                        f"Job: {task.task}"
                        f" each {task.schedule.human_seconds}"
                        f" last execution in {task.last_run_at}"
                    )
                elif isinstance(task.schedule, celery.schedules.crontab):
                    print(
                        f"Job: {task.task}"
                        f" crontab {task.schedule._orig_minute}"
                        f" {task.schedule._orig_hour}"
                        f" {task.schedule._orig_day_of_month}"
                        f" {task.schedule._orig_month_of_year}"
                        f" {task.schedule._orig_day_of_week}"
                        f" last execution in {task.last_run_at}"
                    )
        else:
            print('No active schedules found.')
