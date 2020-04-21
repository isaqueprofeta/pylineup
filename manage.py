#!/usr/bin/python3
import click
from subprocess import run


@click.group()
def manage():
    """
    Controls for pylineup schedule micro-framework
    """
    pass


@manage.group()
def application():
    """
    Simplified controls for container/service management
    """
    pass


@application.command()
def install():
    """
    Build and/or start docker-compose structure
    """

    command = """
        echo 'Building and starting services...';
        docker-compose up -d
        """
    run(command, shell=True)


@application.command()
def uninstall():
    """
    Stop and remove containers, volumes and data from schedule/queue
    """

    command = """
        echo 'Removing all services and history data...';
        docker-compose down -v
        """
    run(command, shell=True)


@application.command()
def reinstall():
    """
    Rebuild and restart docker-compose structure
    """

    command = """
        echo 'Removing all services and history data...';
        docker-compose down -v
        """
    run(command, shell=True)

    command = """
        echo 'Building and starting services...';
        docker-compose up -d
        """
    run(command, shell=True)


@application.command()
def status():
    """
    Status of services
    """

    command = """
        echo 'Status of docker-compose structure';
        docker-compose ps
        """
    run(command, shell=True)


@application.command()
def restart():
    """
    Reset without wiping volumes and data from schedule/queue
    """

    command = """
        echo 'Removing services without wiping log data...';
        docker-compose down
        """
    run(command, shell=True)

    command = """
        echo 'Starting services...';
        docker-compose up -d
        """
    run(command, shell=True)


@manage.group()
def schedule():
    """
    Simplified controls for schedule management
    """
    pass


@schedule.command()
def start_all():
    """
    Start all discovered job schedules
    """

    command = """
        echo 'Starting all schedules from jobs...';
        docker exec -i worker
        python -c 'from pylineup.scheduler import Scheduler;
                   Scheduler.start_all_schedules()'
        """
    run(command.replace('\n', ' '), shell=True)


@schedule.command()
def show():
    """
    List the current schedule table
    """

    command = """
        echo 'Listing current schedules...';
        docker exec -i worker
        python -c 'from pylineup.scheduler import Scheduler;
                   Scheduler.show_all_schedules()'
        """
    run(command.replace('\n', ' '), shell=True)


@schedule.command()
@click.option('--job',
              required=True,
              help='Job name')
def start(job):
    """
    Start the schedule for a job
    """

    command = f"""
        echo 'Starting schedule...';
        docker exec -i worker
        python -c 'from pylineup.scheduler import Scheduler;
                   Scheduler.start_an_schedule("{job}")'
        """
    run(command.replace('\n', ' '), shell=True)


@schedule.command()
@click.option('--job',
              required=True,
              help='Job name')
def stop(job):
    """
    Remove the schedule for a job
    """

    command = f"""
        echo 'Removing schedule...';
        docker exec -i beat
        python -c 'from pylineup.scheduler import Scheduler;
                   Scheduler.stop_an_schedule("{job}")'
        """
    run(command.replace('\n', ' '), shell=True)


@manage.group()
def job():
    """
    Simplified controls for job management
    """
    pass


@job.command()
def list():
    """
    List jobs discovered from jobs directory
    """

    command = """
        docker exec -i worker
        sh -c 'celery -A pylineup inspect registered'
        """
    run(command.replace('\n', ' '), shell=True)


@job.command()
def running():
    """
    List currently running jobs
    """

    command = """
        docker exec -i worker
        sh -c 'celery -A pylineup inspect active'
        """
    run(command.replace('\n', ' '), shell=True)


@job.command()
@click.option('--job',
              required=True,
              help='Job name')
def execute(job):
    """
    Execute a job manually
    """

    command = f"""
        docker exec -i worker
        sh -c 'celery -A pylineup call jobs.{job}.task'
        """
    run(command.replace('\n', ' '), shell=True)


@job.command()
@click.option('--job',
              required=True,
              help='Job name')
def terminate(job):
    """
    Kill/Stop a job running
    """

    command = f"""
        docker exec -i worker
        sh -c 'celery -A pylineup control revoke jobs.{job}.task'
        """
    run(command.replace('\n', ' '), shell=True)


@job.command()
@click.option('--job',
              required=True,
              help='Job name')
def script(job):
    """
    Run job as a python script wihout queuing
    """

    command = f"""
        echo 'Running {job} as a script...';
        docker exec -i worker
        python -c 'from jobs.{job} import task;
                   task()'
        """
    run(command.replace('\n', ' '), shell=True)


@job.command()
def celery_stats():
    """
    Stats directly from celery worker
    """

    command = """
        docker exec -i worker
        sh -c 'celery -A pylineup inspect stats'
        """
    run(command.replace('\n', ' '), shell=True)


if __name__ == '__main__':
    manage()
