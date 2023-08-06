# coding: utf-8
import logging
from abc import ABC, abstractmethod

import pytz
from datetime import datetime

from django.core.validators import validate_email

from djmessenger.receiving import ReceivingType
from djmessenger.utils.serializable import Serializable
from djmessenger.utils.utils import Loggable

"""
================
Filtering Module
================

Filtering module defines a :class:`.BaseFilter` as the most basic abstract class
and all its subclasses provide some specific logic to filter a given
:class:`djmessenger.receiving.Messaging` object


"""
"""
# filtering module

In `should_handle()`, you look at the `Messaging` object and determine whether
this handler should handle this `Messaging`

"""


class BaseFilter(Serializable, Loggable):
    """
    BaseFilter is an ABC for filters, it defines an abstract method which takes
    a Messaging object and returns a bool to indicate whether this Messaging
    should be further processed
    """

    @abstractmethod
    def should_pass(self, messaging):
        """
        Takes a :class:`djmessenger.receiving.Messaging` object and determines
        whether this object should pass this filter and continue

        :param messaging: A Messaging instance to filter against
        :type messaging: djmessenger.receiving.Messaging
        :return: True if the given messaging passed this filter and should
                 continue with the next operation; False otherwise
        :rtype: bool
        """
        return True

    def __str__(self):
        return '<%s>' % self.__class__.__name__

    def __repr__(self):
        return str(self)


class LocationFilter(BaseFilter):
    """
    Pass if messaging is a Location
    """

    def should_pass(self, messaging):
        self.logger.debug('Ready to determine whether %s should handle this '
                          'messaging' % self.__class__.__name__)
        ret = messaging.get_receiving_type() == ReceivingType.LOCATION
        self.logger.debug('We check whether the messaging callback type is '
                          'MESSAGE_RECEIVED_LOCATION. The result is %s' % ret)
        return ret


class StickerFilter(BaseFilter):
    """
    Pass if messaging is a STICKER and the id is within STICKER_IDS
    """
    STICKER_IDS = tuple()

    def should_pass(self, messaging):
        self.logger.debug('Ready to determine whether %s should handle this '
                          'messaging' % self.__class__.__name__)
        ret = messaging.get_receiving_type() == ReceivingType.STICKER \
              and str(messaging.get_sticker_id())[
                  -3:] in self.__class__.STICKER_IDS
        self.logger.debug(
            'We determine whether we should handle the messaging by '
            '1. check if the callback type is MESSAGE_RECEIVED_STICKER'
            ', 2. check if the last 3 digit of sticker id is in '
            '%s. The result is %s' % (self.__class__.STICKER_IDS, ret))
        return ret

    def __str__(self):
        return '%s with STICKER_IDS %s' % (self.__class__.__name__,
                                           self.__class__.STICKER_IDS)


class ThumbUpFilter(StickerFilter):
    STICKER_IDS = ('810', '814', '822')


class PostbackFilter(BaseFilter):
    """
    Pass if messaging is a POSTBACK
    """

    def should_pass(self, messaging):
        return messaging.get_receiving_type() == ReceivingType.POSTBACK


class SimpleTextRegexFilter(BaseFilter):
    """
    Pass if messaging has a text that matches the regex

    An example in :class:`djmessenger.utils.default_routing_policy`

    ::

        {
            "name": "djmessenger.filtering.SimpleTextRegexFilter",
            "args": {
                "regex": "^你好$"
            }
        }

    """

    def __init__(self, regex=None):
        self.regex = regex

    def should_pass(self, messaging):
        from re import compile

        if not self.regex:
            ret = len(messaging.get_text()) > 0
            self.logger.debug('No regex provided for SimpleTextBaseHandler, '
                              'should_handle() evaluates as %s because text [%s] was'
                              ' provided' % (ret, messaging.get_text()))
            return ret
        rex = compile(self.regex)
        res = rex.fullmatch(messaging.get_text())
        ret = res is not None and len(messaging.get_text()) > 0
        logging.debug('Given text and regex (%s, %s), should_pass() is %s' %
                      (messaging.get_text(), self.regex, ret))
        return ret

    def __str__(self):
        return '<%s (regex = %s)>' % (self.__class__.__name__, self.regex)


class MultimediaFilter(BaseFilter):
    """
    Pass if messaging is multimedia
    """

    def should_pass(self, messaging):
        receiving_type = messaging.get_receiving_type()
        return receiving_type in (ReceivingType.IMAGE, ReceivingType.AUDIO,
                                  ReceivingType.VIDEO, ReceivingType.FILE)


class AuthenticationFilter(BaseFilter):
    def should_pass(self, messaging):
        return messaging.get_receiving_type() == ReceivingType.AUTHENTICATION


