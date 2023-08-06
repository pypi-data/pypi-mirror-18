合肥工业大学教务系统学生端接口以及方便开发者开发围绕学生数据的一些工具.

Home-page: https://github.com/er1iang/hfut
Author: erliang
Author-email: dev@erliang.me
License: MIT
Description: ===========================================
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
        - 使用简单, 只需声明一个  ``hfut.Student``  对象即可调用所有接口
        - 接口丰富, 提供了所有学生能够使用的教务接口, 除此外还有众多正常情况下学生无法访问到的接口
        - 提供了强大的选课功能, 你能轻松查询可选的课程, 查看教学班级选中人数, 批量提交增删课程数据
        - 可以灵活控制课表数据, 再也不需要各类上传个人隐私, 功能臃肿的课表软件了
        - 数据能够轻松导出, 能够为基于工大教务数据的服务或应用提供强大的底层支持
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
        
        
        ..
            **功能和改进**
        
            **接口改变**
        
            **接口变动**
        
            **问题修复**
        
            **文档**
        
            **其他杂项**
        
        .. :changelog:
        
        2.1.1 (20161121)
        ++++++++++++++++
        
        **问题修复**
        
        - 删除 ``interface.GetClassStudents.parse`` 遗留的调试信息
        
        2.1.0 (20161121)
        ++++++++++++++++
        
        **功能和改进**
        
        - 添加了 ``parser.GlobalFeaturedSoup`` , 能够通过配置 ``value.ENV['SOUP_FEATURES']`` 属性来全局配置解析器, 目前在 ``html.parser`` 与 ``lxml`` 下进行了测试
        - 添加了 ``log.report_response`` 用来生成响应报告
        - 添加了 ``shortcut.BaseShortcuts.request`` ,  用来分离接口的请求与解析
        - 有关请求的日志记录以及会话类更加友好
        
        **问题修复**
        
        - 修复 Python2 中对 Unicode 匹配不完整的问题
        
        **接口变动**
        
        - 原先使用 ``bs4.BeautifulSoup`` 解析的接口统一改为 ``parser.GlobalFeaturedSoup`` 子类
        - ``HTML_PARSER`` 重命名为 ``SOUP_FEATURES``
        - ``value`` 模块中的值全部添加到 ENV 字典中使其可变动
        - ``interface.GetClassStudents`` 不再因未匹配到班级名称或学期报错
        - ``util.rank_host_speed`` 重构为 ``util.sort_hosts`` ,  不再接受主机 ip 参数, 改为主机 地址参数,  同时不再删除错误请求地址,  而是统一将返回时间设为 INFINITY(10000000ms)
        
        **其他杂项**
        
        - 添加了使用 ``lxml`` 作为解析器的测试, 完善了其他一些测试细节
        
        2.0.0 (20161029)
        ++++++++++++++++
        
        **功能和改进**
        
        - 重构了框架的核心部分, 对原先的接口进行了解耦, 实现细节更加清晰, 现在能够控制接口请求的请求生成, 响应获取, 响应解析的过程
        - 添加了 ``parser.dict_list_2_matrix``
        - 添加了 ``util.curriculum2schedule`` 将课程表转换为上课时间表
        - 添加了将上课时间表转换为 icalendar 协议文件并导出的例子
        
        **问题修复**
        
        - 修复 ``shortcut.Student#change_course`` 旧版结果验证方法没有移除导致的问题
        - 修复 ``shortcut.Student#change_course`` 对教学班号错误的验证逻辑
        
        **接口变动**
        
        - 原来的 ``model`` 模块中的会话类拆分到 ``session`` , ``interface``, ``shortcut`` 三个模块, 具体改变可以阅读源码查看改动
        - 原先使用 ``model.GuestSession`` , ``model.StudentSession`` 快速调用接口现在改为使用 ``shortcut.Guest`` , ``shortcut.Student`` 即可, 接口调用方式与名字没有变化, 但是访问原先会话的属性需要从新类的 ``session`` 属性中获得
        - 删除了属性验证相关的函数, 包括 ``value.validate_attrs`` , ``session.BaseSession.validate_campus``, ``session.StudentSession.validate_account``, ``session.StudentSession.validate_password``
        - 原来会话类的 ``html_parser`` , ``site_encoding`` 迁移到了 ``value`` 模块并改为 ``HTML_PARSER`` , ``SITE_ENCODING``
        - 一些不合法的参数将不再隐式地返回结果而是直接触发错误, 涉及到 ``shortcut.Student#change_password``, ``interface.ChangePassword``, ``interface.SetTelephone``
        - ``shortcut.Student#change_course`` : 当选课教学班号错误, 删除错误的课程时将不再触发错误, 而是得到一个警告
        
        **其他杂项**
        
        - 更新测试用例
        - 更新文档
        
        1.4.3 (20160829)
        ++++++++++++++++
        
        **问题修复**
        
        - 修复 ``model.StudentSession#get_selectable_courses`` 由于 ``multiprocessing.dummy.Pool`` 在 Python 2.7 下不支持 with 语句导致的错误
        
        **其他杂项**
        
        - 修正了 ``model.StudentSession#change_course`` 中的文档错误
        - 改进了测试脚本, 修复由于测试脚本没有判断程序结束状态码导致有时测试失败结果没有捕捉到的问题
        
        1.4.2 (20160828)
        ++++++++++++++++
        
        **功能和改进**
        
        - 优化了 ``model.StudentSession#get_selectable_courses`` 多线程操作
        
        **问题修复**
        
        - 修复了 ``model.StudentSession#get_selectable_courses`` 由于之前版本返回值的接口变动造成的错误
        - 修复了 ``model.StudentSession#change_course`` 由于之前版本返回值的接口变动造成的错误
        
        **接口变动**
        
        - ``model.GuestSession#get_system_state`` -> ``model.GuestSession#get_system_status`` (拼写错误这么久竟然没发现= =)
        - 去除了 ``log.unstable``
        
        1.4.1 (20160812)
        ++++++++++++++++
        
        **接口变动**
        
        - 将当接口没有解析出结果时返回的 None 值改为相应的空的容器
        
        **问题修复**
        
        - 修复 ``model.GuestSession#get_class_info`` 返回结果中的 ``备注`` 字段名中包含空格的错误
        - 修复 ``model.GuestSession#get_class_students`` 班级名称正则表达式匹配不完全导致的错误
        - 修复 ``model.GuestSession#get_class_students`` 在教学班没有学生时触发错误的问题
        
        1.4.0 (20160812)
        ++++++++++++++++
        **接口变动**
        
        - 包名由 ``hfut_stu_lib`` 改为 ``hfut``
        - 删除了 ``APIResult`` , 使用 ``model.BaseSession.histories`` (默认最大长度为10的双端队列)储存历史响应
        
        **问题修复**
        
        - ``list`` 本身是线程安全的, 去除了不必要的锁
        
        1.3.3 (20160730)
        ++++++++++++++++
        
        **问题修复**
        
        - 修复 Python2 下 ``urllib.unquote`` 不接受编码参数的错误( ``model.StudentSession.login`` )
        - 修复 Python2 下 ``list`` 对象缺少 ``copy()`` 方法的错误( ``util.filter_curriculum`` )
        - 修复时多线程时释放锁的方法名拼写错误
        - 修复 ``model.StudentSession#get_selectable_courses`` 文件名重复地添加'.json'后缀
        
        **其他杂项**
        
        - 重新配置了线上持续集成环境
        
        1.3.2 (20160728)
        ++++++++++++++++
        
        **功能和改进**
        
        - 重新实现了类的属性验证方式, ``hfut.value.validate_attrs``
        - 添加了对 `model.StudentSession.account`, `hfut.model.BaseSession.campus` 的验证
        
        **接口变动**
        
        - ``exception`` 中的 `WrongPasswordPattern` 改为了 `ValidationError`
        
        **问题修复**
        
        - 更新了新的学期名称匹配规则
        
        1.3.1 (20160722)
        ++++++++++++++++
        
        **问题修复**
        
        - 修复 ``util.get_point`` 对成绩数据判断的不完整导致的错误
        - 修复 ``model.StudentSession.get_optional_courses`` 分片错误导致总是缺失一门课程的错误
        - 修复 ``model.GuestSession.get_teaching_plan`` 查询公选课时教务系统返回大量重复课程的错误
        - 修复 ``model.GuestSession.search_course`` 结果数据格式化不完整
        
        **接口变动**
        
        - ``model.GuestSession.get_teaching_plan` 查询公选课时不再需要 `zydm`` 参数
        - 删除了所有返回结果中含有的 `序号` 字段
        
        1.3.0 (20160719)
        ++++++++++++++++
        
        **功能和改进**
        
        - 添加了 ``model.StudentSession.get_unfinished_evaluation`` 接口用来查询未完成的课程评价
        - 添加了 ``model.StudentSession.evaluate_course`` 接口用来进行课程评价
        - 添加了登录时的密码格式验证
        - 密码格式不正确时将会触发新增的 ``exception.WrongPasswordPattern``
        - 调整了日志记录格式
        - ``util.rank_host_speed`` 对写操作加锁避免竞争冒险
        - ``model.StudentSession.get_selectable_courses`` 使用了多线程进行优化
        
        **接口变动**
        
        - 去掉了 ``model.StudentSession.change_password` 多余的 `oldpwd`,`new2pwd`` 参数, 合肥校区修改教务密码无意义, 因此不允许调用此接口
        - ``model.StudentSession.login_session`` 改为 ``model.StudentSession.login`` 并且不再有返回值, 同时也修复了上个版本需要主动调用的问题
        
        **问题修复**
        
        - ``model.StudentSession.__str__`` 格式化错误
        - ``model.StudentSession.change_course`` 中错误的属性引用
        - 修复由于存在未完成的课程评价导致接口调用出错的问题
        
        1.2.2 (20160625)
        ++++++++++++++++
        
        **小的改进**
        
        - ``model.StudentSession`` 初始化成功后会从 cookie 中提取出姓名
        - 登录失败时将会触发新增的 ``exception.SystemLoginFailed``, IP被封会触发 ``exception.IPBanned``
        
        **接口变动**
        
        - ``model.StudentSession`` 实例化后不会自动登录，需要主动调用 ``model.StudentSession.login_session`` 登录, 这样可以在登陆前对实例进行其他初始化，例如配置代理等
        
        1.2.1 (20160511)
        ++++++++++++++++
        
        **问题修复**
        
        - 修复了 ``model._get_curriculum`` 在没有获取到课表导致起始周和结束周在计算时出错的问题并相应添加了测试用例
        
        1.2.0 (20160510)
        ++++++++++++++++
        
        **小的改进**
        
        - 优化了 ``utils.filter_curriculum``, 当课程冲突时会给出警告
        
        **接口改变**
        
        - 接口会话初始化参数 ``is_hefei`` 变成了 ``campus`` ( ``value`` 模块中的校区代码 ``HF``, ``XC``) 并且需要显示提供
        - 删除了 ``model.AuthSession`` , ``value`` 中的用户类型常量
        - 去除了 ``model.APIResult`` 中的魔法方法, 保证了调用明确的原则
        
        **问题修复**
        
        - 纠正了错误的通用登陆逻辑
        - 修复了合肥校区登陆网址变更导致合肥校区无法登陆的问题
        
        **其他杂项**
        
        - 调整了例子 ``web_curriculum.py``
        - 相应调整了测试用例
        
        1.1.2 (20160413)
        ++++++++++++++++
        
        **小的改进**
        
        - ``model.APIResult.json`` 支持了 `json.dumps` 的参数
        - 统一 ``model.GuestSession.get_entire_curriculum`` 和 ``model.GuestSession.get_my_curriculum`` 的代码
        - ``model.GuestSession.get_entire_curriculum`` 和 ``model.GuestSession.get_my_curriculum`` 返回值添加了起止周字段
        
        **接口改变**
        
        - ``parser.parse_course`` 不再接受 None 值为参数
        
        **文档**
        
        - 补充例子
        
        **其他杂项**
        
        - 添加例子 ``web_curriculum.py``, 使用 bottle 编写的一个简单课表查看页面, 可以筛选每周的课程, 可以在手机上安装 qpython 并安装好 hfu_stu_lib 后在手机上运行
        
        1.1.1 (20160330)
        ++++++++++++++++
        
        **功能和改进**
        
        - 添加了 ``utils.filter_curriculum``, 筛选出指定星期[和指定星期几]的课程
        - 所有接口文档添加里 ``@structure`` 描述标记用来描述返回数据的结构和类型
        
        **小的改进**
        
        - 添加 ``parser.zip`` 函数保证 zip 过程的准确性
        - 添加 ``log.log_result_not_found`` 输出当接口未解析出数据时的日志
        
        **接口改变**
        
        - ``utils.get_host_speed_rank`` 改名为 ``utils.rank_host_speed``
        - ``log.unfinished`` 装饰器被移除
        - ``parser.parse_tr_strs`` 不再接受单个的 ``Tag`` 对象作为参数, 同时现在 ``td`` 下有子标签也会解析结果, 不再报 ``ValueError``
        
        **接口变动**
        
        - ``__init__`` 中的变量, 迁移到了 ``values``
        
        **问题修复**
        
        - 修复了一些接口返回数据字段类型与整体定义不一致的问题
        - 修复了一些接口出现意外的空值导致 zip 长度不一致导致结果出错的问题
        - 统一了返回空值的行为
        
        **文档**
        
        - 对应地更新了 ``功能特性`` 这一部分
        
        1.1.0 (20160310)
        ++++++++++++++++
        
        **功能和改进**
        
        - 现在支持合肥校区的教务系统了
        
        **小的改进**
        
        - 简单的修改了一下例子
        
        **接口改变**
        
        - 所有继承自 ``model.BaseSession`` 的类现在需要一个 ``is_hefei`` 参数来确定是否是合肥校区
        
        **问题修复**
        
        - 修复 ``model.StudentSession.get_selected_courses`` 的费用字段使用了错误的整数类型
        - 修复 ``model.GuestSession.get_course_classes`` 键值分离由于特殊情况导致的错误, 同时也对其他方法进行了相应的修改避免类似问题发生
        - 修复 ``model.APIResult.__bool__`` 错误
        
        **文档**
        
        - 补充部分接口的文档
        
        **其他杂项**
        
        - 补充和修复了测试用例
        - 为了保护贡献者隐私将测试模块从线上仓库删除, 对用户没有任何影响
        
        1.0.1 (20160308)
        ++++++++++++++++
        
        **其他杂项**
        
        - 将 ``lxml`` 解析器改为内置的 ``html.parser``, 降低了使用门槛, 减少了依赖
        
        1.0.0 (20160307)
        ++++++++++++++++
        
        **功能和改进**
        
        - 精简了架构,现在接口区分更清晰,现在支持单独的会话配置,同时不会再因动态绑定接口而无法进行代码提示
        - 添加了 ``util.cal_term_code`` 和 ``util.term_str2code`` 计算学期代码
        - 添加了 ``model.GuestSession.get_selecting_lesson_time`` 查询选课时间
        - 添加 ``get_host_speed_rank``,由于宣城校区校内还有多个镜像站点,现在提供了测试地址速度排行的功能
        - 现在能够自动更新会话保持登录状态了
        
        **小的改进**
        
        - ``change_lesson`` 现在能够判断当前是否能够选课
        - ``get_lessons_can_be_selected`` 导出的结果现在是格式化后的了
        - ``model.StudentSession.get_stu_timetable`` 现在返回的上课周数为周数列表便于实际处理
        - ``get_selected_lessons`` 结果中的 ``费用`` 和 ``学分`` 两个字段从字符串分别改为了整型和浮点型
        - 调整了 ``model.GuestSession.get_teaching_plan`` 的参数使使用更加方便
        - 统一了 ``model.StudentSession.get_code`` 的结果键值为中文
        - 现在登录时能够判断是否是煞笔的防注入系统导致无法登陆并且如果是宣城校区会自动选取可用地址重新登录
        
        
        **接口改变**
        
        - 去除了 ``const``, ``session``, ``api``, ``api_request_builder``, ``core``
        - 将原来的 ``api`` 中所有的接口根据要求的登录权限不同分别迁移到了 ``model.GuestSession`` 和 ``model.StudentSession``
        - 将原来的 ``core`` 中的 ``@unstable``, ``@unfinish`` 迁移到了 ``log`` 模块中
        - ``const`` 中的配置项迁移到了 ``BaseSession`` 中, 现在的配置是会话级而不是全局的,这样可以方便的根据需要进行修改
        - ``util.store_api_result`` 迁移到了 ``model.APIResult.store_api_result`` 并稍微调整了一下参数
        - 重新命名了大量接口使其更易理解, 同时纠正命名的错误, 接口的重命名状态如下
            - ``get_selecting_lesson_time`` -> ``get_system_state``
            - ``search_lessons`` -> ``search_course``
            - ``get_lesson_classes`` -> ``get_course_classes``
            - ``get_stu_info`` -> ``get_my_info``
            - ``get_stu_grades`` -> ``get_my_achievements``
            - ``get_stu_timetable`` -> ``get_my_curriculum``
            - ``get_stu_feeds`` -> ``get_my_fees``
            - ``get_optional_lessons`` -> ``get_optional_courses``
            - ``get_selected_lessons`` -> ``get_selected_courses``
            - ``is_lesson_selected`` -> ``check_courses``
            - ``get_lessons_can_be_selected`` -> ``get_selectable_courses``
        
        **接口变动**
        
        - 现在登录也看作是一个接口,进行了重构
        - 现在所有的接口返回的都是 ``model.APIResult`` 对象
        
        **问题修复**
        
        - 修复发送登录权限不一致时仍会发送请求的问题
        - 修复 ``AuthSession`` 初始化时参数判断逻辑错误
        - 修复 ``model.APIRequest`` 初始化时继承参数错误
        - 修复 ``api.get_optional_lessons`` 由于疏忽缺少一个参数
        - 修复 ``model.StudentSession.get_stu_timetable`` 上课周数匹配情况的遗漏
        - 修复 ``model.GuestSession.search_lessons`` 由于编码问题无法使用课程名称搜索的问题
        - 修复 ``parser.parse_tr_strs`` 触发异常时字符串格式错误的问题
        
        **文档**
        
        - 在**高级技巧**一章添加了例子
        
        **其他杂项**
        
        - 将默认的测试模块从 ``unitest`` 迁移到了 ``pytest``
        - 添加大量测试,Python 版本覆盖 2.6-3.5
        
        
        0.5.0 (20160225)
        ++++++++++++++++
        
        - 重构 ``api_request_builder.GetLessonClasses``,
              现在可以返回课程已选人数, 课程容量, 时间地点等信息,
              同时修复了一些问题
        - 添加 ``api.get_lessons_can_be_selected``,
              获取可以选上的课程教学班级
        - 合并 ``api.select_lesson`` 和 ``api.delete_lesson`` 为
              ``api.change_lesson`` 并重构了逻辑
        - 修改 ``api.is_lesson_selected`` 参数类型为 list,
              避免使用中重复调用导致发送大量冗余的请求
        - 重构 ``parser.parse_tr_strs`` , 现在支持单个值输入输出
        - 添加 ``parser.dict_list_2_tuple_set``
        - 提升兼容性
        
        0.4.2 (20160218)
        ++++++++++++++++
        
        - 修复由于配置遗漏导致无法安装的问题
        
        0.4.1 (20160217)
        ++++++++++++++++
        
        - 修复一些潜在问题
        - 更新文档
        
        0.4.0 (20160216)
        ++++++++++++++++
        
        - 删除缓存模块及相关接口
        - 分离一般接口与请求接口, 去除了 ``g`` 对象, 只使用列表 ``all_api``
              保存注册的一般接口
        - 将 ``AuthSession.catch_response`` 删除, 改用
              ``AuthSession.api_request``
        - 新增了 ``model`` 模块, 包含 ``model.APIRequestBuilder``,
              ``model.APIRequest``, ``model.APIResult`` 三个类
        - api 模块合并为单个文件, 添加了请求生成与响应处理的
              ``api_request_builder`` 模块
        - 新的架构避免了 ``api`` 注册冗余以及 ``api`` 与 ``session``
              的交叉调用, 简化模型, 增加了灵活性, 并且不改变之前使用 session
              调用接口的方式
        - 修改了 ``api.get_stu_info`` 中照片地址的生成方式
        
        0.3.5 (20160208)
        ++++++++++++++++
        
        - 修复 ``session.AuthSession`` 初始化时的逻辑错误
        - 修改缓存 md5 计算方式
        - 兼容 Python 3.X
        
        0.3.4 (20151030)
        ++++++++++++++++
        
        - 添加 MANIFEST.in
        - 提交到了官方仓库
        
        0.3.3 (20151030)
        ++++++++++++++++
        
        - 修复 setup.py 配置中的一处错误
        - 提交到了官方仓库
        
        0.3.2 (20151030)
        ++++++++++++++++
        
        - 修改持续集成通知
        - 修复 anydbm 在不同环境下触发的 AttributeError: get
        
        0.3.1 (20151030)
        ++++++++++++++++
        
        - 修复接口注册前后的参数差异导致 ``cal_cache_md5``
              计算结果不正确的问题
        - 添加了更多的测试用例
        
        0.3.0 (20151029)
        ++++++++++++++++
        
        - 修改 ``regist_api`` 为 ``register_api``
        - 默认在安装uniout的情况下使用其输出unicode内容方便使用
        - 改用元类来绑定接口, 提升声明对象时的效率
        - 预定义了用户类型, ``user_type`` 参数使用预定义变量
        - ``cal_gpa`` 精度改为5位小数, 与学校一致
        - 添加缓存功能, 你可以通过一个全局的缓存管理对象管理缓存了,
              模块内置了 ``MemoryCache`` 和 ``FileCache``, 当然你也可以继承
              ``BaseCache`` 编写新的缓存管理对象, 模块会自动帮你注册
        
        0.2.0 (20151025)
        ++++++++++++++++
        
        - 调整了模块结构
        - 分离了 ``session`` 与 接口, 通过一个统一的 ``AuthSession``
              自动绑定接口, 参数原来 ``StuLib`` 接口参数相同
        - 区分了用户类型, AuthSession 即使没有登录也能访问公共接口了
        - 添加了 ``regist_api`` ,
              现在你可以在不修改模块代码的情况下添加自己的接口了
        
        0.1.3 (20150912)
        ++++++++++++++++
        
        - 修复因 ``StuLib`` 初始化时未对 ``stu_id`` 进行类型转换而导致
              ``StuLib.get_stu_info`` 出错的问题
        
        0.1.2 (20150912)
        ++++++++++++++++
        
        - 修复安装时 README.md 缺失的问题
        
        0.1.1 (20150912)
        ++++++++++++++++
        
        - 添加了一些单元测试
        
        0.1.0 (20150911)
        ++++++++++++++++
        
        - 解决 ``requests`` 不能对 GBK 转 UTF8 无损转换的问题
        - 添加 ``StuLib.catch_response`` , 抽象了响应的获取,
              提升了代码的可维护性
        
        0.0.4 (20150910)
        ++++++++++++++++
        
        - 修复了 ``StuLib.get_class_student``
              中由于教务网页代码严重的错误导致页面无法解析而不可用的问题
        - 添加了 ``StuLib.get_class_student`` 的测试用例
        - 由于 ``requests`` 返回的的网页无法做到无损转码, 将传递
              ``BeautifulSoup`` 的文档改为原始编码文档,将转码工作交给
              ``BeautifulSoup`` 处理, 但用到正则匹配的方法还存在此问题
        
        0.0.3 (20150909)
        ++++++++++++++++
        
        - 统一将返回的课程代码进行大写转换,
              避免因学校课程代码大小写的不统一产生不可预料的问题
        - 重构了 ``StuLib.select_lesson`` , 现在支持更好地批量选课以及更好地结果处理过程
        - 重构了 ``StuLib.delete_lesson`` , 现在支持批量删课以及更好地结果处理过程
        
        0.0.2 (20150903)
        ++++++++++++++++
        
        - 重构了 ``StuLib.select_lesson`` 的参数处理过程,
              由于第二次选课结束暂时没有完成对提交结果的处理
        - 添加 Travis IC 持续集成工具
        
        0.0.1 (20150902)
        ++++++++++++++++
        
        - 修复 ``StuLib.get_class_info`` 出错
        - 添加 教师信息查询 ``StuLib.get_teacher_info`` 功能
        - 将 ``StuLib.get_url`` 的 ``code`` 修改为对应的方法名称
        - 修复 ``StuLib.change_password`` 正则匹配不完整的问题
        - 修复 ``StuLib.set_telephone`` 正则匹配不完整的问题
        - 添加部分单元测试
        - 调整了包的结构
        
Keywords: hfut,edu,student,interface
Platform: any
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: Topic :: Software Development :: SDK
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
