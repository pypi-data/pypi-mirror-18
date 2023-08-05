===========================
djdg PYTHON COMMON AUTH SDK
===========================

.. toctree::
   :maxdepth: 2


How To Install:
---------------
command ::

    pip install djdg_python_common_verify_SDK

database model description:
---------------------------

    1. VerifiedUser_model_
    2. BankInfo_model_
    3. BankVerify_model_


.. _VerifiedUser_model:

VerifiedUser model
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class VerifiedUser(models.Model):
        TYPE_REAL_NAME_VALIDATE = 0
        TYPE_UPLOAD_VALIDATE = 1
        CHOICE_TYPE = (
            (TYPE_REAL_NAME_VALIDATE, '实名认证'),
            (TYPE_UPLOAD_VALIDATE, '上传认证')
        )
        STATUS_AUDIT_PASS = 0
        STATUS_AUDIT = 1
        STATUS_NOT_USE = 2
        STATUS_RE_AUDIT = 4
        CHOICE_STATUS = (
            (STATUS_AUDIT_PASS, '认证成功'),
            (STATUS_AUDIT, '待审核'),
            (STATUS_NOT_USE, '未使用'),
            (STATUS_RE_AUDIT, '认证失败')
        )
        user = models.OneToOneField(User, related_name="common_verified_user")
        id_name = models.CharField(u"身份证姓名", max_length=64, null=True)
        id_card_no = models.CharField(u"身份证号码", max_length=32, null=True)
        type = models.SmallIntegerField(u"认证类型", default=0, choices=CHOICE_TYPE)
        id_card_img1 = models.CharField(u"身份证正面", max_length=128, null=True)
        id_card_img2 = models.CharField(u"身份证反而", max_length=128, null=True)
        status = models.SmallIntegerField(u"认证状态", default=0, choices=CHOICE_STATUS)
        stime = models.DateTimeField(u"状态时间", auto_now=True)
        ctime = models.DateTimeField(u"创建时间", auto_now_add=True)
        pay_password = models.CharField(u"支付密码", max_length=128, null=True, blank=True)


.. _BankInfo_model:

BankInfo model
^^^^^^^^^^^^^^

.. code-block:: python

    class BankInfo(models.Model):
        name = models.CharField(u"银行名称", max_length=32)
        logo = models.CharField(u"银行LOGO URL", max_length=255)
        color = models.CharField(u"银行卡底色", max_length=8, default='FFFFFF')


.. _BankVerify_model:

BankVerify model
^^^^^^^^^^^^^^^^

.. code-block:: python

    class BankVerify(models.Model):
            TYPE_BANK_BOOK = 0
            TYPE_DEBIT_CARD = 1
            TYPE_CREDIT_CARD = 2
            CHOICE_TYPE = (
                (TYPE_BANK_BOOK, '存折'),
                (TYPE_DEBIT_CARD, '借记卡'),
                (TYPE_CREDIT_CARD, '信用卡')
            )
            STATUS_AUDIT_PASS = 0
            STATUS_AUDIT = 1
            STATUS_NOT_USE = 2
            STATUS_RE_AUDIT = 4
            CHOICE_STATUS = (
                (STATUS_AUDIT_PASS, '绑定成功'),
                (STATUS_AUDIT, '绑定中'),
                (STATUS_NOT_USE, "未使用"),
                (STATUS_RE_AUDIT, '绑定失败')
            )
            user = models.ForeignKey(User)
            bank_info = models.ForeignKey(BankInfo, related_name="dealer_bank_card", null=True, default=None,
                                          on_delete=models.SET_NULL)
            card_branch = models.TextField("开户支行", max_length=64, null=True)
            province = models.CharField("省份", max_length=32, default='')
            city = models.CharField("城市", max_length=16, default='')
            card_no = models.CharField("卡号", max_length=64)
            card_tel = models.CharField("预留手机", max_length=16)
            type = models.SmallIntegerField("卡类型", default=1, choices=CHOICE_TYPE)
            status = models.SmallIntegerField("卡状态", default=0, choices=CHOICE_STATUS)
            stime = models.DateTimeField("状态时间", auto_now=True)
            ctime = models.DateTimeField("创建时间", auto_now_add=True)


