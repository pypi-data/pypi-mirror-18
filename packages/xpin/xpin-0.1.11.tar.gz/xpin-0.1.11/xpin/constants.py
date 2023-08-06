# -*- coding: utf-8 -*-

NAME = 'xpin'

# URL 定义

# 生成并发送PIN码
URL_PIN_CREATE = '/pin/create'

# 验证PIN码
URL_PIN_VERIFY = '/pin/verify'


# 返回码定义

# 内部错误
RET_INTERNAL = -1000

# 参数错误
RET_PARAMS_INVALID = 500

# 签名错误
RET_SIGN_INVALID = 600

# 用户无效
RET_USER_INVALID = 1000

# PIN无效
RET_PIN_VALID = 2000

# PIN过期
RET_PIN_EXPIRED = 3000


# 默认app配置
CONFIG = dict(
    # flask-sqlalchemy
    SQLALCHEMY_ECHO=False,

    # admin_user
    SESSION_KEY_ADMIN_USERNAME='admin_username',

    # PIN码长度
    PIN_LENGTH=6,

    # PIN码有效期(秒)，None代表无限
    PIN_MAX_AGE=None,

    MSG_TITLE='pin code',
    MSG_CONTENT_TPL='{username}@{host} is applying for pin. pin is {pin}'
)

