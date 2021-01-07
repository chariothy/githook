from typing import Optional
from fastapi import FastAPI, Request

import json, os, subprocess
from os import path
from chariothy_common import AppTool
from util import APP
from notify import notify

app = FastAPI()


def make_commands(payload):
    """
    docstring
    """
    rep = payload['repository']
    #print(rep, pusher, commits)

    project_name = rep['name']
    ssh_url = rep['ssh_url']

    project_base_dir = APP['project_base_dir']
    assert path.exists(project_base_dir)

    commands = []
    project_dir = path.join(project_base_dir, project_name)
    if not path.exists(project_dir):
        commands.append(f'cd {project_base_dir}')
        commands.append(f'git clone {ssh_url}')
    else:
        commands.append(f'cd {project_dir}')
        commands.append('git reset --hard HEAD')
        commands.append('git clean -f')
        commands.append('git pull origin master')
        commands.append('git checkout master')
    return commands


def do_notify(payload, commands, result):
    """
    docstring
    """
    rep = payload['repository']
    pusher = payload['pusher']
    commits = payload['commits']
    project_full_name = rep['full_name']
    commit_comments = (x['message'] for x in commits)
    pushed_by = pusher['name']
    compare_url = payload['compare']
    notify(dict(
        pusher = pushed_by,
        rep_name = project_full_name,
        result = 'OK' if result.returncode == 0 else 'ERROR',
        url = compare_url,
        commands = commands,
        comments = commit_comments,
        stdout_list = result.stdout.decode('UTF-8').strip('\n').split('\n'),
        stderr_list = result.stderr.decode('UTF-8').strip('\n').split('\n')
    ))


@app.post('/push')
async def git_push(req: Request):
    body = await req.body()
    payload = json.loads(body)
    commands = make_commands(payload)
    result = subprocess.run(' && '.join(commands), shell=True, capture_output=True)

    do_notify(payload, commands, result)

    return {
        'result': 'success' if result.returncode == 0 else 'error', 
        'code': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }

#TODO: 1. notify dingtalk 2. show commit files