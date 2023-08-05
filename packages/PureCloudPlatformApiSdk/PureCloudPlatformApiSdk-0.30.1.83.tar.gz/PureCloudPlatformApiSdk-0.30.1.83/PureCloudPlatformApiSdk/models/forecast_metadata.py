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


class ForecastMetadata(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ForecastMetadata - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'number_of_periods': 'int',
            'period_frequency': 'str',
            'description': 'str',
            'metrics': 'list[str]',
            'last_modified_date': 'datetime',
            'last_modified_by': 'User',
            'status': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'number_of_periods': 'numberOfPeriods',
            'period_frequency': 'periodFrequency',
            'description': 'description',
            'metrics': 'metrics',
            'last_modified_date': 'lastModifiedDate',
            'last_modified_by': 'lastModifiedBy',
            'status': 'status',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._number_of_periods = None
        self._period_frequency = None
        self._description = None
        self._metrics = None
        self._last_modified_date = None
        self._last_modified_by = None
        self._status = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ForecastMetadata.
        The globally unique identifier for the object.

        :return: The id of this ForecastMetadata.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ForecastMetadata.
        The globally unique identifier for the object.

        :param id: The id of this ForecastMetadata.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ForecastMetadata.


        :return: The name of this ForecastMetadata.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ForecastMetadata.


        :param name: The name of this ForecastMetadata.
        :type: str
        """
        
        self._name = name

    @property
    def number_of_periods(self):
        """
        Gets the number_of_periods of this ForecastMetadata.
        The number of periods to be forecasted for

        :return: The number_of_periods of this ForecastMetadata.
        :rtype: int
        """
        return self._number_of_periods

    @number_of_periods.setter
    def number_of_periods(self, number_of_periods):
        """
        Sets the number_of_periods of this ForecastMetadata.
        The number of periods to be forecasted for

        :param number_of_periods: The number_of_periods of this ForecastMetadata.
        :type: int
        """
        
        self._number_of_periods = number_of_periods

    @property
    def period_frequency(self):
        """
        Gets the period_frequency of this ForecastMetadata.
        The frequency of the period

        :return: The period_frequency of this ForecastMetadata.
        :rtype: str
        """
        return self._period_frequency

    @period_frequency.setter
    def period_frequency(self, period_frequency):
        """
        Sets the period_frequency of this ForecastMetadata.
        The frequency of the period

        :param period_frequency: The period_frequency of this ForecastMetadata.
        :type: str
        """
        allowed_values = ["WEEK"]
        if period_frequency.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for period_frequency -> " + period_frequency
            self._period_frequency = "outdated_sdk_version"
        else:
            self._period_frequency = period_frequency.lower()

    @property
    def description(self):
        """
        Gets the description of this ForecastMetadata.
        The description of the forecast to be created

        :return: The description of this ForecastMetadata.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ForecastMetadata.
        The description of the forecast to be created

        :param description: The description of this ForecastMetadata.
        :type: str
        """
        
        self._description = description

    @property
    def metrics(self):
        """
        Gets the metrics of this ForecastMetadata.
        The metrics the forecast is for

        :return: The metrics of this ForecastMetadata.
        :rtype: list[str]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """
        Sets the metrics of this ForecastMetadata.
        The metrics the forecast is for

        :param metrics: The metrics of this ForecastMetadata.
        :type: list[str]
        """
        
        self._metrics = metrics

    @property
    def last_modified_date(self):
        """
        Gets the last_modified_date of this ForecastMetadata.
        The last modified date time of this object. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The last_modified_date of this ForecastMetadata.
        :rtype: datetime
        """
        return self._last_modified_date

    @last_modified_date.setter
    def last_modified_date(self, last_modified_date):
        """
        Sets the last_modified_date of this ForecastMetadata.
        The last modified date time of this object. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param last_modified_date: The last_modified_date of this ForecastMetadata.
        :type: datetime
        """
        
        self._last_modified_date = last_modified_date

    @property
    def last_modified_by(self):
        """
        Gets the last_modified_by of this ForecastMetadata.
        The person who last modified this object

        :return: The last_modified_by of this ForecastMetadata.
        :rtype: User
        """
        return self._last_modified_by

    @last_modified_by.setter
    def last_modified_by(self, last_modified_by):
        """
        Sets the last_modified_by of this ForecastMetadata.
        The person who last modified this object

        :param last_modified_by: The last_modified_by of this ForecastMetadata.
        :type: User
        """
        
        self._last_modified_by = last_modified_by

    @property
    def status(self):
        """
        Gets the status of this ForecastMetadata.
        The status of the creation of the forecast

        :return: The status of this ForecastMetadata.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ForecastMetadata.
        The status of the creation of the forecast

        :param status: The status of this ForecastMetadata.
        :type: str
        """
        allowed_values = ["SUCCESS", "FAILED"]
        if status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for status -> " + status
            self._status = "outdated_sdk_version"
        else:
            self._status = status.lower()

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ForecastMetadata.
        The URI for this object

        :return: The self_uri of this ForecastMetadata.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ForecastMetadata.
        The URI for this object

        :param self_uri: The self_uri of this ForecastMetadata.
        :type: str
        """
        
        self._self_uri = self_uri

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

