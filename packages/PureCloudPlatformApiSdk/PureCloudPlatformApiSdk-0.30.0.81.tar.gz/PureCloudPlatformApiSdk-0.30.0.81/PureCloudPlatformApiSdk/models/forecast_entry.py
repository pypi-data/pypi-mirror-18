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


class ForecastEntry(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ForecastEntry - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'metric': 'str',
            'dimensions': 'ForecastDimensions',
            'values': 'list[float]'
        }

        self.attribute_map = {
            'metric': 'metric',
            'dimensions': 'dimensions',
            'values': 'values'
        }

        self._metric = None
        self._dimensions = None
        self._values = None

    @property
    def metric(self):
        """
        Gets the metric of this ForecastEntry.
        The metric of the entry

        :return: The metric of this ForecastEntry.
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this ForecastEntry.
        The metric of the entry

        :param metric: The metric of this ForecastEntry.
        :type: str
        """
        allowed_values = ["CALL_VOLUME", "ATT", "ACW", "CHAT_VOLUME"]
        if metric not in allowed_values:
            raise ValueError(
                "Invalid value for `metric`, must be one of {0}"
                .format(allowed_values)
            )

        self._metric = metric

    @property
    def dimensions(self):
        """
        Gets the dimensions of this ForecastEntry.
        The dimensions of the entry

        :return: The dimensions of this ForecastEntry.
        :rtype: ForecastDimensions
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """
        Sets the dimensions of this ForecastEntry.
        The dimensions of the entry

        :param dimensions: The dimensions of this ForecastEntry.
        :type: ForecastDimensions
        """
        
        self._dimensions = dimensions

    @property
    def values(self):
        """
        Gets the values of this ForecastEntry.
        The forecasted values

        :return: The values of this ForecastEntry.
        :rtype: list[float]
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        Sets the values of this ForecastEntry.
        The forecasted values

        :param values: The values of this ForecastEntry.
        :type: list[float]
        """
        
        self._values = values

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

