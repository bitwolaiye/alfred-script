# -*- coding: utf-8 -*-
import subprocess
from workflow import Workflow, PasswordNotFound

__author__ = 'zhouqi'


def get_all_scripts():
    user, _ = subprocess.Popen(['whoami'], stdout=subprocess.PIPE).communicate()
    user = user.split('\n')[0]
    cmd, _ = subprocess.Popen(['ls', '/Users/%s/Scripts' % user], stdout=subprocess.PIPE).communicate()
    return cmd.splitlines()

def get_all_packages():
    cmd, _ = subprocess.Popen(['/usr/local/bin/brew', 'search'], stdout=subprocess.PIPE).communicate()
    return cmd.splitlines()


def get_installed_packages():
    cmd, _ = subprocess.Popen(
        ['/usr/local/bin/brew', 'list', '--versions'], stdout=subprocess.PIPE).communicate()
    return cmd.splitlines()


def get_info():
    cmd, _ = subprocess.Popen(
        ['/usr/local/bin/brew', 'info'], stdout=subprocess.PIPE).communicate()
    return cmd

if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('scripts', get_all_scripts())
    # wf.cache_data('brew_all_formulas', get_all_packages())
    # wf.cache_data('brew_installed_formulas', get_installed_packages())
    # wf.cache_data('brew_info', get_info())
