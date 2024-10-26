from os import environ as env
CONFIG = {
    'log': {
        'level': env.get('LOG_LEVEL', 'DEBUG'),
        'dest': {
            'stdout': True, # None: disabled,
            'file': '',   # None: disabled, 
                                        # PATH: log file path, 
                                        # '': Default path under ./logs/
            'syslog': None,    # None: disabled, or (ip, port)
            'mail': ''   # None: disabled,
                                                    # MAIL: send to
                                                    # '': use setting ['mail']['to']
        },
    },
    'mail': {
        'from': env.get('MAIL_FROM', 'Henry TIAN <6314849@qq.com>'),
        'to': 'Henry TIAN <6314849@qq.com>'
    },
    'smtp': {
        'host': env.get('SMTP_HOST', 'smtp.163.com'),
        'port': env.get('SMTP_PORT', 465),
        'user': env.get('SMTP_USER', '15050506668@163.com'),
        'pwd': env.get('SMTP_PWD', '123456'),
        'type': env.get('SMTP_TYPE', 'ssl')
    },
    'dingtalk': {                       # 通过钉钉机器人发送通知，具体请见钉钉机器人文档
        'token': env.get('DINGTALK_TOKEN', ''),
        'secret' : env.get('DINGTALK_SECRET', '') # 钉钉机器人的三种验证方式之一为密钥验证
    },
    'project_base_dir': '/www',
    'port': 8000
}