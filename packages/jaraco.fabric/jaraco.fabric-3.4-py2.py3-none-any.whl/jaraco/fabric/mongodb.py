import re

import pkg_resources

from fabric.api import sudo, task
from fabric.contrib import files
from fabric.context_managers import settings

from . import apt


__all__ = 'distro_install', 'find_current_version', 'install_systemd'


APT_KEYS = [
    'EA312927',
]


@task
def distro_install(version="3.2"):
    """
    Install mongodb as an apt package (which also configures it as a
    service).

    TODO: Currently, the service doesn't start on Ubuntu 15.04 or later.
    See https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04
    for more details on how to configure it as a service.
    """

    if version.startswith('2.'):
        return distro_install_2(version)

    elif version.startswith('3.'):
        return distro_install_3(version)

    raise RuntimeError('Unknown version {}'.format(version))


def distro_install_2(version):
    """
    Install MongoDB version 2.x
    """
    assert version.startswith('2.')

    # MongoDB 2
    content = (
        'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart '
        'dist 10gen',
    )
    org_list = '/etc/apt/sources.list.d/mongodb.list'
    files.append(org_list, content, use_sudo=True)


@task
def find_current_version():
    output = sudo('apt list -qq mongodb-org')
    return re.search(r'\d+\.\d+\.\d+', output).group(0)


def distro_install_3(version):
    """
    Install MongoDB version 3.x
    """
    assert version.startswith('3.')

    lsb_release = apt.lsb_release()
    repo_url = "http://repo.mongodb.org/apt/ubuntu"
    tmpl = "deb {repo_url} {lsb_release}/mongodb-org/{version} multiverse"
    content = tmpl.format(**locals())
    org_list = '/etc/apt/sources.list.d/mongodb-org-{version}.list'.format(**locals())
    files.append(org_list, content, use_sudo=True)

    with settings(warn_only=True):
        for key in APT_KEYS:
            sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv {}'.format(key))

    sudo('apt update')
    version = find_current_version()
    apt.install_packages('mongodb-org={version}'.format(**locals()))
    install_systemd()


@task
def install_systemd():
    """
    On newer versions of Ubuntu, make sure that systemd is configured
    to manage the service.
    https://docs.mongodb.com/v3.2/tutorial/install-mongodb-on-ubuntu/#ubuntu-16-04-only-create-systemd-service-file
    """
    if apt.lsb_version() < '15.04':
        return

    fn = 'mongod.service'
    service_strm = pkg_resources.resource_stream(__name__, fn)
    files.put(service_strm, '/lib/systemd/system/' + fn, use_sudo=True)
    # TODO: does the service start automatically? If not,
    # sudo('systemctl start mongod')
