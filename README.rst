Django Social Registration/login
==================

从 `django social Auth <https://github.com/omab/django-social-auth/>`_ fork 过来。添加了一个使用pipeline的实例，使得用户可以通过新浪微博，豆瓣，twitter等帐号注册帐号或者直接登录。

这个pipeline的逻辑：

* 如果用户没有注册过，用户可以点击通过weibo/douban注册
* 注册过程中会返回用户一个表单，填写username,password,email即可完成注册
* 如果用户之前已经关联了weibo/douban等，会直接使用户登录
* 用户注册完成或登录之后，仍然可以关联其他帐号

主要的更新有：

* 增加了豆瓣登录
* 增加了新浪微博登录
* 增加了一个pipeline实例，可以让用户通过douban/weibo等注册新的帐户，
并且会返回一个表单，让用户完善用户名，电子邮箱，密码信息
从而完成注册。 (/example) 如果用户之前关联了这个帐号，则直接使用户登录。

安装
----

你需要先安装 OpenId 和 oauth

    pip install python-openid

    pip install oauth2

然后 clone from github

    $ git clone git://github.com/fengli/django-social-auth.git
    
    $ cd django-social-auth
    
    $ sudo python setup.py install


如何测试这个实例
-------------
    
你可以在example里边找到一个完整的例子，主要的功能可以让用户通过weibo/douban
进行注册和登录。
    
你需要申请douban api/key, weibo api/key pair,然后在local_settings.py
中填写相应的信息。

    cd example
    
    python manage.py syncde
    
    python manage.py runserver
    
    http://127.0.0.1:8000

可以 `点击这儿 <http://ww3.sinaimg.cn/mw690/7380e96cgw1dupuy1r1b8j.jpg>`_ 看看网页的截图


更详细的教程
--------------
https://github.com/omab/django-social-auth/blob/master/README.rst

Bring to you by
---------------
http://ikandou.com
http://ikandou.com/book