Setting Config:
    - INSTALLED_APPS_.
    - JAVA_COMMON_SYSTEM_.
    - RESPONSE_CONFIG_.
    - REDIS_.
    - LOGGING_.
    - DATABASE_.

.. _INSTALLED_APPS:

INSTALLED_APPS

.. code-block:: python

    INSTALLED_APPS = [
        "**",
        "djdg_common_verify"
    ]
    # INSTALLED_APPS 增加如上app
    # 然后运行python manage.py migrate djdg_common_verify
    # 生成数据库的表，以及插入bankinfo的信息

.. _JAVA_COMMON_SYSTEM:

JAVA_COMMON_SYSTEM

.. code-block:: python

    JAVA_COMMON_SYSTEM = {
    'host': 'localhost', 'protocol': 'http',
    'base_url': '/ja/common/v1/',
    'appid': 'abc', 'secret': '123'}
    # 需要在settings.py增加java common模块的配置，具体的配置信息如上

.. _RESPONSE_CONFIG:

RESPONSE_CONFIG

.. code-block:: python

    RESPONSE_CONFIG = {
        'STATUS_PARAM': 'statusCode',
        'MSG_PARAM': 'msg',
        'DATA_PARAM': 'data',
        'OK_STATUS': 0,
        'OK_MSG': 'success'
    }
    # 配置RESPONSE_CONFIG， 主要用于系统间的http请求

.. _REDIS:

REDIS

.. code-block:: python

    REDIS = {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '123',
    }
    # 配置redis

.. _LOGGING:

LOGGING

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s [%(levelname)s] [%(process)d:%(thread)d] [%(name)s] [%(module)s.%(funcName)s:%(lineno)d] - %(message)s'
            },
            'middle': {
                'format': '%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] - %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
                },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'middle'
            },
            'testlog': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(BASE_DIR, 'test.log'),
                'maxBytes': '1024 * 1024 * 10',
                'backupCount': '5'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['testlog'],
                'propagate': True,
                'level': 'INFO',
                },
            'djdg_common_verify': {
                'handlers': ['testlog'],
                'propagate': False,
                'level': 'DEBUG',
                },
        }
    }
    # 如果需要将认证的信息保存到log里面，需要在loggers里面设置djdg_common_verify，具体配置可参考上述代码


.. _DATABASE:

DATABASE migrate

.. code-block:: python

   python manage.py migrate djdg_common_verify

Run Test:

Test Command

.. code-block:: python

    # first config setting file.
    # 在DATABASE里面加入类似的如下代码
    # 由于有中文，必须设置编码
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'verifycommon',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'TEST': {
                'NAME': 'mytestdatabase',
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
                },
        },
    }
    # 然后运行下面的代码，执行测试用例,
    # 不要频繁去跑测试用例，由于java的接口直接对接第三方的付费服务， 只要保证功能正常即可
    python manage.py test djdg_common_verify


Function list:
    - idcardauth_example_.
    - bankcardauth_example_.
    - paypasswordauth_example_.


.. _idcardauth_example:

IdCardUserAuther Example:


1. 用户获取实名认证信息

导入工具类 ::

   from djdg_common_verify.idcard_auth import IdCardUserAuther

创建实例对象 ::

    Auther = IdCardUserAuther(user_id=1)

2. 获取序列化之后的信息 ::

    Auther.serializer()

2.1 返回信息为dict

2.1.1 未通过认证::

    {"statusCode": 5000, "msg": "用户暂未通过认证", "data":{}}

2.1.2 通过认证::

    {"statusCode": 0, "msg": "成功", "data":{"name":"张三", "identity":1234}}

3. 传参进行认证 ::

    Auther = IdCardUserAuther(user_id=1, auth_data={"name":"张三", "identity":"123456789"})

3.1 调用认证方法 ::

    Auther.auth()

3.2 获取序列化之后的信息 ::

    Auther.serializer()

3.3 返回信息为dict

3.3.1 未通过认证 ::

    {"statusCode": 5000, "msg": "用户暂未通过认证", "data":{}}

3.3.2 通过认证 ::

    {"statusCode": 0, "msg": "成功", "data":{"name":"张三", "identity":1234}}



.. _bankcardauth_example:

