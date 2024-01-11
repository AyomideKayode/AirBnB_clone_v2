#!/usr/bin/python3

from fabric.api import run, put, env
import os

env.hosts = ['100.26.11.61', '100.25.151.196']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/id_rsa']


def do_deploy(archive_path):
    """Distributes an archive to web servers and deploys it."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on web servers
        put(archive_path, '/tmp/')

        # Extract archive to 
        # /data/web_static/releases/<archive filename without extension>/
        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/{}'.format(
            filename.split('.')[0])
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Move files from web_static folder to its parent folder
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))

        # Remove unnecessary web_static folder
        run('rm -rf {}/web_static'.format(folder_name))

        # Delete the archive from web server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('ln -s {} /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
