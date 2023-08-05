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


class AnalyticsParticipant(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AnalyticsParticipant - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'participant_id': 'str',
            'participant_name': 'str',
            'user_id': 'str',
            'purpose': 'str',
            'external_contact_id': 'str',
            'external_organization_id': 'str',
            'sessions': 'list[AnalyticsSession]'
        }

        self.attribute_map = {
            'participant_id': 'participantId',
            'participant_name': 'participantName',
            'user_id': 'userId',
            'purpose': 'purpose',
            'external_contact_id': 'externalContactId',
            'external_organization_id': 'externalOrganizationId',
            'sessions': 'sessions'
        }

        self._participant_id = None
        self._participant_name = None
        self._user_id = None
        self._purpose = None
        self._external_contact_id = None
        self._external_organization_id = None
        self._sessions = None

    @property
    def participant_id(self):
        """
        Gets the participant_id of this AnalyticsParticipant.


        :return: The participant_id of this AnalyticsParticipant.
        :rtype: str
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, participant_id):
        """
        Sets the participant_id of this AnalyticsParticipant.


        :param participant_id: The participant_id of this AnalyticsParticipant.
        :type: str
        """
        
        self._participant_id = participant_id

    @property
    def participant_name(self):
        """
        Gets the participant_name of this AnalyticsParticipant.


        :return: The participant_name of this AnalyticsParticipant.
        :rtype: str
        """
        return self._participant_name

    @participant_name.setter
    def participant_name(self, participant_name):
        """
        Sets the participant_name of this AnalyticsParticipant.


        :param participant_name: The participant_name of this AnalyticsParticipant.
        :type: str
        """
        
        self._participant_name = participant_name

    @property
    def user_id(self):
        """
        Gets the user_id of this AnalyticsParticipant.


        :return: The user_id of this AnalyticsParticipant.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this AnalyticsParticipant.


        :param user_id: The user_id of this AnalyticsParticipant.
        :type: str
        """
        
        self._user_id = user_id

    @property
    def purpose(self):
        """
        Gets the purpose of this AnalyticsParticipant.


        :return: The purpose of this AnalyticsParticipant.
        :rtype: str
        """
        return self._purpose

    @purpose.setter
    def purpose(self, purpose):
        """
        Sets the purpose of this AnalyticsParticipant.


        :param purpose: The purpose of this AnalyticsParticipant.
        :type: str
        """
        allowed_values = ["manual", "dialer", "inbound", "acd", "ivr", "voicemail", "outbound", "agent", "user", "station", "group", "customer", "external"]
        if purpose not in allowed_values:
            raise ValueError(
                "Invalid value for `purpose`, must be one of {0}"
                .format(allowed_values)
            )

        self._purpose = purpose

    @property
    def external_contact_id(self):
        """
        Gets the external_contact_id of this AnalyticsParticipant.


        :return: The external_contact_id of this AnalyticsParticipant.
        :rtype: str
        """
        return self._external_contact_id

    @external_contact_id.setter
    def external_contact_id(self, external_contact_id):
        """
        Sets the external_contact_id of this AnalyticsParticipant.


        :param external_contact_id: The external_contact_id of this AnalyticsParticipant.
        :type: str
        """
        
        self._external_contact_id = external_contact_id

    @property
    def external_organization_id(self):
        """
        Gets the external_organization_id of this AnalyticsParticipant.


        :return: The external_organization_id of this AnalyticsParticipant.
        :rtype: str
        """
        return self._external_organization_id

    @external_organization_id.setter
    def external_organization_id(self, external_organization_id):
        """
        Sets the external_organization_id of this AnalyticsParticipant.


        :param external_organization_id: The external_organization_id of this AnalyticsParticipant.
        :type: str
        """
        
        self._external_organization_id = external_organization_id

    @property
    def sessions(self):
        """
        Gets the sessions of this AnalyticsParticipant.


        :return: The sessions of this AnalyticsParticipant.
        :rtype: list[AnalyticsSession]
        """
        return self._sessions

    @sessions.setter
    def sessions(self, sessions):
        """
        Sets the sessions of this AnalyticsParticipant.


        :param sessions: The sessions of this AnalyticsParticipant.
        :type: list[AnalyticsSession]
        """
        
        self._sessions = sessions

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