bankcardauth Example:

导入工具类 ::

   from djdg_common_verify.bankcard_auth import BankCardUserAuther

用户获取银行卡绑定信息 ::

    Auther = BankCardUserAuther(user_id=1)

获取序列化之后的信息  ::

    Auther.serializer()

返回信息为dict ::

    # 未通过认证
    {"statusCode": 5000, "msg": "银行卡暂未通过认证", "data": {}}
    # 通过认证
    {"statusCode": 0, "msg": "成功",
        "data": {
        "bankcard": "", "bank_branch_name": "",
        "type": "",  "province": "",
        "city": "", "tel": "",
        "bank_name": "", "bank_logo": "",
        "color": "", "name": "", "identity": ""
     }
    }

传参进行认证 ::

    Auther = BankCardUserAuther(user_id=1, auth_data={
        "bankcard": "", "bank_branch_name": "",
        "type": "", "province": "", "city": "",
        "tel": "", "bank_name": "", "bank_logo": "",
        "color": "", "name": "", "identity": ""
     }

绑定或修改银行卡 ::


    auth_data={
        "name": "张三", "bankcard": "1234567890", "tel":"13112345678"
     }
    # "name":姓名， "bankcard":银行卡号， "tel":电话号码 三个字段不能为空


修改银行卡支行信息 ::

    auth_data={
    "province": "广东", "city":"深圳", "bank_branch_name": "科技园支行"
     }
    # "province":省份， "city":城市， "bank_branch_name":支行名称 三个字段不能为空


调用认证方法 ::

    Auther.auth()

获取序列化之后的信息 ::

    Auther.serializer()

返回信息为dict ::

    # 未通过认证
    {"statusCode": 5000, "msg": "用户暂未通过认证", "data":{}}

    # 通过认证
    {"statusCode": 0, "msg": "成功",
        "data": {
        "bankcard": "", "bank_branch_name": "",
        "type": "", "province": "", "city": "",
        "tel": "", "bank_name": "", "bank_logo": "",
        "color": "", "name": "", "identity": ""
     }
    }


.. _paypasswordauth_example:

paypasswordauth Example:

导入工具类 ::

   from djdg_common_verify.bankcard_auth import BankCardUserAuther

用户获取银行卡绑定信息 ::

    Auther = UserPasswordAuther(user_id=1)

获取序列化之后的信息 ::

    Auther.serializer()

返回信息为dict ::

    {"statusCode": 0, "msg": "成功", "data": {"password": "设置的密码"}}

    # 已经设置密码

    {"statusCode": 5000, "msg": "用户暂未设置交易密码", "data": {}}

    # 未设置密码

传参进行认证

设置交易密码 (之前尚未设置交易密码) ::

    Auther = UserPasswordAuther(user_id=1)
    # 调用认证方法
    Auther.auth()
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    {"statusCode": 5006, "msg": "密码无效或者为空", "data": {}}  # 未通过认证
    {"statusCode": 0, "msg": "成功", "data": {"password": "设置的密码"}} # 通过认证


修改交易密码 (之前已经设置交易密码) ::

    # 第一步获取settingtoken
    Auther = UserPasswordAuther(user_id=1, auth_data={"identity":"身份证号码"})
    # 调用获取settingtoken方法
    Auther.get_settingtoken()
    # 返回信息为dict
    {"statusCode": 5003, "msg": "用户身份证信息未通过校验", "data": {}}
    {"statusCode": 5000, "msg": "用户暂未设置交易密码", "data": {}}
    {"statusCode": 0,
                "msg": "验证身份信息成功",
                "data": {
                    "settingToken": settingtoken.token
                }}  # 获取成功返回信息
    # 第一步获取settingtoken
    Auther = UserPasswordAuther(user_id=1, \
    auth_data={"password":"设置的交易密码", "setttingtoken":"通过第一步获取的settingtoken"})
    # 调用认证方法
    Auther.auth()
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    {"statusCode": 5001, "msg": "setting token未通过校验", "data": {}} # 未通过认证
    {"statusCode": 5005, "msg": "settingtoken失效", "data": {}} # 未通过认证
    {"statusCode": 0, "msg": "成功", "data": {"password": "设置的密码"}} # 通过认证
