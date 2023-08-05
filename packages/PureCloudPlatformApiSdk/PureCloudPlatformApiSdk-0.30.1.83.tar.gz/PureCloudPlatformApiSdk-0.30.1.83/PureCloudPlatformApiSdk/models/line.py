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


class Line(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Line - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'version': 'int',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'modified_by': 'str',
            'created_by': 'str',
            'state': 'str',
            'modified_by_app': 'str',
            'created_by_app': 'str',
            'properties': 'dict(str, object)',
            'edge_group': 'UriReference',
            'template': 'UriReference',
            'site': 'UriReference',
            'line_base_settings': 'UriReference',
            'primary_edge': 'Edge',
            'secondary_edge': 'Edge',
            'logged_in_user': 'UriReference',
            'default_for_user': 'UriReference',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'version': 'version',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'modified_by': 'modifiedBy',
            'created_by': 'createdBy',
            'state': 'state',
            'modified_by_app': 'modifiedByApp',
            'created_by_app': 'createdByApp',
            'properties': 'properties',
            'edge_group': 'edgeGroup',
            'template': 'template',
            'site': 'site',
            'line_base_settings': 'lineBaseSettings',
            'primary_edge': 'primaryEdge',
            'secondary_edge': 'secondaryEdge',
            'logged_in_user': 'loggedInUser',
            'default_for_user': 'defaultForUser',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._version = None
        self._date_created = None
        self._date_modified = None
        self._modified_by = None
        self._created_by = None
        self._state = None
        self._modified_by_app = None
        self._created_by_app = None
        self._properties = None
        self._edge_group = None
        self._template = None
        self._site = None
        self._line_base_settings = None
        self._primary_edge = None
        self._secondary_edge = None
        self._logged_in_user = None
        self._default_for_user = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Line.
        The globally unique identifier for the object.

        :return: The id of this Line.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Line.
        The globally unique identifier for the object.

        :param id: The id of this Line.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Line.
        The name of the entity.

        :return: The name of this Line.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Line.
        The name of the entity.

        :param name: The name of this Line.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this Line.


        :return: The description of this Line.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Line.


        :param description: The description of this Line.
        :type: str
        """
        
        self._description = description

    @property
    def version(self):
        """
        Gets the version of this Line.


        :return: The version of this Line.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this Line.


        :param version: The version of this Line.
        :type: int
        """
        
        self._version = version

    @property
    def date_created(self):
        """
        Gets the date_created of this Line.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this Line.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this Line.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this Line.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this Line.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this Line.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this Line.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this Line.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def modified_by(self):
        """
        Gets the modified_by of this Line.


        :return: The modified_by of this Line.
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this Line.


        :param modified_by: The modified_by of this Line.
        :type: str
        """
        
        self._modified_by = modified_by

    @property
    def created_by(self):
        """
        Gets the created_by of this Line.


        :return: The created_by of this Line.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this Line.


        :param created_by: The created_by of this Line.
        :type: str
        """
        
        self._created_by = created_by

    @property
    def state(self):
        """
        Gets the state of this Line.


        :return: The state of this Line.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Line.


        :param state: The state of this Line.
        :type: str
        """
        allowed_values = ["active", "inactive", "deleted"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state.lower()

    @property
    def modified_by_app(self):
        """
        Gets the modified_by_app of this Line.


        :return: The modified_by_app of this Line.
        :rtype: str
        """
        return self._modified_by_app

    @modified_by_app.setter
    def modified_by_app(self, modified_by_app):
        """
        Sets the modified_by_app of this Line.


        :param modified_by_app: The modified_by_app of this Line.
        :type: str
        """
        
        self._modified_by_app = modified_by_app

    @property
    def created_by_app(self):
        """
        Gets the created_by_app of this Line.


        :return: The created_by_app of this Line.
        :rtype: str
        """
        return self._created_by_app

    @created_by_app.setter
    def created_by_app(self, created_by_app):
        """
        Sets the created_by_app of this Line.


        :param created_by_app: The created_by_app of this Line.
        :type: str
        """
        
        self._created_by_app = created_by_app

    @property
    def properties(self):
        """
        Gets the properties of this Line.


        :return: The properties of this Line.
        :rtype: dict(str, object)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this Line.


        :param properties: The properties of this Line.
        :type: dict(str, object)
        """
        
        self._properties = properties

    @property
    def edge_group(self):
        """
        Gets the edge_group of this Line.


        :return: The edge_group of this Line.
        :rtype: UriReference
        """
        return self._edge_group

    @edge_group.setter
    def edge_group(self, edge_group):
        """
        Sets the edge_group of this Line.


        :param edge_group: The edge_group of this Line.
        :type: UriReference
        """
        
        self._edge_group = edge_group

    @property
    def template(self):
        """
        Gets the template of this Line.


        :return: The template of this Line.
        :rtype: UriReference
        """
        return self._template

    @template.setter
    def template(self, template):
        """
        Sets the template of this Line.


        :param template: The template of this Line.
        :type: UriReference
        """
        
        self._template = template

    @property
    def site(self):
        """
        Gets the site of this Line.


        :return: The site of this Line.
        :rtype: UriReference
        """
        return self._site

    @site.setter
    def site(self, site):
        """
        Sets the site of this Line.


        :param site: The site of this Line.
        :type: UriReference
        """
        
        self._site = site

    @property
    def line_base_settings(self):
        """
        Gets the line_base_settings of this Line.


        :return: The line_base_settings of this Line.
        :rtype: UriReference
        """
        return self._line_base_settings

    @line_base_settings.setter
    def line_base_settings(self, line_base_settings):
        """
        Sets the line_base_settings of this Line.


        :param line_base_settings: The line_base_settings of this Line.
        :type: UriReference
        """
        
        self._line_base_settings = line_base_settings

    @property
    def primary_edge(self):
        """
        Gets the primary_edge of this Line.


        :return: The primary_edge of this Line.
        :rtype: Edge
        """
        return self._primary_edge

    @primary_edge.setter
    def primary_edge(self, primary_edge):
        """
        Sets the primary_edge of this Line.


        :param primary_edge: The primary_edge of this Line.
        :type: Edge
        """
        
        self._primary_edge = primary_edge

    @property
    def secondary_edge(self):
        """
        Gets the secondary_edge of this Line.


        :return: The secondary_edge of this Line.
        :rtype: Edge
        """
        return self._secondary_edge

    @secondary_edge.setter
    def secondary_edge(self, secondary_edge):
        """
        Sets the secondary_edge of this Line.


        :param secondary_edge: The secondary_edge of this Line.
        :type: Edge
        """
        
        self._secondary_edge = secondary_edge

    @property
    def logged_in_user(self):
        """
        Gets the logged_in_user of this Line.


        :return: The logged_in_user of this Line.
        :rtype: UriReference
        """
        return self._logged_in_user

    @logged_in_user.setter
    def logged_in_user(self, logged_in_user):
        """
        Sets the logged_in_user of this Line.


        :param logged_in_user: The logged_in_user of this Line.
        :type: UriReference
        """
        
        self._logged_in_user = logged_in_user

    @property
    def default_for_user(self):
        """
        Gets the default_for_user of this Line.


        :return: The default_for_user of this Line.
        :rtype: UriReference
        """
        return self._default_for_user

    @default_for_user.setter
    def default_for_user(self, default_for_user):
        """
        Sets the default_for_user of this Line.


        :param default_for_user: The default_for_user of this Line.
        :type: UriReference
        """
        
        self._default_for_user = default_for_user

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Line.
        The URI for this object

        :return: The self_uri of this Line.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Line.
        The URI for this object

        :param self_uri: The self_uri of this Line.
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

