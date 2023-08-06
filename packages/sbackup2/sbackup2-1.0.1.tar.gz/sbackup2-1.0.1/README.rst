sbackup2
========

Requirements
------------

- python3
- sshpass
- mysqldump
- click


Set up
------
::

    pip install sbackup2


Sample task config
------------------

Default placed in ``/etc/sbackup2.d/``. ``sbackup2`` loads all tasks with ``*.conf``.
::

    {
      "options": {
        "sftp_host": "sftp.selcdn.ru",
        "sftp_user": "USER",
        "sftp_password": "PASSWORD",
        "sftp_options": "-oBatchMode=no",
        "sftp_remote_dir": "DIR",
        "file_name_tpl": "{host_name}_{year}_{month}_{day}__{hour}_{minutes}_{seconds}.tar.bz2"
      },
      "tasks": [
        {
          "fd": [
            "/var/www/",
            "/etc/nginx/nginx.conf"
          ],
          "db": [
            ["mysql", "db1"],
            ["mysql", "db2"],
            ["psql", "db1"]     // postgresql not support yet
          ]
        }
      ]
    }


DB's
----
MySQL
^^^^^

For access to databases you should create the file ``/<user>/.my.cfg`` with context::

    [client]
    user=root
    password=PASSWORD

