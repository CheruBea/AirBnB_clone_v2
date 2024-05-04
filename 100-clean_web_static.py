#!/usr/bin/python3
'''
Fabric script that distributes an archive to web servers
using deploy
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['107.23.91.47', '35.174.211.188']


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


def do_clean(number=0):
    """Deletes archive files that are out of date"""
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))
