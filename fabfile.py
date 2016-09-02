"""Run a fabric task only once even though it is decorated as parallel"""

import datetime
import running

from fabric.api import roles, env, task, parallel, run
from fabric.colors import red

TIME_STAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Replace this with your list of hosts.
env.roledefs = {
    'application_servers':
        {'hosts': ['192.168.56.10{}'.format(i) for i in range(1, 6)]},
}

# Replace the value with your ssh user name
env.user = 'raja'

# If you are using `sudo` instead of `run`
# env.sudo_user = 'application user'

@task
@parallel
@roles('application_servers')
@running.runs_once(marker='file_mutex_{time}'.format(time=TIME_STAMP))
def db_migration():
    """This task runs only on one host even though it is decorated with `parallel`"""
    run("echo 'Running migration'")

@task
@parallel
@roles('application_servers')
@running.runs_once(marker='/tmp/file_mutex_{time}'.format(time=TIME_STAMP),
                   error_msg=red("Migration is already running in one host"))
def db_migration_with_error_msg():
    """
    This task runs on one host even though it is decorated with `parallel`
    and prints the error message if attemted in other hosts.
    """
    run("echo 'Running migration'")
