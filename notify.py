import requests
import json
from util import APP
import time
import hmac
import base64
import hashlib
import urllib.parse


MAIL_SUBJECT = "[GITHOOK] {pusher}推送项目{rep_name}{result}"
MAIL_BODY = """<h3>{pusher}推送项目<a href="{url}">{rep_name}</a>，钩子运行{result}</h3>
<h4>COMMITS：</h4>
<ul>{comment_li}</ul>
<h4>COMMANDS：</h4>
<ul>{command_li}</ul>
<h4>STDOUT：</h4>
<ul>{stdout_li}</ul>
<h4>STDERR：</h4>
<ul>{stderr_li}</ul>
"""

def notify_by_email(data):
    mail_data = data.copy()
    #APP.debug(f'邮件 数据===> {subject} ; {body}')
    subject = MAIL_SUBJECT.format(**data)

    mail_data['comment_li'] = ''.join((f'<li>{c}</li>' for c in data['comments']))
    mail_data['command_li'] = ''.join((f'<li>{c}</li>' for c in data['commands']))
    mail_data['stdout_li'] = ''.join((f'<li>{c}</li>' for c in data['stdout_list']))
    mail_data['stderr_li'] = ''.join((f'<li>{c}</li>' for c in data['stderr_list']))
    
    body = MAIL_BODY.format(**mail_data)
    res = APP.send_email(subject, html_body=body)
    if res:
        APP.error(f'邮件推送失败：{res}')
    else:
        APP.debug(f'邮件发送成功，数据===> {subject}')


def create_sign_for_dingtalk(secret: str):
    """
    docstring
    """
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


DINGTALK_API_URL="https://oapi.dingtalk.com/robot/send?access_token={}"
DINGTAIL_HEADERS = {'Content-Type': 'application/json'}

def do_notify_by_ding_talk(config, data):
    """发消息给钉钉机器人
    """
    token = config['token']
    secret = config['secret']
    
    assert token and secret

    url = DINGTALK_API_URL.format(token)
    timestamp, sign = create_sign_for_dingtalk(secret)
    url += f'&timestamp={timestamp}&sign={sign}'
    
    #APP.debug(f'钉钉机器人 数据===> {data}')
    return requests.post(url=url, headers = DINGTAIL_HEADERS, data=json.dumps(data))


DINGTAIL_SUBJECT = "[GITHOOK] {pusher}推送项目{rep_name}{result}"
DINGTAIL_BODY = """## {pusher}推送项目[{rep_name}]({url}){result}\n
### <font color=red>COMMITS：</font>\n
{comment_li}\n
### <font color=red>COMMANDS：</font>\n
{command_li}\n
### <font color=red>STDOUT：</font>\n
{stdout_li}\n
### <font color=red>STDERR：</font>\n
{stderr_li}
"""


def notify_by_ding_talk(config, data):
    """发消息给钉钉机器人
    """
    dt_data = data.copy()
    dt_data['comment_li'] = '\n'.join((f'- {c}' for c in data['comments']))
    dt_data['command_li'] = '\n'.join((f'- {c}' for c in data['commands']))
    dt_data['stdout_li'] = '\n'.join((f'- {c}' for c in data['stdout_list']))
    dt_data['stderr_li'] = '\n'.join((f'- {c}' for c in data['stderr_list']))

    dt_msg = {
        "msgtype": 'markdown',
        "markdown": {
            'title': DINGTAIL_SUBJECT.format(**dt_data),
            'text': DINGTAIL_BODY.format(**dt_data)
        }
    }
    res = do_notify_by_ding_talk(config, dt_msg)
    APP.debug(f'钉钉推送结果：{res.json()}')


def notify_by_server_chan(config, data):
    prefix = 'error_' if 'error' in data else ''
    url = 'https://sc.ftqq.com/{sckey}.send'.format(**config)
    title = config[prefix + 'title'].format(**data)
    message = config[prefix + 'message'].format(**data)
    APP.debug(f'Server酱 数据===> {title} ; {message}')
    res = requests.get(url, params={'text': title, 'desp': message})
    APP.debug(f'Server酱推送结果：{res.json()}')


def notify(data):
    if APP['notify.mail'] == 1:
        notify_by_email(data)
    if APP['notify.dingtalk'] == 1:
        notify_by_ding_talk(APP['dingtalk'], data)
