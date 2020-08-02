import json

from nexuscli.cli import util


def cmd_list(nexus_client, **kwargs):
    """Performs `nexus3 task list`"""
    tasks = nexus_client.tasks.list()

    if kwargs.get('json'):
        print(json.dumps(tasks))
    else:
        util.print_as_table(tasks['items'], ['id', 'name', 'currentState', 'lastRunResult'])


def cmd_show(nexus_client, task_id):
    """Performs `nexus3 task show`"""
    task = nexus_client.tasks.show(task_id)
    print(json.dumps(task))


def cmd_run(nexus_client, task_id):
    """Performs `nexus3 task run`"""
    nexus_client.tasks.run(task_id)


def cmd_stop(nexus_client, task_id):
    """Performs `nexus3 task stop`"""
    nexus_client.tasks.stop(task_id)
