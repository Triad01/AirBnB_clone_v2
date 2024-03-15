#!/usr/bin/python3
''' This is a fabric file that deploys versions to remote servers'''

from datetime import datetime
from fabric.api import run, put, env, local
import os

env.hosts = ['34.232.69.133', '54.209.193.30']


def do_pack():
    ''' This function creates an archive and stores it in versions folder '''

    if not os.path.exists('versions'):
        local('mkdir versions')

    now = datetime.now()
    arch_file = 'versions/web_static{}.tgz'.format(
        now.strftime("%Y%m%d%H%M%S")
    )

    command = local("tar -cvzf {} web_static".format(arch_file))
    if not command.failed:
        return arch_file


def do_deploy(archive_path):
    ''' Deploys a version to the web servers '''

    if not os.path.exists(archive_path):
        return False

    try:
        unzipped = archive_path[9:-4]
        put(archive_path, '/tmp/')

        run("mkdir /data/web_static/releases/new")
        run("tar -xzf /tmp/{} -C /data/web_static/releases/new/".format(
            archive_path[9:]))

        run("mv /data/web_static/releases/new/web_static\
        /data/web_static/releases/{}".format(unzipped))

        run('rm -r /tmp/{}'.format(archive_path[9:]))
        run('rm -r /data/web_static/releases/new/')
        run('rm -r /data/web_static/current')
        run('ln -s /data/web_static/releases/{}\
            /data/web_static/current'.format(unzipped))

    except Exception:
        return False

    return True


def deploy():
    ''' This function calls the previous methods for deployment '''

    arch_file = do_pack()

    if arch_file is None:
        return False

    return do_deploy(arch_file)
