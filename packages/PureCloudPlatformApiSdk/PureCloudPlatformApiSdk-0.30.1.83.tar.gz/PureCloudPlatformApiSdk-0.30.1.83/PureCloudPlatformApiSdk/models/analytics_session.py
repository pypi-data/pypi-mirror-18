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


class AnalyticsSession(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AnalyticsSession - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'media_type': 'str',
            'session_id': 'str',
            'address_other': 'str',
            'address_self': 'str',
            'ani': 'str',
            'direction': 'str',
            'dnis': 'str',
            'outbound_campaign_id': 'str',
            'outbound_contact_id': 'str',
            'outbound_contact_list_id': 'str',
            'disposition_analyzer': 'str',
            'disposition_name': 'str',
            'edge_id': 'str',
            'remote_name_displayable': 'str',
            'room_id': 'str',
            'monitored_session_id': 'str',
            'monitored_participant_id': 'str',
            'callback_user_name': 'str',
            'callback_numbers': 'list[str]',
            'callback_scheduled_time': 'datetime',
            'script_id': 'str',
            'skip_enabled': 'bool',
            'timeout_seconds': 'int',
            'segments': 'list[AnalyticsConversationSegment]'
        }

        self.attribute_map = {
            'media_type': 'mediaType',
            'session_id': 'sessionId',
            'address_other': 'addressOther',
            'address_self': 'addressSelf',
            'ani': 'ani',
            'direction': 'direction',
            'dnis': 'dnis',
            'outbound_campaign_id': 'outboundCampaignId',
            'outbound_contact_id': 'outboundContactId',
            'outbound_contact_list_id': 'outboundContactListId',
            'disposition_analyzer': 'dispositionAnalyzer',
            'disposition_name': 'dispositionName',
            'edge_id': 'edgeId',
            'remote_name_displayable': 'remoteNameDisplayable',
            'room_id': 'roomId',
            'monitored_session_id': 'monitoredSessionId',
            'monitored_participant_id': 'monitoredParticipantId',
            'callback_user_name': 'callbackUserName',
            'callback_numbers': 'callbackNumbers',
            'callback_scheduled_time': 'callbackScheduledTime',
            'script_id': 'scriptId',
            'skip_enabled': 'skipEnabled',
            'timeout_seconds': 'timeoutSeconds',
            'segments': 'segments'
        }

        self._media_type = None
        self._session_id = None
        self._address_other = None
        self._address_self = None
        self._ani = None
        self._direction = None
        self._dnis = None
        self._outbound_campaign_id = None
        self._outbound_contact_id = None
        self._outbound_contact_list_id = None
        self._disposition_analyzer = None
        self._disposition_name = None
        self._edge_id = None
        self._remote_name_displayable = None
        self._room_id = None
        self._monitored_session_id = None
        self._monitored_participant_id = None
        self._callback_user_name = None
        self._callback_numbers = None
        self._callback_scheduled_time = None
        self._script_id = None
        self._skip_enabled = False
        self._timeout_seconds = None
        self._segments = None

    @property
    def media_type(self):
        """
        Gets the media_type of this AnalyticsSession.


        :return: The media_type of this AnalyticsSession.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this AnalyticsSession.


        :param media_type: The media_type of this AnalyticsSession.
        :type: str
        """
        allowed_values = ["voice", "chat", "email", "callback", "cobrowse", "video", "screenShare"]
        if media_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for media_type -> " + media_type
            self._media_type = "outdated_sdk_version"
        else:
            self._media_type = media_type.lower()

    @property
    def session_id(self):
        """
        Gets the session_id of this AnalyticsSession.


        :return: The session_id of this AnalyticsSession.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """
        Sets the session_id of this AnalyticsSession.


        :param session_id: The session_id of this AnalyticsSession.
        :type: str
        """
        
        self._session_id = session_id

    @property
    def address_other(self):
        """
        Gets the address_other of this AnalyticsSession.


        :return: The address_other of this AnalyticsSession.
        :rtype: str
        """
        return self._address_other

    @address_other.setter
    def address_other(self, address_other):
        """
        Sets the address_other of this AnalyticsSession.


        :param address_other: The address_other of this AnalyticsSession.
        :type: str
        """
        
        self._address_other = address_other

    @property
    def address_self(self):
        """
        Gets the address_self of this AnalyticsSession.


        :return: The address_self of this AnalyticsSession.
        :rtype: str
        """
        return self._address_self

    @address_self.setter
    def address_self(self, address_self):
        """
        Sets the address_self of this AnalyticsSession.


        :param address_self: The address_self of this AnalyticsSession.
        :type: str
        """
        
        self._address_self = address_self

    @property
    def ani(self):
        """
        Gets the ani of this AnalyticsSession.


        :return: The ani of this AnalyticsSession.
        :rtype: str
        """
        return self._ani

    @ani.setter
    def ani(self, ani):
        """
        Sets the ani of this AnalyticsSession.


        :param ani: The ani of this AnalyticsSession.
        :type: str
        """
        
        self._ani = ani

    @property
    def direction(self):
        """
        Gets the direction of this AnalyticsSession.


        :return: The direction of this AnalyticsSession.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this AnalyticsSession.


        :param direction: The direction of this AnalyticsSession.
        :type: str
        """
        allowed_values = ["inbound", "outbound"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for direction -> " + direction
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction.lower()

    @property
    def dnis(self):
        """
        Gets the dnis of this AnalyticsSession.


        :return: The dnis of this AnalyticsSession.
        :rtype: str
        """
        return self._dnis

    @dnis.setter
    def dnis(self, dnis):
        """
        Sets the dnis of this AnalyticsSession.


        :param dnis: The dnis of this AnalyticsSession.
        :type: str
        """
        
        self._dnis = dnis

    @property
    def outbound_campaign_id(self):
        """
        Gets the outbound_campaign_id of this AnalyticsSession.


        :return: The outbound_campaign_id of this AnalyticsSession.
        :rtype: str
        """
        return self._outbound_campaign_id

    @outbound_campaign_id.setter
    def outbound_campaign_id(self, outbound_campaign_id):
        """
        Sets the outbound_campaign_id of this AnalyticsSession.


        :param outbound_campaign_id: The outbound_campaign_id of this AnalyticsSession.
        :type: str
        """
        
        self._outbound_campaign_id = outbound_campaign_id

    @property
    def outbound_contact_id(self):
        """
        Gets the outbound_contact_id of this AnalyticsSession.


        :return: The outbound_contact_id of this AnalyticsSession.
        :rtype: str
        """
        return self._outbound_contact_id

    @outbound_contact_id.setter
    def outbound_contact_id(self, outbound_contact_id):
        """
        Sets the outbound_contact_id of this AnalyticsSession.


        :param outbound_contact_id: The outbound_contact_id of this AnalyticsSession.
        :type: str
        """
        
        self._outbound_contact_id = outbound_contact_id

    @property
    def outbound_contact_list_id(self):
        """
        Gets the outbound_contact_list_id of this AnalyticsSession.


        :return: The outbound_contact_list_id of this AnalyticsSession.
        :rtype: str
        """
        return self._outbound_contact_list_id

    @outbound_contact_list_id.setter
    def outbound_contact_list_id(self, outbound_contact_list_id):
        """
        Sets the outbound_contact_list_id of this AnalyticsSession.


        :param outbound_contact_list_id: The outbound_contact_list_id of this AnalyticsSession.
        :type: str
        """
        
        self._outbound_contact_list_id = outbound_contact_list_id

    @property
    def disposition_analyzer(self):
        """
        Gets the disposition_analyzer of this AnalyticsSession.


        :return: The disposition_analyzer of this AnalyticsSession.
        :rtype: str
        """
        return self._disposition_analyzer

    @disposition_analyzer.setter
    def disposition_analyzer(self, disposition_analyzer):
        """
        Sets the disposition_analyzer of this AnalyticsSession.


        :param disposition_analyzer: The disposition_analyzer of this AnalyticsSession.
        :type: str
        """
        
        self._disposition_analyzer = disposition_analyzer

    @property
    def disposition_name(self):
        """
        Gets the disposition_name of this AnalyticsSession.


        :return: The disposition_name of this AnalyticsSession.
        :rtype: str
        """
        return self._disposition_name

    @disposition_name.setter
    def disposition_name(self, disposition_name):
        """
        Sets the disposition_name of this AnalyticsSession.


        :param disposition_name: The disposition_name of this AnalyticsSession.
        :type: str
        """
        
        self._disposition_name = disposition_name

    @property
    def edge_id(self):
        """
        Gets the edge_id of this AnalyticsSession.


        :return: The edge_id of this AnalyticsSession.
        :rtype: str
        """
        return self._edge_id

    @edge_id.setter
    def edge_id(self, edge_id):
        """
        Sets the edge_id of this AnalyticsSession.


        :param edge_id: The edge_id of this AnalyticsSession.
        :type: str
        """
        
        self._edge_id = edge_id

    @property
    def remote_name_displayable(self):
        """
        Gets the remote_name_displayable of this AnalyticsSession.


        :return: The remote_name_displayable of this AnalyticsSession.
        :rtype: str
        """
        return self._remote_name_displayable

    @remote_name_displayable.setter
    def remote_name_displayable(self, remote_name_displayable):
        """
        Sets the remote_name_displayable of this AnalyticsSession.


        :param remote_name_displayable: The remote_name_displayable of this AnalyticsSession.
        :type: str
        """
        
        self._remote_name_displayable = remote_name_displayable

    @property
    def room_id(self):
        """
        Gets the room_id of this AnalyticsSession.


        :return: The room_id of this AnalyticsSession.
        :rtype: str
        """
        return self._room_id

    @room_id.setter
    def room_id(self, room_id):
        """
        Sets the room_id of this AnalyticsSession.


        :param room_id: The room_id of this AnalyticsSession.
        :type: str
        """
        
        self._room_id = room_id

    @property
    def monitored_session_id(self):
        """
        Gets the monitored_session_id of this AnalyticsSession.


        :return: The monitored_session_id of this AnalyticsSession.
        :rtype: str
        """
        return self._monitored_session_id

    @monitored_session_id.setter
    def monitored_session_id(self, monitored_session_id):
        """
        Sets the monitored_session_id of this AnalyticsSession.


        :param monitored_session_id: The monitored_session_id of this AnalyticsSession.
        :type: str
        """
        
        self._monitored_session_id = monitored_session_id

    @property
    def monitored_participant_id(self):
        """
        Gets the monitored_participant_id of this AnalyticsSession.


        :return: The monitored_participant_id of this AnalyticsSession.
        :rtype: str
        """
        return self._monitored_participant_id

    @monitored_participant_id.setter
    def monitored_participant_id(self, monitored_participant_id):
        """
        Sets the monitored_participant_id of this AnalyticsSession.


        :param monitored_participant_id: The monitored_participant_id of this AnalyticsSession.
        :type: str
        """
        
        self._monitored_participant_id = monitored_participant_id

    @property
    def callback_user_name(self):
        """
        Gets the callback_user_name of this AnalyticsSession.


        :return: The callback_user_name of this AnalyticsSession.
        :rtype: str
        """
        return self._callback_user_name

    @callback_user_name.setter
    def callback_user_name(self, callback_user_name):
        """
        Sets the callback_user_name of this AnalyticsSession.


        :param callback_user_name: The callback_user_name of this AnalyticsSession.
        :type: str
        """
        
        self._callback_user_name = callback_user_name

    @property
    def callback_numbers(self):
        """
        Gets the callback_numbers of this AnalyticsSession.


        :return: The callback_numbers of this AnalyticsSession.
        :rtype: list[str]
        """
        return self._callback_numbers

    @callback_numbers.setter
    def callback_numbers(self, callback_numbers):
        """
        Sets the callback_numbers of this AnalyticsSession.


        :param callback_numbers: The callback_numbers of this AnalyticsSession.
        :type: list[str]
        """
        
        self._callback_numbers = callback_numbers

    @property
    def callback_scheduled_time(self):
        """
        Gets the callback_scheduled_time of this AnalyticsSession.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The callback_scheduled_time of this AnalyticsSession.
        :rtype: datetime
        """
        return self._callback_scheduled_time

    @callback_scheduled_time.setter
    def callback_scheduled_time(self, callback_scheduled_time):
        """
        Sets the callback_scheduled_time of this AnalyticsSession.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param callback_scheduled_time: The callback_scheduled_time of this AnalyticsSession.
        :type: datetime
        """
        
        self._callback_scheduled_time = callback_scheduled_time

    @property
    def script_id(self):
        """
        Gets the script_id of this AnalyticsSession.


        :return: The script_id of this AnalyticsSession.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this AnalyticsSession.


        :param script_id: The script_id of this AnalyticsSession.
        :type: str
        """
        
        self._script_id = script_id

    @property
    def skip_enabled(self):
        """
        Gets the skip_enabled of this AnalyticsSession.


        :return: The skip_enabled of this AnalyticsSession.
        :rtype: bool
        """
        return self._skip_enabled

    @skip_enabled.setter
    def skip_enabled(self, skip_enabled):
        """
        Sets the skip_enabled of this AnalyticsSession.


        :param skip_enabled: The skip_enabled of this AnalyticsSession.
        :type: bool
        """
        
        self._skip_enabled = skip_enabled

    @property
    def timeout_seconds(self):
        """
        Gets the timeout_seconds of this AnalyticsSession.


        :return: The timeout_seconds of this AnalyticsSession.
        :rtype: int
        """
        return self._timeout_seconds

    @timeout_seconds.setter
    def timeout_seconds(self, timeout_seconds):
        """
        Sets the timeout_seconds of this AnalyticsSession.


        :param timeout_seconds: The timeout_seconds of this AnalyticsSession.
        :type: int
        """
        
        self._timeout_seconds = timeout_seconds

    @property
    def segments(self):
        """
        Gets the segments of this AnalyticsSession.


        :return: The segments of this AnalyticsSession.
        :rtype: list[AnalyticsConversationSegment]
        """
        return self._segments

    @segments.setter
    def segments(self, segments):
        """
        Sets the segments of this AnalyticsSession.


        :param segments: The segments of this AnalyticsSession.
        :type: list[AnalyticsConversationSegment]
        """
        
        self._segments = segments

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

