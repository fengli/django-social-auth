Django Social Auth
==================

从django social Auth fork 过来。主要的更改有：

    * 增加了豆瓣登录
    * 增加了新浪微博登录
    * 增加了一个pipeline实例，可以让用户通过douban/weibo等
    注册新的帐户，并且会返回一个表单，让用户填写用户名，电子邮箱，密码信息
    从而完成注册。 (/example) 如果用户之前关联了这个帐号，则直接使用户登录。

安装
----

你需要先安装 OpenId 和 oauth

    pip install python-openid
    pip install python-oauth2

然后 clone from github

    $ git clone git://github.com/fengli/django-social-auth.git
    $ cd django-social-auth
    $ sudo python setup.py install


有没有一个完整的例子
-------------

你可以在example里边找到一个完整的例子，主要的功能可以让用户通过weibo/douban
进行注册和登录：

   * 如果用户没有注册过，用户可以点击通过weibo/douban注册
   * 注册过程中会返回用户一个表单，填写username,password,email即可完成注册
   * 如果用户之前已经关联了weibo/douban等，会直接使用户登录
   * 用户注册完成或登录之后，仍然可以关联其他帐号

如何测试这个实例
-------------
    
    你需要申请douban api/key, weibo api/key pair,然后在local_settings.py
    中填写。

    cd example
    python manage.py syncde
    python manage.py runserver
    
    http://127.0.0.1:8000

更详细的教程
--------------
https://github.com/omab/django-social-auth/blob/master/README.rst
