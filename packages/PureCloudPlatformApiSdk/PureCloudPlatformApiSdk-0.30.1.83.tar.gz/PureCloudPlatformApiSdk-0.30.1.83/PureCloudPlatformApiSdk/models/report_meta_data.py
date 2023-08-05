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


class ReportMetaData(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ReportMetaData - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'title': 'str',
            'description': 'str',
            'keywords': 'list[str]',
            'available_locales': 'list[str]',
            'parameters': 'list[Parameter]',
            'example_url': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'title': 'title',
            'description': 'description',
            'keywords': 'keywords',
            'available_locales': 'availableLocales',
            'parameters': 'parameters',
            'example_url': 'exampleUrl',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._title = None
        self._description = None
        self._keywords = None
        self._available_locales = None
        self._parameters = None
        self._example_url = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ReportMetaData.
        The globally unique identifier for the object.

        :return: The id of this ReportMetaData.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ReportMetaData.
        The globally unique identifier for the object.

        :param id: The id of this ReportMetaData.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ReportMetaData.


        :return: The name of this ReportMetaData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ReportMetaData.


        :param name: The name of this ReportMetaData.
        :type: str
        """
        
        self._name = name

    @property
    def title(self):
        """
        Gets the title of this ReportMetaData.


        :return: The title of this ReportMetaData.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this ReportMetaData.


        :param title: The title of this ReportMetaData.
        :type: str
        """
        
        self._title = title

    @property
    def description(self):
        """
        Gets the description of this ReportMetaData.


        :return: The description of this ReportMetaData.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ReportMetaData.


        :param description: The description of this ReportMetaData.
        :type: str
        """
        
        self._description = description

    @property
    def keywords(self):
        """
        Gets the keywords of this ReportMetaData.


        :return: The keywords of this ReportMetaData.
        :rtype: list[str]
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """
        Sets the keywords of this ReportMetaData.


        :param keywords: The keywords of this ReportMetaData.
        :type: list[str]
        """
        
        self._keywords = keywords

    @property
    def available_locales(self):
        """
        Gets the available_locales of this ReportMetaData.


        :return: The available_locales of this ReportMetaData.
        :rtype: list[str]
        """
        return self._available_locales

    @available_locales.setter
    def available_locales(self, available_locales):
        """
        Sets the available_locales of this ReportMetaData.


        :param available_locales: The available_locales of this ReportMetaData.
        :type: list[str]
        """
        
        self._available_locales = available_locales

    @property
    def parameters(self):
        """
        Gets the parameters of this ReportMetaData.


        :return: The parameters of this ReportMetaData.
        :rtype: list[Parameter]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this ReportMetaData.


        :param parameters: The parameters of this ReportMetaData.
        :type: list[Parameter]
        """
        
        self._parameters = parameters

    @property
    def example_url(self):
        """
        Gets the example_url of this ReportMetaData.


        :return: The example_url of this ReportMetaData.
        :rtype: str
        """
        return self._example_url

    @example_url.setter
    def example_url(self, example_url):
        """
        Sets the example_url of this ReportMetaData.


        :param example_url: The example_url of this ReportMetaData.
        :type: str
        """
        
        self._example_url = example_url

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ReportMetaData.
        The URI for this object

        :return: The self_uri of this ReportMetaData.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ReportMetaData.
        The URI for this object

        :param self_uri: The self_uri of this ReportMetaData.
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