class EmailFilter(BaseFilter):
    """
    Filter that the text sent by user is a valid email address
    """

    def should_pass(self, messaging):
        if messaging.get_receiving_type() != ReceivingType.SIMPLE_TEXT:
            return False
        return validate_email(messaging.get_text())


class DatetimeRangeFilter(BaseFilter):
    """
    Filter that passes if the messaging timestamp is within the predefined
    time period

    An example in policy

    ::

        {
            "name": "djmessenger.filtering.DatetimeRangeFilter",
            "args": {
                "start_time": "2016-1-1T00:00:00Z-0800",
                "end_time": "2017-1-1T01:00:00Z-0800"
            }
        }

    """

    FORMAT = '%Y-%m-%dT%H:%M:%SZ%z'

    def __init__(self, start_time, end_time):
        """

        :param start_time: start time in the format of %Y-%m-%dT%H:%M:%SZ%z
        :type start_time: str

        :param end_time: end time in the format of %Y-%m-%dT%H:%M:%SZ%z
        :type end_time: str

        :param utc_offset: The timezone for this time period by specifying the
                           offset from UTC
        :type utc_offset: int
        """
        self.start_time = start_time
        self.end_time = end_time

    def should_pass(self, messaging):
        try:
            start_timestamp = datetime.strptime(self.start_time,
                                                self.FORMAT).timestamp() * 1000
            end_timestamp = datetime.strptime(self.end_time,
                                              self.FORMAT).timestamp() * 1000
            messaging_timestamp = messaging.timestamp
            ret = start_timestamp <= messaging_timestamp <= end_timestamp
            self.logger.debug(
                'DatetimeRangeFilter checking %d <= %d <= %d, result '
                'is %s'
                % (start_timestamp, messaging_timestamp,
                   end_timestamp, ret))
            return ret
        except Exception as e:
            self.logger.exception(
                '%s failed to convert either start time or end time because '
                '%s. The expected format is %s. Please double check the time '
                'strings given in settings are valid'
                % (self.__class__.__name__, e, self.FORMAT))
            return True

    def __str__(self):
        return '<%s (start time: %s, end time = %s)>' \
               % (self.__class__.__name__, self.start_time, self.end_time)


class DailyTimeRangeFilter(BaseFilter):
    """
    DailyTimeFilter takes 2 arguments, start_hour and end_hour just like
    :class:`.DatetimeRangeFilter` but these times format is in 24-hour

    start_hour = 0 - 23
    end_hour = 0 - 23 and must larger than start_hour

    and optional start_minute and end_minute

    start_minute = 0 - 59
    end_minute = 0 - 59

    which means this filter checks whether the messaging was received within
    those 2 times everyday
    """

    def __init__(self, start_hour, end_hour, timezone='UTC', start_minute=0,
                 end_minute=0):
        """

        :param start_hour: 0 - 23
        :type start_hour: str

        :param end_hour: 0 - 23
        :type end_hour: str

        :param timezone: actual geographic timezones, as listed in :func:`pytz.all_timezones()`
        :type timezone: str

        :param start_minute: 0 - 59
        :type start_minute: str

        :param end_minute: 0 - 59
        :type end_minute: str

        """
        try:
            self.start_hour = int(start_hour)
            self.end_hour = int(end_hour)
            self.start_minute = int(start_minute)
            self.end_minute = int(end_minute)
            self.timezone = pytz.timezone(timezone)
        except Exception as e:
            self.logger.exception('DailyTimeFilter constructor got invalid '
                                  'arguments %s' % e)
            raise e
        if not 0 <= self.start_hour <= 23:
            raise ValueError('start_hour should be between 0-23')
        if not 0 <= self.end_hour <= 23:
            raise ValueError('end_hour should be between 0-23')
        if not 0 <= self.start_minute <= 59:
            raise ValueError('start_minute should be between 0-59')
        if not 0 <= self.end_minute <= 59:
            raise ValueError('end_minute should be between 0-59')
        if self.start_hour * 100 + self.start_minute >= self.end_hour * 100 + self.end_minute:
            raise ValueError('%s constructor got invalid arguments because '
                             'start time %d:%d should be less than end time'
                             ' %d:%d' % (self.__class__, self.start_hour,
                                         self.start_minute, self.end_hour,
                                         self.end_minute))

    def should_pass(self, messaging):
        now = datetime.now(self.timezone)
        time = now.hour * 100 + now.hour
        start_time = self.start_hour * 100 + self.start_minute
        end_time = self.end_hour * 100 + self.end_minute
        return start_time <= time <= end_time
