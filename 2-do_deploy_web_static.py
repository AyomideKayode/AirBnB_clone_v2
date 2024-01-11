#!/usr/bin/python3

from fabric.api import run, put, env
from os import path
# from datetime import datetime

# Set the remote hosts, user, and key file for Fabric
env.hosts = ['100.26.11.61', '100.25.151.196']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/id_rsa']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.

    :param archive_path: Path to the local archive to be deployed
    :return: True if deployment is successful, False otherwise
    """

    try:
        # Check if the local archive exists
        if not path.exists(archive_path):
            return False

        # Upload the archive to /tmp/ directory on web servers
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive filename without extension>/
        filename = path.basename(archive_path)
        folder_name = '/data/web_static/releases/{}'.format(
            filename.split('.')[0])
        run('sudo mkdir -p {}'.format(folder_name))
        run('sudo tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Move files from web_static folder to its parent folder
        run('sudo mv {}/web_static/* {}'.format(folder_name, folder_name))

        # Remove unnecessary web_static folder
        run('sudo rm -rf {}/web_static'.format(folder_name))

        # Delete the archive from web server
        run('sudo rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('sudo ln -s {} /data/web_static/current'.format(folder_name))

        print("New version deployed!")

    except Exception as e:
        return False

    # return True on success
    return True
