# -*- coding:utf-8 -*-
"""
一些能够帮你提升效率的辅助函数
"""
from __future__ import unicode_literals, division

from copy import deepcopy
from datetime import timedelta
from threading import Thread

import requests
import requests.exceptions
from six.moves import urllib

from .log import logger
from .value import ENV

__all__ = ['get_point', 'cal_gpa', 'cal_term_code', 'term_str2code', 'sort_hosts', 'filter_curriculum']


def get_point(grade_str):
    """
    根据成绩判断绩点

    :param grade_str: 一个字符串,因为可能是百分制成绩或等级制成绩
    :return: 成绩绩点
    :rtype: float
    """
    try:
        grade = float(grade_str)
        assert 0 <= grade <= 100
        if 95 <= grade <= 100:
            return 4.3
        elif 90 <= grade < 95:
            return 4.0
        elif 85 <= grade < 90:
            return 3.7
        elif 82 <= grade < 85:
            return 3.3
        elif 78 <= grade < 82:
            return 3.0
        elif 75 <= grade < 78:
            return 2.7
        elif 72 <= grade < 75:
            return 2.3
        elif 68 <= grade < 72:
            return 2.0
        elif 66 <= grade < 68:
            return 1.7
        elif 64 <= grade < 66:
            return 1.3
        elif 60 <= grade < 64:
            return 1.0
        else:
            return 0.0
    except ValueError:
        if grade_str == '优':
            return 3.9
        elif grade_str == '良':
            return 3.0
        elif grade_str == '中':
            return 2.0
        elif grade_str == '及格':
            return 1.2
        elif grade_str in ('不及格', '免修', '未考'):
            return 0.0
        else:
            raise ValueError('{:s} 不是有效的成绩'.format(grade_str))


def cal_gpa(grades):
    """
    根据成绩数组计算课程平均绩点和 gpa, 算法不一定与学校一致, 结果仅供参考

    :param grades: :meth:`models.StudentSession.get_my_achievements` 返回的成绩数组
    :return: 包含了课程平均绩点和 gpa 的元组
    """
    # 课程总数
    courses_sum = len(grades)
    # 课程绩点和
    points_sum = 0
    # 学分和
    credit_sum = 0
    # 课程学分 x 课程绩点之和
    gpa_points_sum = 0
    for grade in grades:
        point = get_point(grade.get('补考成绩') or grade['成绩'])
        credit = float(grade['学分'])

        points_sum += point
        credit_sum += credit
        gpa_points_sum += credit * point
    ave_point = points_sum / courses_sum
    gpa = gpa_points_sum / credit_sum
    return round(ave_point, 5), round(gpa, 5)


def cal_term_code(year, is_first_term=True):
    """
    计算对应的学期代码

    :param year: 学年开始年份,例如 "2012-2013学年第二学期" 就是 2012
    :param is_first_term: 是否为第一学期
    :type is_first_term: bool
    :return: 形如 "022" 的学期代码
    """
    if year <= 2001:
        msg = '出现了超出范围年份: {}'.format(year)
        raise ValueError(msg)
    term_code = (year - 2001) * 2
    if is_first_term:
        term_code -= 1
    return '%03d' % term_code


def term_str2code(term_str):
    """
    将学期字符串转换为对应的学期代码串

    :param term_str: 形如 "2012-2013学年第二学期" 的学期字符串
    :return: 形如 "022" 的学期代码
    """
    result = ENV['TERM_PATTERN'].match(term_str).groups()
    year = int(result[0])
    return cal_term_code(year, result[1] == '一')


def sort_hosts(hosts, method='GET', path='/', timeout=(5, 10), **kwargs):
    """
    测试各个地址的速度并返回排名, 当出现错误时消耗时间为 INFINITY = 10000000

    :param method: 请求方法
    :param path: 默认的访问路径
    :param hosts: 进行的主机地址列表, 如 `['http://222.195.8.201/']`
    :param timeout: 超时时间, 可以是一个浮点数或 形如 ``(连接超时, 读取超时)`` 的元祖
    :param kwargs: 其他传递到 ``requests.request`` 的参数
    :return: 形如 ``[(访问耗时, 地址)]`` 的排名数据
    """
    ranks = []

    class HostCheckerThread(Thread):
        def __init__(self, host):
            super(HostCheckerThread, self).__init__()
            self.host = host

        def run(self):
            INFINITY = 10000000
            try:
                url = urllib.parse.urljoin(self.host, path)
                res = requests.request(method, url, timeout=timeout, **kwargs)
                res.raise_for_status()
                cost = res.elapsed.total_seconds() * 1000
            except Exception as e:
                logger.warning('访问出错: %s', e)
                cost = INFINITY
            # http://stackoverflow.com/questions/6319207/are-lists-thread-safe
            ranks.append((cost, self.host))

    threads = [HostCheckerThread(u) for u in hosts]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    ranks.sort()
    return ranks


