import unittest

try:
    import mock
except:
    from unittest import mock

from datetime import datetime, timedelta
from iso8601utils.validators import interval, duration, date, time, datetime


class TestValidators(unittest.TestCase):
    def test_interval(self):
        self.assertTrue(interval('P7Y'))
        self.assertTrue(interval('P6W'))
        self.assertTrue(interval('P6Y5M'))
        self.assertTrue(interval('1999-12-31T16:00:00.000Z/2000-12-31T16:00:00.000+00:30'))
        self.assertTrue(interval('2016-08-01T23:10:59.111-09:30/2016-10-02T12:45:21+04:00'))
        self.assertTrue(interval('1999-12-31T16:00:00.000Z/P5DT7H'))
        self.assertTrue(interval('2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z'))
        self.assertFalse(interval('P6Y5M/P9D'))
        self.assertFalse(interval('P6Yasdf'))
        self.assertFalse(interval('7432891'))
        self.assertFalse(interval('23P7DT5H'))
        self.assertFalse(interval('P6Yasdf/P8Y'))
        self.assertFalse(interval('P7Y/asdf'))
        self.assertFalse(interval('7432891/1234'))
        self.assertFalse(interval('asdf/87rf'))
        self.assertFalse(interval('23P7DT5H/89R3'))

    def test_duration(self):
        self.assertTrue(duration('P3Y6M4DT12H30M5S'))
        self.assertTrue(duration('P6M4DT12H30M15S'))
        self.assertTrue(duration('P6M1DT'))
        self.assertTrue(duration('P6D'))
        self.assertTrue(duration('P5M3DT5S'))
        self.assertTrue(duration('P3Y4DT12H5S'))
        self.assertTrue(duration('P3Y4DT12H30M0.5005S'))
        self.assertTrue(duration('PT.5005S'))
        self.assertFalse(duration('P6Yasdf'))
        self.assertFalse(duration('7432891'))
        self.assertFalse(duration('asdf'))
        self.assertFalse(duration('23P7DT5H'))
        self.assertFalse(duration(''))

    def test_date(self):
        self.assertTrue(date('2008-W39-6'))
        self.assertTrue(date('2008W396'))
        self.assertTrue(date('2016W431'))
        self.assertTrue(date('2016-W43-1'))
        self.assertTrue(date('1981-095'))
        self.assertTrue(date('1981095'))
        self.assertTrue(date('1981-04-05'))
        self.assertTrue(date('19810405'))
        self.assertTrue(date('--04-03'))
        self.assertTrue(date('--1001'))
        self.assertFalse(date('2008-W396'))
        self.assertFalse(date('2008W39-6'))
        self.assertFalse(date('198195'))
        self.assertFalse(date('1981-0405'))
        self.assertFalse(date('198104-05'))

    def test_time(self):
        self.assertFalse(time('1234a'))
        self.assertFalse(time('12:30:40.05+0:15'))
        self.assertFalse(time('1230401.05+10:15'))
        self.assertTrue(time('12'))
        self.assertTrue(time('12+05:10'))
        self.assertTrue(time('12-05:10'))
        self.assertTrue(time('13:15'))
        self.assertTrue(time('13:15+05:10'))
        self.assertTrue(time('13:15-05:10'))
        self.assertTrue(time('14:20:50'))
        self.assertTrue(time('14:20:50+05:10'))
        self.assertTrue(time('14:20:50-05:10'))
        self.assertTrue(time('14:20:50+05'))
        self.assertTrue(time('14:20:50-05'))
        self.assertTrue(time('14:20:50+0510'))
        self.assertTrue(time('14:20:50-0510'))
        self.assertTrue(time('12:30:40.05'))
        self.assertTrue(time('12:30:40.05Z'))
        self.assertTrue(time('12:30:40.05+10:15'))
        self.assertTrue(time('12:30:40.05-08:45'))
        self.assertTrue(time('1315'))
        self.assertTrue(time('1315+05:10'))
        self.assertTrue(time('1315-05:10'))
        self.assertTrue(time('142050'))
        self.assertTrue(time('142050+05:10'))
        self.assertTrue(time('142050-05:10'))
        self.assertTrue(time('142050+05'))
        self.assertTrue(time('142050-05'))
        self.assertTrue(time('142050+0510'))
        self.assertTrue(time('142050-0510'))
        self.assertTrue(time('123040.05'))
        self.assertTrue(time('123040.05Z'))
        self.assertTrue(time('123040.05+10:15'))
        self.assertTrue(time('123040.05-08:45'))

    def test_datetime(self):
        self.assertTrue(datetime('2007-04-05T14:30'))
        self.assertTrue(datetime('2007-08-09T12:30Z'))
        self.assertTrue(datetime('2007-08-09T12:30-02:00'))
        self.assertFalse(datetime('007-04-15T12:30'))
        self.assertFalse(datetime('2007-08-09T12:30+0'))
        self.assertFalse(datetime('2007-08-09T12:30-02:aa'))
