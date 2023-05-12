CONFIG = {
    'log': {
        'level': 'DEBUG',
        'dest': {
            'stdout': True, # None: disabled,
            'file': None,   # None: disabled, 
                                        # PATH: log file path, 
                                        # '': Default path under ./logs/
            'syslog': ('10.8.0.2', 514),    # None: disabled, or (ip, port)
            'mail': 'Henry TIAN <6314849@qq.com>'   # None: disabled,
                                                    # MAIL: send to
                                                    # '': use setting ['mail']['to']
        },
    },
    'mail': {
        'from': "Henry TIAN <chariothy@gmail.com>",
        'to': "Henry TIAN <chariothy@gmail.com>"
    },
    'smtp': {
        'host': 'smtp.163.com',
        'port': 25,
        'user': 'chariothy@gmail.com',
        'pwd': '123456'
    },
    'project_base_dir': '/app',
    'notify': {                         # 通知方式，会对列表中列出的方式进去通知，列表为空则不做任何通知
        'mail': 1,                         # 通过邮件方式通知，需要配置'mail'和'smtp'
        'dingtalk': 0                      # 通过钉钉机器人[http://dwz.win/MqK]通知，需要配置'dingtalk'
    },
    'dingtalk': {                       # 通过钉钉机器人发送通知，具体请见钉钉机器人文档
        'token': 'DINGTALK_BOT_TOKEN',
        'secret' : 'DINGTALK_BOT_SECRET' # 钉钉机器人的三种验证方式之一为密钥验证
    },
    'port': 8000
}