# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from hfut import util
from . import TestBase


class TestUtil(TestBase):
    def test_get_point(self):
        assert util.get_point('100') == 4.3
        assert util.get_point(100) == 4.3
        assert util.get_point(90) == 4.0
        assert util.get_point(85) == 3.7
        assert util.get_point(82) == 3.3
        assert util.get_point(78) == 3.0
        assert util.get_point(75) == 2.7
        assert util.get_point(72) == 2.3
        assert util.get_point(68) == 2.0
        assert util.get_point(66) == 1.7
        assert util.get_point(64) == 1.3
        assert util.get_point(60) == 1.0
        assert util.get_point(50) == 0.0
        assert util.get_point('优') == 3.9
        assert util.get_point('优') == 3.9
        assert util.get_point('良') == 3.0
        assert util.get_point('中') == 2.0
        assert util.get_point('及格') == 1.2
        assert util.get_point('不及格') == 0
        assert util.get_point('未考') == 0
        assert util.get_point('免修') == 0

        with pytest.raises(AssertionError):
            util.get_point(150)
        with pytest.raises(ValueError):
            util.get_point('蛤蛤')

    def test_cal_gpa(self, shortcuts):
        assert isinstance(util.cal_gpa(shortcuts.get_my_achievements()), tuple)

    def test_cal_term_code(self):
        with pytest.raises(ValueError):
            util.cal_term_code(2001)
        assert util.cal_term_code(2002) == '001'
        assert util.cal_term_code(2002, is_first_term=False) == '002'

    def test_term_str2code(self):
        assert util.term_str2code('2002-2003学年第一学期') == '001'
        assert util.term_str2code('2002-2003学年第二学期') == '002'
        assert util.term_str2code('2002-2003学年 第二学期') == '002'
        with pytest.raises(AttributeError):
            assert util.term_str2code('第二学期')

    def test_get_host_speed_rank(self):
        r = util.sort_hosts([
            'http://172.18.6.93/',
            'http://172.18.6.94/',
            'http://172.18.6.95/',
            'http://172.18.6.96/',
            'http://172.18.6.97/',
            'http://172.18.6.98/',
            'http://172.18.6.99/'
        ])
        assert len(r) == 7
        assert util.sort_hosts(['http://qq.com'])[0][0] == 10000000
        assert util.sort_hosts(timeout=0)[0][0] == 10000000

    def test_filter_curriculum(self, shortcuts):
        c = shortcuts.get_my_curriculum()['课表']
        res = util.filter_curriculum(c, 2)
        assert len(res) == 7
        for v in res:
            assert len(v) == 11
        res = util.filter_curriculum(c, 2, 1)
        assert len(res) == 11

    def test_schedule_and_calendar(self, shortcuts):
        curriculum = shortcuts.get_my_curriculum()
        from datetime import datetime
        first_day = datetime(2016, 8, 29)
        schedule1 = util.curriculum2schedule(curriculum['课表'], first_day)
        schedule2 = util.curriculum2schedule(curriculum['课表'], first_day, compress=True)
        assert len(schedule1) > len(schedule2)
