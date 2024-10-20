from typing import Optional
from fastapi import FastAPI, Request

import json, os, subprocess, re
from os import path
from util import APP
from notify import notify

ENV = os.environ.get('ENV', 'dev')
app = FastAPI()
REG_MAIN_BRANCH = re.compile(r'\* (\w+)')

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
        result = subprocess.run(f'cd {project_dir} && git branch', shell=True, capture_output=True)
        output = result.stdout.decode('UTF-8')
        main_branch = ''
        for branch in output.split('\n'):
            if 0 == branch.find('*'):
                main_branch = REG_MAIN_BRANCH.match(branch).groups()[0]
                break
        commands.append(f'cd {project_dir}')
        commands.append('git reset --hard HEAD')
        commands.append('git clean -f')
        commands.append(f'git pull --ff-only origin {main_branch}')
        commands.append(f'git checkout {main_branch}')
    return commands


def do_notify(payload, commands, result):
    """
    docstring
    """
    rep = payload['repository']
    pusher = payload.get('pusher')
    if not pusher:
        return 
    commits = payload['commits']
    project_full_name = rep['full_name']
    commit_comments = (x['message'] for x in commits)
    pushed_by = pusher['name']
    compare_url = payload['compare']
    
    comment_li = '\n'.join((f'- {c}' for c in commit_comments))
    command_li = '\n'.join((f'- {c}' for c in commands))
    stdout_li = '\n'.join((f'- {c}' for c in result.stdout.decode('UTF-8').strip('\n').split('\n')))
    stderr_li = '\n'.join((f'- {c}' for c in result.stderr.decode('UTF-8').strip('\n').split('\n')))
    success = '成功' if result.returncode == 0 else '失败'
    
    title = f"[GITHOOK] {pushed_by}推送项目{project_full_name}{success}"
    text = f"""## {pushed_by}推送项目[{project_full_name}]({compare_url}){success}\n
### <font color=#000080>COMMITS：</font>\n
{comment_li}\n
### <font color=#6A65FF>COMMANDS：</font>\n
{command_li}\n
### <font color=#4169e1>STDOUT：</font>\n
{stdout_li}\n
### <font color=#ff0000>STDERR：</font>\n
{stderr_li}
"""
    APP.ding(title, text)


@app.post('/push')
async def git_push(req: Request):
    body = await req.body()
    payload = json.loads(body)

    if 'repository' not in payload or 'pusher' not in payload:
        return {
            'result': 'error', 
            'message': 'Not push event'
        }

    commands = make_commands(payload)
    result = subprocess.run(' && '.join(commands), shell=True, capture_output=True)
    print('=' * 80)
    print(result.args)
    print('=' * 80)
    print(result.stderr.decode('UTF-8'))
    print('=' * 80)
    print(result.stdout.decode('UTF-8'))
    print('=' * 80)

    do_notify(payload, commands, result)

    return {
        'result': 'success' if result.returncode == 0 else 'error', 
        'code': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }


@app.get('/push')
async def test_push(req: Request):
    print('=' * 80, 'test push', '=' * 80)

    return {
        'result': 'success'
    }

#TODO: 1. notify dingtalk 2. show commit files

if __name__ == "__main__":
    import uvicorn, os
    print(f'Listening ++++++ ENV={ENV} ++++++')
    uvicorn.run("main:app", host="0.0.0.0", port=APP['port'], reload=(ENV != 'prod'))