#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from datetime import datetime
from os import path
from os.path import exists


env.hosts = ['54.90.16.59', '100.25.150.206']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception as e:
        return False


"""
def do_deploy(archive_path):
    try:
        if not path.exists(archive_path):
            return False

        # Upload archive
        put(archive_path, '/tmp/')

        # Create target directory
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        target_dir = '/data/web_static/releases/web_static_{}/'.\
                format(timestamp)
        run('sudo mkdir -p {}'.format(target_dir))

        # Uncompress archive
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C {}'.\
                format(timestamp, target_dir))

        # Check if source directory is empty
        result = run('ls -A {}web_static/'.format(target_dir), warn=True)
        if result.succeeded and result.strip():
            # Move contents into target directory
            run('sudo mv {}web_static/* {}'.format(target_dir, target_dir))

            # Remove extraneous directories
            run('sudo rm -rf {}web_static'.format(target_dir))

            # Delete pre-existing symbolic link
            run('sudo rm -rf /data/web_static/current')

            # Re-establish symbolic link
            run('sudo ln -s {} /data/web_static/current'.format(target_dir))

            return True
        else:
            print("Source directory is empty.")
            return False
    except Exception as e:
        print("Error:", e)
        return False

"""
