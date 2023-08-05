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


class CreateQueueRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CreateQueueRequest - a model defined in Swagger

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
            'media_settings': 'dict(str, MediaSetting)',
            'bullseye': 'Bullseye',
            'acw_settings': 'AcwSettings',
            'skill_evaluation_method': 'str',
            'queue_flow': 'UriReference',
            'calling_party_name': 'str',
            'calling_party_number': 'str',
            'source_queue_id': 'str',
            'member_count': 'int',
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
            'media_settings': 'mediaSettings',
            'bullseye': 'bullseye',
            'acw_settings': 'acwSettings',
            'skill_evaluation_method': 'skillEvaluationMethod',
            'queue_flow': 'queueFlow',
            'calling_party_name': 'callingPartyName',
            'calling_party_number': 'callingPartyNumber',
            'source_queue_id': 'sourceQueueId',
            'member_count': 'memberCount',
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
        self._media_settings = None
        self._bullseye = None
        self._acw_settings = None
        self._skill_evaluation_method = None
        self._queue_flow = None
        self._calling_party_name = None
        self._calling_party_number = None
        self._source_queue_id = None
        self._member_count = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this CreateQueueRequest.
        The globally unique identifier for the object.

        :return: The id of this CreateQueueRequest.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CreateQueueRequest.
        The globally unique identifier for the object.

        :param id: The id of this CreateQueueRequest.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this CreateQueueRequest.


        :return: The name of this CreateQueueRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateQueueRequest.


        :param name: The name of this CreateQueueRequest.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this CreateQueueRequest.


        :return: The description of this CreateQueueRequest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateQueueRequest.


        :param description: The description of this CreateQueueRequest.
        :type: str
        """
        
        self._description = description

    @property
    def version(self):
        """
        Gets the version of this CreateQueueRequest.


        :return: The version of this CreateQueueRequest.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this CreateQueueRequest.


        :param version: The version of this CreateQueueRequest.
        :type: int
        """
        
        self._version = version

    @property
    def date_created(self):
        """
        Gets the date_created of this CreateQueueRequest.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this CreateQueueRequest.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this CreateQueueRequest.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this CreateQueueRequest.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this CreateQueueRequest.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this CreateQueueRequest.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this CreateQueueRequest.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this CreateQueueRequest.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def modified_by(self):
        """
        Gets the modified_by of this CreateQueueRequest.


        :return: The modified_by of this CreateQueueRequest.
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this CreateQueueRequest.


        :param modified_by: The modified_by of this CreateQueueRequest.
        :type: str
        """
        
        self._modified_by = modified_by

    @property
    def created_by(self):
        """
        Gets the created_by of this CreateQueueRequest.


        :return: The created_by of this CreateQueueRequest.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this CreateQueueRequest.


        :param created_by: The created_by of this CreateQueueRequest.
        :type: str
        """
        
        self._created_by = created_by

    @property
    def state(self):
        """
        Gets the state of this CreateQueueRequest.


        :return: The state of this CreateQueueRequest.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this CreateQueueRequest.


        :param state: The state of this CreateQueueRequest.
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
        Gets the modified_by_app of this CreateQueueRequest.


        :return: The modified_by_app of this CreateQueueRequest.
        :rtype: str
        """
        return self._modified_by_app

    @modified_by_app.setter
    def modified_by_app(self, modified_by_app):
        """
        Sets the modified_by_app of this CreateQueueRequest.


        :param modified_by_app: The modified_by_app of this CreateQueueRequest.
        :type: str
        """
        
        self._modified_by_app = modified_by_app

    @property
    def created_by_app(self):
        """
        Gets the created_by_app of this CreateQueueRequest.


        :return: The created_by_app of this CreateQueueRequest.
        :rtype: str
        """
        return self._created_by_app

    @created_by_app.setter
    def created_by_app(self, created_by_app):
        """
        Sets the created_by_app of this CreateQueueRequest.


        :param created_by_app: The created_by_app of this CreateQueueRequest.
        :type: str
        """
        
        self._created_by_app = created_by_app

    @property
    def media_settings(self):
        """
        Gets the media_settings of this CreateQueueRequest.
        The media settings for the queue.

        :return: The media_settings of this CreateQueueRequest.
        :rtype: dict(str, MediaSetting)
        """
        return self._media_settings

    @media_settings.setter
    def media_settings(self, media_settings):
        """
        Sets the media_settings of this CreateQueueRequest.
        The media settings for the queue.

        :param media_settings: The media_settings of this CreateQueueRequest.
        :type: dict(str, MediaSetting)
        """
        
        self._media_settings = media_settings

    @property
    def bullseye(self):
        """
        Gets the bullseye of this CreateQueueRequest.
        The bulls-eye settings for the queue.

        :return: The bullseye of this CreateQueueRequest.
        :rtype: Bullseye
        """
        return self._bullseye

    @bullseye.setter
    def bullseye(self, bullseye):
        """
        Sets the bullseye of this CreateQueueRequest.
        The bulls-eye settings for the queue.

        :param bullseye: The bullseye of this CreateQueueRequest.
        :type: Bullseye
        """
        
        self._bullseye = bullseye

    @property
    def acw_settings(self):
        """
        Gets the acw_settings of this CreateQueueRequest.
        The ACW settings for the queue.

        :return: The acw_settings of this CreateQueueRequest.
        :rtype: AcwSettings
        """
        return self._acw_settings

    @acw_settings.setter
    def acw_settings(self, acw_settings):
        """
        Sets the acw_settings of this CreateQueueRequest.
        The ACW settings for the queue.

        :param acw_settings: The acw_settings of this CreateQueueRequest.
        :type: AcwSettings
        """
        
        self._acw_settings = acw_settings

    @property
    def skill_evaluation_method(self):
        """
        Gets the skill_evaluation_method of this CreateQueueRequest.
        The skill evaluation method to use when routing conversations.

        :return: The skill_evaluation_method of this CreateQueueRequest.
        :rtype: str
        """
        return self._skill_evaluation_method

    @skill_evaluation_method.setter
    def skill_evaluation_method(self, skill_evaluation_method):
        """
        Sets the skill_evaluation_method of this CreateQueueRequest.
        The skill evaluation method to use when routing conversations.

        :param skill_evaluation_method: The skill_evaluation_method of this CreateQueueRequest.
        :type: str
        """
        allowed_values = ["NONE", "BEST", "ALL"]
        if skill_evaluation_method.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for skill_evaluation_method -> " + skill_evaluation_method
            self._skill_evaluation_method = "outdated_sdk_version"
        else:
            self._skill_evaluation_method = skill_evaluation_method.lower()

    @property
    def queue_flow(self):
        """
        Gets the queue_flow of this CreateQueueRequest.
        The in-queue flow to use for conversations waiting in queue.

        :return: The queue_flow of this CreateQueueRequest.
        :rtype: UriReference
        """
        return self._queue_flow

    @queue_flow.setter
    def queue_flow(self, queue_flow):
        """
        Sets the queue_flow of this CreateQueueRequest.
        The in-queue flow to use for conversations waiting in queue.

        :param queue_flow: The queue_flow of this CreateQueueRequest.
        :type: UriReference
        """
        
        self._queue_flow = queue_flow

    @property
    def calling_party_name(self):
        """
        Gets the calling_party_name of this CreateQueueRequest.
        The name to use for caller identification for outbound calls from this queue.

        :return: The calling_party_name of this CreateQueueRequest.
        :rtype: str
        """
        return self._calling_party_name

    @calling_party_name.setter
    def calling_party_name(self, calling_party_name):
        """
        Sets the calling_party_name of this CreateQueueRequest.
        The name to use for caller identification for outbound calls from this queue.

        :param calling_party_name: The calling_party_name of this CreateQueueRequest.
        :type: str
        """
        
        self._calling_party_name = calling_party_name

    @property
    def calling_party_number(self):
        """
        Gets the calling_party_number of this CreateQueueRequest.
        The phone number to use for caller identification for outbound calls from this queue.

        :return: The calling_party_number of this CreateQueueRequest.
        :rtype: str
        """
        return self._calling_party_number

    @calling_party_number.setter
    def calling_party_number(self, calling_party_number):
        """
        Sets the calling_party_number of this CreateQueueRequest.
        The phone number to use for caller identification for outbound calls from this queue.

        :param calling_party_number: The calling_party_number of this CreateQueueRequest.
        :type: str
        """
        
        self._calling_party_number = calling_party_number

    @property
    def source_queue_id(self):
        """
        Gets the source_queue_id of this CreateQueueRequest.
        The id of an existing queue to copy the settings from when creating a new queue.

        :return: The source_queue_id of this CreateQueueRequest.
        :rtype: str
        """
        return self._source_queue_id

    @source_queue_id.setter
    def source_queue_id(self, source_queue_id):
        """
        Sets the source_queue_id of this CreateQueueRequest.
        The id of an existing queue to copy the settings from when creating a new queue.

        :param source_queue_id: The source_queue_id of this CreateQueueRequest.
        :type: str
        """
        
        self._source_queue_id = source_queue_id

    @property
    def member_count(self):
        """
        Gets the member_count of this CreateQueueRequest.


        :return: The member_count of this CreateQueueRequest.
        :rtype: int
        """
        return self._member_count

    @member_count.setter
    def member_count(self, member_count):
        """
        Sets the member_count of this CreateQueueRequest.


        :param member_count: The member_count of this CreateQueueRequest.
        :type: int
        """
        
        self._member_count = member_count

    @property
    def self_uri(self):
        """
        Gets the self_uri of this CreateQueueRequest.
        The URI for this object

        :return: The self_uri of this CreateQueueRequest.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this CreateQueueRequest.
        The URI for this object

        :param self_uri: The self_uri of this CreateQueueRequest.
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

