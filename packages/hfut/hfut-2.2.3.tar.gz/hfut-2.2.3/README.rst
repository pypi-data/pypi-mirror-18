===========================================
hfut - 合肥工业大学学生教务接口
===========================================

开发状态
--------------------

.. image:: https://img.shields.io/github/license/er1iang/hfut.svg
    :target: https://github.com/er1iang/hfut/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/hfut.svg
    :target: https://pypi.python.org/pypi/hfut

.. image:: https://img.shields.io/travis/er1iang/hfut.svg
    :target: https://travis-ci.org/er1iang/hfut

hfut 提供了合肥工业大学教务系统学生端接口并提供了方便开发者开发围绕学生数据的一些工具.


QQ 群
----------------

你可以点这 `加入QQ群 <http://shang.qq.com/wpa/qunwpa?idkey=649d2da17d209065a5e662eb951f5b8ab971b7ed0daec0fe17e4db7b660b902d>`_ 或者扫描二维码加入我们.

.. image:: docs/_static/qq_group_qr.png


功能特性
--------------------

- 同时支持合肥校区和宣城校区的教务系统, 对应接口的使用方式完全相同
- 支持会话自动更新, 无需担心超过时间后访问接口会出错
- 支持非法参数检查, 你再也不用担心一不小心就被封了 IP 了
- 支持全局配置 HTML 解析器, 同时照顾了不会处理依赖编译的新手和对性能有要求的场景
- 使用简单, 只需声明一个  ``hfut.Student``  对象即可调用所有接口
- 接口丰富, 提供了所有学生能够使用的教务接口, 除此外还有正常情况下学生无法访问到的接口
- 可以灵活控制课表数据, 再也不需要各类上传个人隐私, 功能臃肿的课表软件了
- 数据能够轻松导出, 能够为基于工大教务数据的服务或应用提供强大的底层支持
- 提供了强大的选课功能, 你能轻松查询可选的课程, 查看教学班级选中人数, 批量提交增删课程数据
- 对开发友好, 每个接口返回的数据结构都提供了描述, 同时提供了用于继承的基类以及页面处理的函数和其他工具提升你的开发效率
- Python2/3 兼容, 代码在 2.7,3.3,3.4,3.5, pypy 五个版本上进行了测试


它能做什么？
---------------

- 学生微信后台服务支持
- 选课助手
- 学生数据分析
- OAuth 登陆服务
- 以及一切你能想到的与学生信息与教务数据有关的项目


快速上手
============

你只需要在命令行下输入一下代码便能安装好 hfut::

    $ pip install hfut

如果你没有安装 `pip <https://pip.pypa.io>`_ ，
`Python 安装包指南 <http://docs.python-guide.org/en/latest/starting/installation/>`_
能够指导你安装 PIP .

调用接口
----------

    >>> from hfut import Student
    >>> stu = Student('your-account', 'your-password', 'campus')
    >>> stu.get_my_info()

所有的接口在这: :ref:`所有接口 <api>`.

:ref:`高级技巧 <advanced>` 这一节有更多的例子.

文档
-----

完整文档位于 http://hfut.rtfd.io/ , 你只要花一点时间就能了解整个项目.


**更新日志请查看:** `HISTORY.rst <https://github.com/er1iang/hfut/blob/master/HISTORY.rst>`_