def filter_curriculum(curriculum, week, weekday=None):
    """
    筛选出指定星期[和指定星期几]的课程

    :param curriculum: 课程表数据
    :param week: 需要筛选的周数, 是一个代表周数的正整数
    :param weekday: 星期几, 是一个代表星期的整数, 1-7 对应周一到周日
    :return: 如果 weekday 参数没给出, 返回的格式与原课表一致, 但只包括了在指定周数的课程, 否则返回指定周数和星期几的当天课程
    """
    if weekday:
        c = [deepcopy(curriculum[weekday - 1])]
    else:
        c = deepcopy(curriculum)
    for d in c:
        l = len(d)
        for t_idx in range(l):
            t = d[t_idx]
            if t is None:
                continue
            # 一般同一时间课程不会重复，重复时给出警告
            t = list(filter(lambda k: week in k['上课周数'], t)) or None
            if t is not None and len(t) > 1:
                logger.warning('第 %d 周周 %d 第 %d 节课有冲突: %s', week, weekday or c.index(d) + 1, t_idx + 1, t)
            d[t_idx] = t
    return c[0] if weekday else c


def curriculum2schedule(curriculum, first_day, compress=False, time_table=None):
    """
    将课程表转换为上课时间表, 如果 compress=False 结果是未排序的, 否则为压缩并排序后的上课时间表

    :param curriculum: 课表
    :param first_day: 第一周周一, 如 datetime.datetime(2016, 8, 29)
    :param compress: 压缩连续的课时为一个
    :param time_table: 每天上课的时间表, 形如 ``((start timedelta, end timedelta), ...)`` 的 11 × 2 的矩阵
    :return: [(datetime.datetime, str) ...]
    """
    schedule = []
    time_table = time_table or (
        (timedelta(hours=8), timedelta(hours=8, minutes=50)),
        (timedelta(hours=9), timedelta(hours=9, minutes=50)),
        (timedelta(hours=10, minutes=10), timedelta(hours=11)),
        (timedelta(hours=11, minutes=10), timedelta(hours=12)),
        (timedelta(hours=14), timedelta(hours=14, minutes=50)),
        (timedelta(hours=15), timedelta(hours=15, minutes=50)),
        (timedelta(hours=16), timedelta(hours=16, minutes=50)),
        (timedelta(hours=17), timedelta(hours=17, minutes=50)),
        (timedelta(hours=19), timedelta(hours=19, minutes=50)),
        (timedelta(hours=19, minutes=50), timedelta(hours=20, minutes=40)),
        (timedelta(hours=20, minutes=40), timedelta(hours=21, minutes=30))
    )
    for i, d in enumerate(curriculum):
        for j, cs in enumerate(d):
            for c in cs or []:
                course = '{name}[{place}]'.format(name=c['课程名称'], place=c['课程地点'])
                for week in c['上课周数']:
                    day = first_day + timedelta(weeks=week - 1, days=i)
                    start, end = time_table[j]
                    item = (week, day + start, day + end, course)
                    schedule.append(item)

    schedule.sort()
    if compress:
        new_schedule = [schedule[0]]
        for i in range(1, len(schedule)):
            sch = schedule[i]
            # 同一天的连续课程
            if new_schedule[-1][1].date() == sch[1].date() and new_schedule[-1][3] == sch[3]:
                # 更新结束时间
                old_item = new_schedule.pop()
                # week, start, end, course
                new_item = (old_item[0], old_item[1], sch[2], old_item[3])
            else:
                new_item = sch
            new_schedule.append(new_item)
        return new_schedule

    return schedule
