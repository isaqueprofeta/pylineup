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
                                    'jobs.' + job_name.split(".")[0])
        job_module.schedule()

    def stop_an_schedule(job_name):
        """
        Stop the schedule for a specific job
        """
        from pylineup import pylineup
        from redisbeat.scheduler import RedisScheduler

        schduler = RedisScheduler(app=pylineup)

        result = schduler.remove(job_name)

        print("Removed schedule for job: ", job_name, result)

    def start_all_schedules():
        """
        Start all schedules from schedule function
        on each job inside jobs folder
        """
        from os import listdir
        import importlib

        for job in listdir('./jobs'):
            if job.endswith('.py') and not job.startswith('_'):
                job_module = importlib.import_module(
                                            'jobs.' + job.split(".")[0])
                job_module.schedule()

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
