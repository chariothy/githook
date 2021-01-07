import requests
import json
from util import APP


MAIL_SUBJECT = "[GITHOOK] {pusher}推送到项目{rep_name}，钩子结果：{result}"
MAIL_BODY = """<h3>{pusher}推送到项目{rep_name}，钩子运行结果：{result}</h3>
<p><a href="{url}">{url}</a></p>
<h4>COMMITS：</h4>
<ul>{comment_li}</ul>
<h4>COMMANDS：</h4>
<ul>{command_li}</ul>
<h4>STDOUT：</h4>
<ul>{stdout_li}</ul>
<h4>STDERR：</h4>
<ul>{stderr_li}</ul>
"""

DINGTAIL_BODY = """
<p>
"""


def notifyByEmail(data):
    #APP.debug(f'邮件 数据===> {subject} ; {body}')
    subject = MAIL_SUBJECT.format(**data)

    comment_li = ''.join((f'<li>{c}</li>' for c in data['comments']))
    command_li = ''.join((f'<li>{c}</li>' for c in data['commands']))
    stdout_li = ''.join((f'<li>{c}</li>' for c in data['stdout_list']))
    stderr_li = ''.join((f'<li>{c}</li>' for c in data['stderr_list']))
    data['comment_li'] = comment_li
    data['command_li'] = command_li
    data['stdout_li'] = stdout_li
    data['stderr_li'] = stderr_li
    
    body = MAIL_BODY.format(**data)
    print(subject, body)
    res = APP.send_email(subject, html_body=body)
    if res:
        APP.error(f'邮件推送失败：{res}')
    else:
        APP.debug(f'邮件发送成功，数据===> {subject}')


def notifyByDingTail(config, data):
    """发消息给钉钉机器人
    """
    token = config['token']
    if not token:
        APP.error('没有钉钉token')
        #p('APP.error: 没有钉钉token')
        return
    prefix = 'error_' if 'error' in data else ''
    data = {
        "msgtype": "text",
        "text": {
            "content": config['keyword'] + config[prefix + 'message'].format(**data)
        },
        "at": config['at']
    }
    APP.debug(f'钉钉机器人 数据===> {data}')
    #p('钉钉机器人===>', data)
    res = requests.post(url="https://oapi.dingtalk.com/robot/send?access_token={}".format(token), \
        headers = {'Content-Type': 'application/json'}, data=json.dumps(data))
    #p('钉钉推送结果：', res.json())
    APP.debug(f'钉钉推送结果：{res.json()}')


def notifyByServerChan(config, data):
    prefix = 'error_' if 'error' in data else ''
    url = 'https://sc.ftqq.com/{sckey}.send'.format(**config)
    title = config[prefix + 'title'].format(**data)
    message = config[prefix + 'message'].format(**data)
    APP.debug(f'Server酱 数据===> {title} ; {message}')
    #p('Server酱===>', title, '; ', message)
    if not CONFIG['dry']:
        res = requests.get(url, params={'text': title, 'desp': message})
        #p('Server酱推送结果：', res.json())
        APP.debug(f'Server酱推送结果：{res.json()}')


def notify(data):
    notifyConfig = APP['notify']
    if 'mail' in notifyConfig:
        notifyByEmail(data)
    if 'dingtalk' in notifyConfig:
        notifyByDingTail(APP['dingtalk'], data)
