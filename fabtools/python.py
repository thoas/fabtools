"""
Fabric tools for managing Python packages using pip
"""
from fabric.api import *


def is_installed(package, virtualenv=None):
    """
    Check if a Python package is installed
    """
    options = []
    if virtualenv:
        options.append('-E "%s"' % virtualenv)
    options = " ".join(options)
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("pip freeze %(options)s" % locals())
    packages = [line.split('==')[0] for line in res.splitlines()]
    return (package in packages)


def install(packages, installer=None, upgrade=False, use_sudo=False):
    """
    Install Python packages
    """
    func = use_sudo and sudo or run
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = []
    if upgrade:
        options.append("-U")
    options = " ".join(options)
    func('PIP_USE_MIRRORS=true pip install %(options)s %(packages)s' % locals())
