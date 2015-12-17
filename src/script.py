# -*- coding: utf-8 -*-
import sys
import os
import subprocess

from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background

import script_refresh

__author__ = 'zhouqi'

WF = Workflow(update_settings={
    'github_slug': 'bitwolaiye/alfred-script',
    'version': open(os.path.join(os.path.dirname(__file__), 'version')).read(),
})

def get_icon(name):
    name = '%s-dark' % name if is_dark() else name
    return "icons/%s.png" % name


def is_dark():
    rgb = [int(x) for x in WF.alfred_env['theme_background'][5:-6].split(',')]
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2] ) / 255 < 0.5


def get_all_packages(query):
    formulas = WF.cached_data(
        'scripts', script_refresh.get_all_scripts, max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1],
                         formulas, match_on=MATCH_SUBSTRING)
    return formulas

def get_shell(query):
    # scripts = WF.cached_data(
    #     'scripts', script_refresh.get_all_scripts, max_age=0)
    scripts = script_refresh.get_all_scripts()
    scripts = [e[:-3] for e in scripts]
    query_filter = query.split()
    start = '_'.join(query_filter[:-1])
    scripts = [e for e in scripts if e.startswith(start)]
    # return scripts
    if query:
        scripts = WF.filter(query_filter[-1], scripts, match_on=MATCH_SUBSTRING)
    return [e for e in scripts]

def search_key_for_action(action):
    elements = []
    elements.append(action['name'])
    elements.append(action['description'])
    return u' '.join(elements)

if __name__ == '__main__':
    query = WF.args[0] if len(WF.args) else None

    for shell in get_shell(query):
        WF.add_item(
            shell,
            arg=shell,
            valid=True
            # icon=get_icon("info")
        )

    WF.send_feedback()

    # refresh cache
    # cmd = ['/usr/bin/python', WF.workflowfile('script_refresh.py')]
    # run_in_background('script_refresh', cmd)