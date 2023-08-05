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


class DocumentAudit(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DocumentAudit - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'user': 'UriReference',
            'workspace': 'UriReference',
            'transaction_id': 'str',
            'transaction_initiator': 'bool',
            'application': 'str',
            'service_name': 'str',
            'level': 'str',
            'timestamp': 'datetime',
            'status': 'str',
            'action_context': 'str',
            'action': 'str',
            'entity': 'AuditEntityReference',
            'changes': 'list[AuditChange]',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'user': 'user',
            'workspace': 'workspace',
            'transaction_id': 'transactionId',
            'transaction_initiator': 'transactionInitiator',
            'application': 'application',
            'service_name': 'serviceName',
            'level': 'level',
            'timestamp': 'timestamp',
            'status': 'status',
            'action_context': 'actionContext',
            'action': 'action',
            'entity': 'entity',
            'changes': 'changes',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._user = None
        self._workspace = None
        self._transaction_id = None
        self._transaction_initiator = False
        self._application = None
        self._service_name = None
        self._level = None
        self._timestamp = None
        self._status = None
        self._action_context = None
        self._action = None
        self._entity = None
        self._changes = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this DocumentAudit.
        The globally unique identifier for the object.

        :return: The id of this DocumentAudit.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DocumentAudit.
        The globally unique identifier for the object.

        :param id: The id of this DocumentAudit.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this DocumentAudit.


        :return: The name of this DocumentAudit.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DocumentAudit.


        :param name: The name of this DocumentAudit.
        :type: str
        """
        
        self._name = name

    @property
    def user(self):
        """
        Gets the user of this DocumentAudit.


        :return: The user of this DocumentAudit.
        :rtype: UriReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this DocumentAudit.


        :param user: The user of this DocumentAudit.
        :type: UriReference
        """
        
        self._user = user

    @property
    def workspace(self):
        """
        Gets the workspace of this DocumentAudit.


        :return: The workspace of this DocumentAudit.
        :rtype: UriReference
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """
        Sets the workspace of this DocumentAudit.


        :param workspace: The workspace of this DocumentAudit.
        :type: UriReference
        """
        
        self._workspace = workspace

    @property
    def transaction_id(self):
        """
        Gets the transaction_id of this DocumentAudit.


        :return: The transaction_id of this DocumentAudit.
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """
        Sets the transaction_id of this DocumentAudit.


        :param transaction_id: The transaction_id of this DocumentAudit.
        :type: str
        """
        
        self._transaction_id = transaction_id

    @property
    def transaction_initiator(self):
        """
        Gets the transaction_initiator of this DocumentAudit.


        :return: The transaction_initiator of this DocumentAudit.
        :rtype: bool
        """
        return self._transaction_initiator

    @transaction_initiator.setter
    def transaction_initiator(self, transaction_initiator):
        """
        Sets the transaction_initiator of this DocumentAudit.


        :param transaction_initiator: The transaction_initiator of this DocumentAudit.
        :type: bool
        """
        
        self._transaction_initiator = transaction_initiator

    @property
    def application(self):
        """
        Gets the application of this DocumentAudit.


        :return: The application of this DocumentAudit.
        :rtype: str
        """
        return self._application

    @application.setter
    def application(self, application):
        """
        Sets the application of this DocumentAudit.


        :param application: The application of this DocumentAudit.
        :type: str
        """
        
        self._application = application

    @property
    def service_name(self):
        """
        Gets the service_name of this DocumentAudit.


        :return: The service_name of this DocumentAudit.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Sets the service_name of this DocumentAudit.


        :param service_name: The service_name of this DocumentAudit.
        :type: str
        """
        
        self._service_name = service_name

    @property
    def level(self):
        """
        Gets the level of this DocumentAudit.


        :return: The level of this DocumentAudit.
        :rtype: str
        """
        return self._level

    @level.setter
    def level(self, level):
        """
        Sets the level of this DocumentAudit.


        :param level: The level of this DocumentAudit.
        :type: str
        """
        allowed_values = ["USER", "SYSTEM"]
        if level not in allowed_values:
            raise ValueError(
                "Invalid value for `level`, must be one of {0}"
                .format(allowed_values)
            )

        self._level = level

    @property
    def timestamp(self):
        """
        Gets the timestamp of this DocumentAudit.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The timestamp of this DocumentAudit.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this DocumentAudit.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param timestamp: The timestamp of this DocumentAudit.
        :type: datetime
        """
        
        self._timestamp = timestamp

    @property
    def status(self):
        """
        Gets the status of this DocumentAudit.


        :return: The status of this DocumentAudit.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this DocumentAudit.


        :param status: The status of this DocumentAudit.
        :type: str
        """
        allowed_values = ["SUCCESS", "FAILURE"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status`, must be one of {0}"
                .format(allowed_values)
            )

        self._status = status

    @property
    def action_context(self):
        """
        Gets the action_context of this DocumentAudit.


        :return: The action_context of this DocumentAudit.
        :rtype: str
        """
        return self._action_context

    @action_context.setter
    def action_context(self, action_context):
        """
        Sets the action_context of this DocumentAudit.


        :param action_context: The action_context of this DocumentAudit.
        :type: str
        """
        allowed_values = ["CREATE", "READ", "UPDATE", "DELETE", "DOWNLOAD", "VIEW", "UPLOAD", "SAVE", "MOVE", "COPY", "ADD", "REMOVE", "RECEIVE", "CONVERT", "FAX", "CREATE_COVERPAGE", "USER_ADD", "USER_REMOVE", "MEMBER_ADD", "MEMBER_REMOVE", "MEMBER_UPDATE", "TAG_ADD", "TAG_REMOVE", "TAG_UPDATE", "ATTRIBUTE_ADD", "ATTRIBUTE_REMOVE", "ATTRIBUTE_UPDATE", "ATTRIBUTE_GROUP_INSTANCE_ADD", "ATTRIBUTE_GROUP_INSTANCE_REMOVE", "ATTRIBUTE_GROUP_INSTANCE_UPDATE", "INDEX_SAVE", "INDEX_DELETE", "INDEX_CREATE", "FILE_SAVE", "FILE_DELETE", "FILE_READ", "THUMBNAIL_CREATE", "TEXT_EXTRACT", "SHARE_ADD", "SHARE_REMOVE", "VERSION_CREATE"]
        if action_context not in allowed_values:
            raise ValueError(
                "Invalid value for `action_context`, must be one of {0}"
                .format(allowed_values)
            )

        self._action_context = action_context

    @property
    def action(self):
        """
        Gets the action of this DocumentAudit.


        :return: The action of this DocumentAudit.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this DocumentAudit.


        :param action: The action of this DocumentAudit.
        :type: str
        """
        allowed_values = ["CREATE", "READ", "UPDATE", "DELETE", "DOWNLOAD", "VIEW", "UPLOAD", "SAVE", "MOVE", "COPY", "ADD", "REMOVE", "RECEIVE", "CONVERT", "FAX", "CREATE_COVERPAGE", "USER_ADD", "USER_REMOVE", "MEMBER_ADD", "MEMBER_REMOVE", "MEMBER_UPDATE", "TAG_ADD", "TAG_REMOVE", "TAG_UPDATE", "ATTRIBUTE_ADD", "ATTRIBUTE_REMOVE", "ATTRIBUTE_UPDATE", "ATTRIBUTE_GROUP_INSTANCE_ADD", "ATTRIBUTE_GROUP_INSTANCE_REMOVE", "ATTRIBUTE_GROUP_INSTANCE_UPDATE", "INDEX_SAVE", "INDEX_DELETE", "INDEX_CREATE", "FILE_SAVE", "FILE_DELETE", "FILE_READ", "THUMBNAIL_CREATE", "TEXT_EXTRACT", "SHARE_ADD", "SHARE_REMOVE", "VERSION_CREATE"]
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action`, must be one of {0}"
                .format(allowed_values)
            )

        self._action = action

    @property
    def entity(self):
        """
        Gets the entity of this DocumentAudit.


        :return: The entity of this DocumentAudit.
        :rtype: AuditEntityReference
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """
        Sets the entity of this DocumentAudit.


        :param entity: The entity of this DocumentAudit.
        :type: AuditEntityReference
        """
        
        self._entity = entity

    @property
    def changes(self):
        """
        Gets the changes of this DocumentAudit.


        :return: The changes of this DocumentAudit.
        :rtype: list[AuditChange]
        """
        return self._changes

    @changes.setter
    def changes(self, changes):
        """
        Sets the changes of this DocumentAudit.


        :param changes: The changes of this DocumentAudit.
        :type: list[AuditChange]
        """
        
        self._changes = changes

    @property
    def self_uri(self):
        """
        Gets the self_uri of this DocumentAudit.
        The URI for this object

        :return: The self_uri of this DocumentAudit.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this DocumentAudit.
        The URI for this object

        :param self_uri: The self_uri of this DocumentAudit.
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

