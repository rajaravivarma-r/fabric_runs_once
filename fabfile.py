"""Run a fabric task only once even though it is decorated as parallel"""

import datetime
import running

from fabric.api import roles, env, task, parallel, run
from fabric.colors import red

TIME_STAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

env.roledefs = {
    'application_servers':
        {'hosts': ['192.168.56.10{}'.format(i) for i in range(1, 6)]},
}

env.user = 'raja'

@task
@parallel
@roles('application_servers')
@running.runs_once(marker='file_mutex_{time}'.format(time=TIME_STAMP))
def db_migration():
    """This task runs only on one host even though it is decorated with `parallel`"""
    run("bundle exec rake db:migrate")

@task
@parallel
@roles('application_servers')
@running.runs_once(marker='file_mutex_{time}'.format(time=TIME_STAMP),
                    error_msg=red("Migration is already running in one host"))
def db_migration():
    """This task runs only on one host even though it is decorated with `parallel`"""
    run("bundle exec rake db:migrate")
