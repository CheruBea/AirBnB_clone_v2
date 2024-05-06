#!/usr/bin/python3
'''
Fabric script that distributes an archive to web servers
using deploy
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['54.197.93.99', '34.202.158.84']


@runs_once
def do_pack():
    """Static files archives"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    time = datetime.now()
    res = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        time.year,
        time.month,
        time.day,
        time.hour,
        time.minute,
        time.second
    )
    try:
        print("Packing web_static to {}".format(res))
        local("tar -cvzf {} web_static".format(res))
        archize_size = os.stat(res).st_size
        print("web_static packed: {} -> {} Bytes".format(res, archize_size))
    except Exception:
        res = None
    return res


def do_deploy(archive_path):
    """Deploys the static files to the host servers

    Args:
        archive_path (str): The path of the archive to distribute
    """

    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
    Full deployment of that static files to the servers
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
