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


class Call(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Call - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'id': 'str',
            'direction': 'str',
            'recording': 'bool',
            'recording_state': 'str',
            'muted': 'bool',
            'confined': 'bool',
            'held': 'bool',
            'recording_id': 'str',
            'segments': 'list[Segment]',
            'error_info': 'ErrorBody',
            'disconnect_type': 'str',
            'start_hold_time': 'datetime',
            'document_id': 'str',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'disconnect_reasons': 'list[DisconnectReason]',
            'fax_status': 'FaxStatus',
            'provider': 'str'
        }

        self.attribute_map = {
            'state': 'state',
            'id': 'id',
            'direction': 'direction',
            'recording': 'recording',
            'recording_state': 'recordingState',
            'muted': 'muted',
            'confined': 'confined',
            'held': 'held',
            'recording_id': 'recordingId',
            'segments': 'segments',
            'error_info': 'errorInfo',
            'disconnect_type': 'disconnectType',
            'start_hold_time': 'startHoldTime',
            'document_id': 'documentId',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'disconnect_reasons': 'disconnectReasons',
            'fax_status': 'faxStatus',
            'provider': 'provider'
        }

        self._state = None
        self._id = None
        self._direction = None
        self._recording = False
        self._recording_state = None
        self._muted = False
        self._confined = False
        self._held = False
        self._recording_id = None
        self._segments = None
        self._error_info = None
        self._disconnect_type = None
        self._start_hold_time = None
        self._document_id = None
        self._connected_time = None
        self._disconnected_time = None
        self._disconnect_reasons = None
        self._fax_status = None
        self._provider = None

    @property
    def state(self):
        """
        Gets the state of this Call.
        The connection state of this communication.

        :return: The state of this Call.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Call.
        The connection state of this communication.

        :param state: The state of this Call.
        :type: str
        """
        allowed_values = ["ALERTING", "DIALING", "CONTACTING", "OFFERING", "CONNECTED", "DISCONNECTED", "TERMINATED", "CONVERTING", "UPLOADING", "TRANSMITTING", "NONE"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state.lower()

    @property
    def id(self):
        """
        Gets the id of this Call.
        A globally unique identifier for this communication.

        :return: The id of this Call.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Call.
        A globally unique identifier for this communication.

        :param id: The id of this Call.
        :type: str
        """
        
        self._id = id

    @property
    def direction(self):
        """
        Gets the direction of this Call.
        The direction of the call

        :return: The direction of this Call.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this Call.
        The direction of the call

        :param direction: The direction of this Call.
        :type: str
        """
        allowed_values = ["INBOUND", "OUTBOUND"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for direction -> " + direction
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction.lower()

    @property
    def recording(self):
        """
        Gets the recording of this Call.
        True if this call is being recorded.

        :return: The recording of this Call.
        :rtype: bool
        """
        return self._recording

    @recording.setter
    def recording(self, recording):
        """
        Sets the recording of this Call.
        True if this call is being recorded.

        :param recording: The recording of this Call.
        :type: bool
        """
        
        self._recording = recording

    @property
    def recording_state(self):
        """
        Gets the recording_state of this Call.
        State of recording on this call.

        :return: The recording_state of this Call.
        :rtype: str
        """
        return self._recording_state

    @recording_state.setter
    def recording_state(self, recording_state):
        """
        Sets the recording_state of this Call.
        State of recording on this call.

        :param recording_state: The recording_state of this Call.
        :type: str
        """
        allowed_values = ["NONE", "ACTIVE", "PAUSED"]
        if recording_state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for recording_state -> " + recording_state
            self._recording_state = "outdated_sdk_version"
        else:
            self._recording_state = recording_state.lower()

    @property
    def muted(self):
        """
        Gets the muted of this Call.
        True if this call is muted so that remote participants can't hear any audio from this end.

        :return: The muted of this Call.
        :rtype: bool
        """
        return self._muted

    @muted.setter
    def muted(self, muted):
        """
        Sets the muted of this Call.
        True if this call is muted so that remote participants can't hear any audio from this end.

        :param muted: The muted of this Call.
        :type: bool
        """
        
        self._muted = muted

    @property
    def confined(self):
        """
        Gets the confined of this Call.
        True if this call is held and the person on this side hears hold music.

        :return: The confined of this Call.
        :rtype: bool
        """
        return self._confined

    @confined.setter
    def confined(self, confined):
        """
        Sets the confined of this Call.
        True if this call is held and the person on this side hears hold music.

        :param confined: The confined of this Call.
        :type: bool
        """
        
        self._confined = confined

    @property
    def held(self):
        """
        Gets the held of this Call.
        True if this call is held and the person on this side hears silence.

        :return: The held of this Call.
        :rtype: bool
        """
        return self._held

    @held.setter
    def held(self, held):
        """
        Sets the held of this Call.
        True if this call is held and the person on this side hears silence.

        :param held: The held of this Call.
        :type: bool
        """
        
        self._held = held

    @property
    def recording_id(self):
        """
        Gets the recording_id of this Call.
        A globally unique identifier for the recording associated with this call.

        :return: The recording_id of this Call.
        :rtype: str
        """
        return self._recording_id

    @recording_id.setter
    def recording_id(self, recording_id):
        """
        Sets the recording_id of this Call.
        A globally unique identifier for the recording associated with this call.

        :param recording_id: The recording_id of this Call.
        :type: str
        """
        
        self._recording_id = recording_id

    @property
    def segments(self):
        """
        Gets the segments of this Call.
        The time line of the participant's call, divided into activity segments.

        :return: The segments of this Call.
        :rtype: list[Segment]
        """
        return self._segments

    @segments.setter
    def segments(self, segments):
        """
        Sets the segments of this Call.
        The time line of the participant's call, divided into activity segments.

        :param segments: The segments of this Call.
        :type: list[Segment]
        """
        
        self._segments = segments

    @property
    def error_info(self):
        """
        Gets the error_info of this Call.


        :return: The error_info of this Call.
        :rtype: ErrorBody
        """
        return self._error_info

    @error_info.setter
    def error_info(self, error_info):
        """
        Sets the error_info of this Call.


        :param error_info: The error_info of this Call.
        :type: ErrorBody
        """
        
        self._error_info = error_info

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this Call.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :return: The disconnect_type of this Call.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this Call.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :param disconnect_type: The disconnect_type of this Call.
        :type: str
        """
        allowed_values = ["ENDPOINT", "CLIENT", "SYSTEM", "TIMEOUT", "TRANSFER", "TRANSFER_CONFERENCE", "TRANSFER_CONSULT", "TRANSFER_FORWARD", "TRANSFER_NOANSWER", "TRANSFER_NOTAVAILABLE", "TRANSPORT_FAILURE", "ERROR", "PEER", "OTHER", "SPAM"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for disconnect_type -> " + disconnect_type
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type.lower()

    @property
    def start_hold_time(self):
        """
        Gets the start_hold_time of this Call.
        The timestamp the call was placed on hold in the cloud clock if the call is currently on hold. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The start_hold_time of this Call.
        :rtype: datetime
        """
        return self._start_hold_time

    @start_hold_time.setter
    def start_hold_time(self, start_hold_time):
        """
        Sets the start_hold_time of this Call.
        The timestamp the call was placed on hold in the cloud clock if the call is currently on hold. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param start_hold_time: The start_hold_time of this Call.
        :type: datetime
        """
        
        self._start_hold_time = start_hold_time

    @property
    def document_id(self):
        """
        Gets the document_id of this Call.
        If call is an outbound fax of a document from content management, then this is the id in content management.

        :return: The document_id of this Call.
        :rtype: str
        """
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        """
        Sets the document_id of this Call.
        If call is an outbound fax of a document from content management, then this is the id in content management.

        :param document_id: The document_id of this Call.
        :type: str
        """
        
        self._document_id = document_id

    @property
    def connected_time(self):
        """
        Gets the connected_time of this Call.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The connected_time of this Call.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this Call.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param connected_time: The connected_time of this Call.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this Call.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The disconnected_time of this Call.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this Call.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param disconnected_time: The disconnected_time of this Call.
        :type: datetime
        """
        
        self._disconnected_time = disconnected_time

    @property
    def disconnect_reasons(self):
        """
        Gets the disconnect_reasons of this Call.
        List of reasons that this call was disconnected. This will be set once the call disconnects.

        :return: The disconnect_reasons of this Call.
        :rtype: list[DisconnectReason]
        """
        return self._disconnect_reasons

    @disconnect_reasons.setter
    def disconnect_reasons(self, disconnect_reasons):
        """
        Sets the disconnect_reasons of this Call.
        List of reasons that this call was disconnected. This will be set once the call disconnects.

        :param disconnect_reasons: The disconnect_reasons of this Call.
        :type: list[DisconnectReason]
        """
        
        self._disconnect_reasons = disconnect_reasons

    @property
    def fax_status(self):
        """
        Gets the fax_status of this Call.
        Extra information on fax transmission.

        :return: The fax_status of this Call.
        :rtype: FaxStatus
        """
        return self._fax_status

    @fax_status.setter
    def fax_status(self, fax_status):
        """
        Sets the fax_status of this Call.
        Extra information on fax transmission.

        :param fax_status: The fax_status of this Call.
        :type: FaxStatus
        """
        
        self._fax_status = fax_status

    @property
    def provider(self):
        """
        Gets the provider of this Call.
        The source provider for the call.

        :return: The provider of this Call.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this Call.
        The source provider for the call.

        :param provider: The provider of this Call.
        :type: str
        """
        
        self._provider = provider

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

