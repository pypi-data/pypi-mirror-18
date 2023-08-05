# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class InteractionStatAlertNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        InteractionStatAlertNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'rule_id': 'str',
            'dimension': 'str',
            'dimension_value': 'str',
            'dimension_value_name': 'str',
            'metric': 'str',
            'media_type': 'str',
            'numeric_range': 'str',
            'statistic': 'str',
            'value': 'float',
            'unread': 'bool',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'notification_users': 'list[HeartBeatAlertNotificationNotificationUsers]',
            'alert_types': 'list[str]'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'rule_id': 'ruleId',
            'dimension': 'dimension',
            'dimension_value': 'dimensionValue',
            'dimension_value_name': 'dimensionValueName',
            'metric': 'metric',
            'media_type': 'mediaType',
            'numeric_range': 'numericRange',
            'statistic': 'statistic',
            'value': 'value',
            'unread': 'unread',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'notification_users': 'notificationUsers',
            'alert_types': 'alertTypes'
        }

        self._id = None
        self._name = None
        self._rule_id = None
        self._dimension = None
        self._dimension_value = None
        self._dimension_value_name = None
        self._metric = None
        self._media_type = None
        self._numeric_range = None
        self._statistic = None
        self._value = None
        self._unread = None
        self._start_date = None
        self._end_date = None
        self._notification_users = None
        self._alert_types = None

    @property
    def id(self):
        """
        Gets the id of this InteractionStatAlertNotification.


        :return: The id of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this InteractionStatAlertNotification.


        :param id: The id of this InteractionStatAlertNotification.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this InteractionStatAlertNotification.


        :return: The name of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this InteractionStatAlertNotification.


        :param name: The name of this InteractionStatAlertNotification.
        :type: str
        """
        
        self._name = name

    @property
    def rule_id(self):
        """
        Gets the rule_id of this InteractionStatAlertNotification.


        :return: The rule_id of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id):
        """
        Sets the rule_id of this InteractionStatAlertNotification.


        :param rule_id: The rule_id of this InteractionStatAlertNotification.
        :type: str
        """
        
        self._rule_id = rule_id

    @property
    def dimension(self):
        """
        Gets the dimension of this InteractionStatAlertNotification.


        :return: The dimension of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        """
        Sets the dimension of this InteractionStatAlertNotification.


        :param dimension: The dimension of this InteractionStatAlertNotification.
        :type: str
        """
        allowed_values = ["queueId", "userId"]
        if dimension not in allowed_values:
            raise ValueError(
                "Invalid value for `dimension`, must be one of {0}"
                .format(allowed_values)
            )

        self._dimension = dimension

    @property
    def dimension_value(self):
        """
        Gets the dimension_value of this InteractionStatAlertNotification.


        :return: The dimension_value of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._dimension_value

    @dimension_value.setter
    def dimension_value(self, dimension_value):
        """
        Sets the dimension_value of this InteractionStatAlertNotification.


        :param dimension_value: The dimension_value of this InteractionStatAlertNotification.
        :type: str
        """
        
        self._dimension_value = dimension_value

    @property
    def dimension_value_name(self):
        """
        Gets the dimension_value_name of this InteractionStatAlertNotification.


        :return: The dimension_value_name of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._dimension_value_name

    @dimension_value_name.setter
    def dimension_value_name(self, dimension_value_name):
        """
        Sets the dimension_value_name of this InteractionStatAlertNotification.


        :param dimension_value_name: The dimension_value_name of this InteractionStatAlertNotification.
        :type: str
        """
        
        self._dimension_value_name = dimension_value_name

    @property
    def metric(self):
        """
        Gets the metric of this InteractionStatAlertNotification.


        :return: The metric of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this InteractionStatAlertNotification.


        :param metric: The metric of this InteractionStatAlertNotification.
        :type: str
        """
        allowed_values = ["tAbandon", "tAnswered", "tTalk", "nOffered", "tHandle", "nTransferred", "oServiceLevel", "tWait", "tHeld", "tAcw"]
        if metric not in allowed_values:
            raise ValueError(
                "Invalid value for `metric`, must be one of {0}"
                .format(allowed_values)
            )

        self._metric = metric

    @property
    def media_type(self):
        """
        Gets the media_type of this InteractionStatAlertNotification.


        :return: The media_type of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this InteractionStatAlertNotification.


        :param media_type: The media_type of this InteractionStatAlertNotification.
        :type: str
        """
        allowed_values = ["voice", "chat", "email"]
        if media_type not in allowed_values:
            raise ValueError(
                "Invalid value for `media_type`, must be one of {0}"
                .format(allowed_values)
            )

        self._media_type = media_type

    @property
    def numeric_range(self):
        """
        Gets the numeric_range of this InteractionStatAlertNotification.


        :return: The numeric_range of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._numeric_range

    @numeric_range.setter
    def numeric_range(self, numeric_range):
        """
        Sets the numeric_range of this InteractionStatAlertNotification.


        :param numeric_range: The numeric_range of this InteractionStatAlertNotification.
        :type: str
        """
        allowed_values = ["gt", "gte", "lt", "lte", "eq", "ne"]
        if numeric_range not in allowed_values:
            raise ValueError(
                "Invalid value for `numeric_range`, must be one of {0}"
                .format(allowed_values)
            )

        self._numeric_range = numeric_range

    @property
    def statistic(self):
        """
        Gets the statistic of this InteractionStatAlertNotification.


        :return: The statistic of this InteractionStatAlertNotification.
        :rtype: str
        """
        return self._statistic

    @statistic.setter
    def statistic(self, statistic):
        """
        Sets the statistic of this InteractionStatAlertNotification.


        :param statistic: The statistic of this InteractionStatAlertNotification.
        :type: str
        """
        allowed_values = ["count", "min", "ratio", "max"]
        if statistic not in allowed_values:
            raise ValueError(
                "Invalid value for `statistic`, must be one of {0}"
                .format(allowed_values)
            )

        self._statistic = statistic

    @property
    def value(self):
        """
        Gets the value of this InteractionStatAlertNotification.


        :return: The value of this InteractionStatAlertNotification.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this InteractionStatAlertNotification.


        :param value: The value of this InteractionStatAlertNotification.
        :type: float
        """
        
        self._value = value

    @property
    def unread(self):
        """
        Gets the unread of this InteractionStatAlertNotification.


        :return: The unread of this InteractionStatAlertNotification.
        :rtype: bool
        """
        return self._unread

    @unread.setter
    def unread(self, unread):
        """
        Sets the unread of this InteractionStatAlertNotification.


        :param unread: The unread of this InteractionStatAlertNotification.
        :type: bool
        """
        
        self._unread = unread

    @property
    def start_date(self):
        """
        Gets the start_date of this InteractionStatAlertNotification.


        :return: The start_date of this InteractionStatAlertNotification.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this InteractionStatAlertNotification.


        :param start_date: The start_date of this InteractionStatAlertNotification.
        :type: datetime
        """
        
        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this InteractionStatAlertNotification.


        :return: The end_date of this InteractionStatAlertNotification.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this InteractionStatAlertNotification.


        :param end_date: The end_date of this InteractionStatAlertNotification.
        :type: datetime
        """
        
        self._end_date = end_date

    @property
    def notification_users(self):
        """
        Gets the notification_users of this InteractionStatAlertNotification.


        :return: The notification_users of this InteractionStatAlertNotification.
        :rtype: list[HeartBeatAlertNotificationNotificationUsers]
        """
        return self._notification_users

    @notification_users.setter
    def notification_users(self, notification_users):
        """
        Sets the notification_users of this InteractionStatAlertNotification.


        :param notification_users: The notification_users of this InteractionStatAlertNotification.
        :type: list[HeartBeatAlertNotificationNotificationUsers]
        """
        
        self._notification_users = notification_users

    @property
    def alert_types(self):
        """
        Gets the alert_types of this InteractionStatAlertNotification.


        :return: The alert_types of this InteractionStatAlertNotification.
        :rtype: list[str]
        """
        return self._alert_types

    @alert_types.setter
    def alert_types(self, alert_types):
        """
        Sets the alert_types of this InteractionStatAlertNotification.


        :param alert_types: The alert_types of this InteractionStatAlertNotification.
        :type: list[str]
        """
        
        self._alert_types = alert_types

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

