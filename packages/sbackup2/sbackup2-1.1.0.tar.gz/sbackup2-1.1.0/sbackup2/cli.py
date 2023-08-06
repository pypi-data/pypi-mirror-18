# coding: utf-8

import os
from logging import error

import click

import sbackup2.task
import sbackup2.utils


key_verbose = click.option(
    '--verbose', help='show message', is_flag=True, default=False)


@click.group()
def cli():
    pass


@cli.command()
@key_verbose
@click.option('--task', help='Use only this task')
@click.option('--tasks', help='Directory where placed task configs',
              default='/etc/sbackup2.d')
@click.option('--rm-tmp', help='delete temp directory', is_flag=True,
              default=False)
def backup(task, tasks, rm_tmp, verbose):
    if verbose:
        sbackup2.utils.define_log()

    if task:
        tasks_list = [os.path.abspath(task)]

    elif tasks:
        tasks_list = sbackup2.utils.get_task_files(tasks)

    else:
        return False

    for item in tasks_list:
        if not sbackup2.task.execute_task(item, rm_tmp):
            error('Executed tasks {} is not success...'.format(item))

    return True
