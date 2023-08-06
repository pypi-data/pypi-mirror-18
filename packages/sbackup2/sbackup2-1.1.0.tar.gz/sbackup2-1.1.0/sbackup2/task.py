# coding: utf-8

import os
import shutil
import tempfile

import logbook

import sbackup2.utils

logbook.set_datetime_format('local')
logger = logbook.Logger('sbackup2')


def execute_task(task_file, rm_tmp):
    task_conf = sbackup2.utils.read_task_conf(task_file)
    task_options = task_conf.get('options', {})
    tasks = task_conf.get('tasks', [])
    tmp_dir = tempfile.mkdtemp(prefix='sbackup2_')
    tar_file = os.path.join(
        tmp_dir, sbackup2.utils.build_file_name(task_options))

    if not tasks:
        logger.info('Tasks not found')
        return False

    for task in tasks:
        db_dumps = sbackup2.utils.dump_db(tmp_dir, task.get('db', []))
        fd = task.get('fd', [])
        fd_exclude = task.get('fd_exclude', [])

        for item in db_dumps:
            fd.append(item)

        if not fd:
            continue

        try:
            logger.info('Creating TAR file ...')

            if sbackup2.utils.create_tar(tar_file, ' '.join(fd), fd_exclude):
                logger.info('Create TAR file is complete')
            else:
                logger.error('TAR file was not created')
                return False

            logger.info('Sending TAR file to remote host ...')

            if sbackup2.utils.sent_file(tmp_dir, task_options, tar_file) != 0:
                logger.info('File {} was send to remote host'.format(tar_file))
            else:
                logger.error('TAR file was not sent to remote host')
                return False

        finally:
            if rm_tmp:
                shutil.rmtree(tmp_dir)

    return True
