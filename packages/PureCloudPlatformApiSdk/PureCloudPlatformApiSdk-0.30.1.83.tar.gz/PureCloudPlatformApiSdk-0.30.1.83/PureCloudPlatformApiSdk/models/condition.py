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


class Condition(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Condition - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'type': 'str',
            'inverted': 'bool',
            'attribute_name': 'str',
            'value': 'str',
            'value_type': 'str',
            'operator': 'str',
            'codes': 'list[str]'
        }

        self.attribute_map = {
            'type': 'type',
            'inverted': 'inverted',
            'attribute_name': 'attributeName',
            'value': 'value',
            'value_type': 'valueType',
            'operator': 'operator',
            'codes': 'codes'
        }

        self._type = None
        self._inverted = False
        self._attribute_name = None
        self._value = None
        self._value_type = None
        self._operator = None
        self._codes = None

    @property
    def type(self):
        """
        Gets the type of this Condition.
        The type of the condition

        :return: The type of this Condition.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this Condition.
        The type of the condition

        :param type: The type of this Condition.
        :type: str
        """
        allowed_values = ["wrapupCondition", "contactAttributeCondition", "phoneNumberCondition", "phoneNumberTypeCondition", "callAnalysisCondition"]
        if type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for type -> " + type
            self._type = "outdated_sdk_version"
        else:
            self._type = type.lower()

    @property
    def inverted(self):
        """
        Gets the inverted of this Condition.
        Indicates whether to evaluate for the opposite of the stated condition; default is false

        :return: The inverted of this Condition.
        :rtype: bool
        """
        return self._inverted

    @inverted.setter
    def inverted(self, inverted):
        """
        Sets the inverted of this Condition.
        Indicates whether to evaluate for the opposite of the stated condition; default is false

        :param inverted: The inverted of this Condition.
        :type: bool
        """
        
        self._inverted = inverted

    @property
    def attribute_name(self):
        """
        Gets the attribute_name of this Condition.
        An attribute name associated with the condition (applies only to certain rule conditions)

        :return: The attribute_name of this Condition.
        :rtype: str
        """
        return self._attribute_name

    @attribute_name.setter
    def attribute_name(self, attribute_name):
        """
        Sets the attribute_name of this Condition.
        An attribute name associated with the condition (applies only to certain rule conditions)

        :param attribute_name: The attribute_name of this Condition.
        :type: str
        """
        
        self._attribute_name = attribute_name

    @property
    def value(self):
        """
        Gets the value of this Condition.
        A value associated with the condition

        :return: The value of this Condition.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this Condition.
        A value associated with the condition

        :param value: The value of this Condition.
        :type: str
        """
        
        self._value = value

    @property
    def value_type(self):
        """
        Gets the value_type of this Condition.
        Determines the type of the value associated with the condition

        :return: The value_type of this Condition.
        :rtype: str
        """
        return self._value_type

    @value_type.setter
    def value_type(self, value_type):
        """
        Sets the value_type of this Condition.
        Determines the type of the value associated with the condition

        :param value_type: The value_type of this Condition.
        :type: str
        """
        allowed_values = ["STRING", "NUMERIC", "DATETIME", "PERIOD"]
        if value_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for value_type -> " + value_type
            self._value_type = "outdated_sdk_version"
        else:
            self._value_type = value_type.lower()

    @property
    def operator(self):
        """
        Gets the operator of this Condition.
        An operation type for condition evaluation

        :return: The operator of this Condition.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """
        Sets the operator of this Condition.
        An operation type for condition evaluation

        :param operator: The operator of this Condition.
        :type: str
        """
        allowed_values = ["EQUALS", "LESS_THAN", "LESS_THAN_EQUALS", "GREATER_THAN", "GREATER_THAN_EQUALS", "CONTAINS", "BEGINS_WITH", "ENDS_WITH", "BEFORE", "AFTER"]
        if operator.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for operator -> " + operator
            self._operator = "outdated_sdk_version"
        else:
            self._operator = operator.lower()

    @property
    def codes(self):
        """
        Gets the codes of this Condition.
        List of wrap-up code identifiers (used only in conditions of type 'wrapupCondition')

        :return: The codes of this Condition.
        :rtype: list[str]
        """
        return self._codes

    @codes.setter
    def codes(self, codes):
        """
        Sets the codes of this Condition.
        List of wrap-up code identifiers (used only in conditions of type 'wrapupCondition')

        :param codes: The codes of this Condition.
        :type: list[str]
        """
        
        self._codes = codes

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

