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


class OrganizationPresence(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        OrganizationPresence - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'language_labels': 'dict(str, str)',
            'system_presence': 'str',
            'deactivated': 'bool',
            'primary': 'bool',
            'created_by': 'User',
            'created_date': 'datetime',
            'modified_by': 'User',
            'modified_date': 'datetime',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'language_labels': 'languageLabels',
            'system_presence': 'systemPresence',
            'deactivated': 'deactivated',
            'primary': 'primary',
            'created_by': 'createdBy',
            'created_date': 'createdDate',
            'modified_by': 'modifiedBy',
            'modified_date': 'modifiedDate',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._language_labels = None
        self._system_presence = None
        self._deactivated = False
        self._primary = False
        self._created_by = None
        self._created_date = None
        self._modified_by = None
        self._modified_date = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this OrganizationPresence.
        The globally unique identifier for the object.

        :return: The id of this OrganizationPresence.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this OrganizationPresence.
        The globally unique identifier for the object.

        :param id: The id of this OrganizationPresence.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this OrganizationPresence.


        :return: The name of this OrganizationPresence.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this OrganizationPresence.


        :param name: The name of this OrganizationPresence.
        :type: str
        """
        
        self._name = name

    @property
    def language_labels(self):
        """
        Gets the language_labels of this OrganizationPresence.
        The label used for the system presence in each specified language

        :return: The language_labels of this OrganizationPresence.
        :rtype: dict(str, str)
        """
        return self._language_labels

    @language_labels.setter
    def language_labels(self, language_labels):
        """
        Sets the language_labels of this OrganizationPresence.
        The label used for the system presence in each specified language

        :param language_labels: The language_labels of this OrganizationPresence.
        :type: dict(str, str)
        """
        
        self._language_labels = language_labels

    @property
    def system_presence(self):
        """
        Gets the system_presence of this OrganizationPresence.


        :return: The system_presence of this OrganizationPresence.
        :rtype: str
        """
        return self._system_presence

    @system_presence.setter
    def system_presence(self, system_presence):
        """
        Sets the system_presence of this OrganizationPresence.


        :param system_presence: The system_presence of this OrganizationPresence.
        :type: str
        """
        
        self._system_presence = system_presence

    @property
    def deactivated(self):
        """
        Gets the deactivated of this OrganizationPresence.


        :return: The deactivated of this OrganizationPresence.
        :rtype: bool
        """
        return self._deactivated

    @deactivated.setter
    def deactivated(self, deactivated):
        """
        Sets the deactivated of this OrganizationPresence.


        :param deactivated: The deactivated of this OrganizationPresence.
        :type: bool
        """
        
        self._deactivated = deactivated

    @property
    def primary(self):
        """
        Gets the primary of this OrganizationPresence.


        :return: The primary of this OrganizationPresence.
        :rtype: bool
        """
        return self._primary

    @primary.setter
    def primary(self, primary):
        """
        Sets the primary of this OrganizationPresence.


        :param primary: The primary of this OrganizationPresence.
        :type: bool
        """
        
        self._primary = primary

    @property
    def created_by(self):
        """
        Gets the created_by of this OrganizationPresence.


        :return: The created_by of this OrganizationPresence.
        :rtype: User
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this OrganizationPresence.


        :param created_by: The created_by of this OrganizationPresence.
        :type: User
        """
        
        self._created_by = created_by

    @property
    def created_date(self):
        """
        Gets the created_date of this OrganizationPresence.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The created_date of this OrganizationPresence.
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """
        Sets the created_date of this OrganizationPresence.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param created_date: The created_date of this OrganizationPresence.
        :type: datetime
        """
        
        self._created_date = created_date

    @property
    def modified_by(self):
        """
        Gets the modified_by of this OrganizationPresence.


        :return: The modified_by of this OrganizationPresence.
        :rtype: User
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this OrganizationPresence.


        :param modified_by: The modified_by of this OrganizationPresence.
        :type: User
        """
        
        self._modified_by = modified_by

    @property
    def modified_date(self):
        """
        Gets the modified_date of this OrganizationPresence.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The modified_date of this OrganizationPresence.
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """
        Sets the modified_date of this OrganizationPresence.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param modified_date: The modified_date of this OrganizationPresence.
        :type: datetime
        """
        
        self._modified_date = modified_date

    @property
    def self_uri(self):
        """
        Gets the self_uri of this OrganizationPresence.
        The URI for this object

        :return: The self_uri of this OrganizationPresence.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this OrganizationPresence.
        The URI for this object

        :param self_uri: The self_uri of this OrganizationPresence.
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

