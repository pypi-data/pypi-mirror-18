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


class AggregateMetricData(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AggregateMetricData - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'metric': 'str',
            'qualifier': 'str',
            'stats': 'StatisticalSummary'
        }

        self.attribute_map = {
            'metric': 'metric',
            'qualifier': 'qualifier',
            'stats': 'stats'
        }

        self._metric = None
        self._qualifier = None
        self._stats = None

    @property
    def metric(self):
        """
        Gets the metric of this AggregateMetricData.


        :return: The metric of this AggregateMetricData.
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this AggregateMetricData.


        :param metric: The metric of this AggregateMetricData.
        :type: str
        """
        allowed_values = ["tSegmentDuration", "oTotalCriticalScore", "oTotalScore", "nEvaluations", "tAbandon", "tIvr", "tAnswered", "tAcd", "tTalk", "tHeld", "tTalkComplete", "tHeldComplete", "tAcw", "tHandle", "tWait", "tAgentRoutingStatus", "tOrganizationPresence", "tSystemPresence", "tUserResponseTime", "tAgentResponseTime", "nOffered", "nOverSla", "nTransferred", "nOutboundAttempted", "nOutboundConnected", "nOutboundAbandoned", "nError", "oServiceTarget", "oServiceLevel", "tActive", "tInactive", "oActiveUsers", "oMemberUsers", "oActiveQueues", "oMemberQueues", "oInteracting", "oWaiting", "oOnQueueUsers", "oOffQueueUsers"]
        if metric.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for metric -> " + metric
            self._metric = "outdated_sdk_version"
        else:
            self._metric = metric.lower()

    @property
    def qualifier(self):
        """
        Gets the qualifier of this AggregateMetricData.


        :return: The qualifier of this AggregateMetricData.
        :rtype: str
        """
        return self._qualifier

    @qualifier.setter
    def qualifier(self, qualifier):
        """
        Sets the qualifier of this AggregateMetricData.


        :param qualifier: The qualifier of this AggregateMetricData.
        :type: str
        """
        
        self._qualifier = qualifier

    @property
    def stats(self):
        """
        Gets the stats of this AggregateMetricData.


        :return: The stats of this AggregateMetricData.
        :rtype: StatisticalSummary
        """
        return self._stats

    @stats.setter
    def stats(self, stats):
        """
        Sets the stats of this AggregateMetricData.


        :param stats: The stats of this AggregateMetricData.
        :type: StatisticalSummary
        """
        
        self._stats = stats

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

