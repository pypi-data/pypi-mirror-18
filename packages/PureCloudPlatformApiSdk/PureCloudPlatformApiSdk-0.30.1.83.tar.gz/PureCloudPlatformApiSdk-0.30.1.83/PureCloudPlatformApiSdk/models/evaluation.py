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


class Evaluation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Evaluation - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'conversation': 'Conversation',
            'evaluation_form': 'EvaluationForm',
            'evaluator': 'User',
            'agent': 'User',
            'calibration': 'Calibration',
            'status': 'str',
            'answers': 'EvaluationScoringSet',
            'agent_has_read': 'bool',
            'release_date': 'datetime',
            'assigned_date': 'datetime',
            'changed_date': 'datetime',
            'queue': 'Queue',
            'never_release': 'bool',
            'resource_id': 'str',
            'resource_type': 'str',
            'redacted': 'bool',
            'is_scoring_index': 'bool',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'conversation': 'conversation',
            'evaluation_form': 'evaluationForm',
            'evaluator': 'evaluator',
            'agent': 'agent',
            'calibration': 'calibration',
            'status': 'status',
            'answers': 'answers',
            'agent_has_read': 'agentHasRead',
            'release_date': 'releaseDate',
            'assigned_date': 'assignedDate',
            'changed_date': 'changedDate',
            'queue': 'queue',
            'never_release': 'neverRelease',
            'resource_id': 'resourceId',
            'resource_type': 'resourceType',
            'redacted': 'redacted',
            'is_scoring_index': 'isScoringIndex',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._conversation = None
        self._evaluation_form = None
        self._evaluator = None
        self._agent = None
        self._calibration = None
        self._status = None
        self._answers = None
        self._agent_has_read = False
        self._release_date = None
        self._assigned_date = None
        self._changed_date = None
        self._queue = None
        self._never_release = False
        self._resource_id = None
        self._resource_type = None
        self._redacted = False
        self._is_scoring_index = False
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Evaluation.
        The globally unique identifier for the object.

        :return: The id of this Evaluation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Evaluation.
        The globally unique identifier for the object.

        :param id: The id of this Evaluation.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Evaluation.


        :return: The name of this Evaluation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Evaluation.


        :param name: The name of this Evaluation.
        :type: str
        """
        
        self._name = name

    @property
    def conversation(self):
        """
        Gets the conversation of this Evaluation.


        :return: The conversation of this Evaluation.
        :rtype: Conversation
        """
        return self._conversation

    @conversation.setter
    def conversation(self, conversation):
        """
        Sets the conversation of this Evaluation.


        :param conversation: The conversation of this Evaluation.
        :type: Conversation
        """
        
        self._conversation = conversation

    @property
    def evaluation_form(self):
        """
        Gets the evaluation_form of this Evaluation.
        Evaluation form used for evaluation.

        :return: The evaluation_form of this Evaluation.
        :rtype: EvaluationForm
        """
        return self._evaluation_form

    @evaluation_form.setter
    def evaluation_form(self, evaluation_form):
        """
        Sets the evaluation_form of this Evaluation.
        Evaluation form used for evaluation.

        :param evaluation_form: The evaluation_form of this Evaluation.
        :type: EvaluationForm
        """
        
        self._evaluation_form = evaluation_form

    @property
    def evaluator(self):
        """
        Gets the evaluator of this Evaluation.


        :return: The evaluator of this Evaluation.
        :rtype: User
        """
        return self._evaluator

    @evaluator.setter
    def evaluator(self, evaluator):
        """
        Sets the evaluator of this Evaluation.


        :param evaluator: The evaluator of this Evaluation.
        :type: User
        """
        
        self._evaluator = evaluator

    @property
    def agent(self):
        """
        Gets the agent of this Evaluation.


        :return: The agent of this Evaluation.
        :rtype: User
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """
        Sets the agent of this Evaluation.


        :param agent: The agent of this Evaluation.
        :type: User
        """
        
        self._agent = agent

    @property
    def calibration(self):
        """
        Gets the calibration of this Evaluation.


        :return: The calibration of this Evaluation.
        :rtype: Calibration
        """
        return self._calibration

    @calibration.setter
    def calibration(self, calibration):
        """
        Sets the calibration of this Evaluation.


        :param calibration: The calibration of this Evaluation.
        :type: Calibration
        """
        
        self._calibration = calibration

    @property
    def status(self):
        """
        Gets the status of this Evaluation.


        :return: The status of this Evaluation.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this Evaluation.


        :param status: The status of this Evaluation.
        :type: str
        """
        allowed_values = ["PENDING", "INPROGRESS", "FINISHED"]
        if status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for status -> " + status
            self._status = "outdated_sdk_version"
        else:
            self._status = status.lower()

    @property
    def answers(self):
        """
        Gets the answers of this Evaluation.


        :return: The answers of this Evaluation.
        :rtype: EvaluationScoringSet
        """
        return self._answers

    @answers.setter
    def answers(self, answers):
        """
        Sets the answers of this Evaluation.


        :param answers: The answers of this Evaluation.
        :type: EvaluationScoringSet
        """
        
        self._answers = answers

    @property
    def agent_has_read(self):
        """
        Gets the agent_has_read of this Evaluation.


        :return: The agent_has_read of this Evaluation.
        :rtype: bool
        """
        return self._agent_has_read

    @agent_has_read.setter
    def agent_has_read(self, agent_has_read):
        """
        Sets the agent_has_read of this Evaluation.


        :param agent_has_read: The agent_has_read of this Evaluation.
        :type: bool
        """
        
        self._agent_has_read = agent_has_read

    @property
    def release_date(self):
        """
        Gets the release_date of this Evaluation.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The release_date of this Evaluation.
        :rtype: datetime
        """
        return self._release_date

    @release_date.setter
    def release_date(self, release_date):
        """
        Sets the release_date of this Evaluation.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param release_date: The release_date of this Evaluation.
        :type: datetime
        """
        
        self._release_date = release_date

    @property
    def assigned_date(self):
        """
        Gets the assigned_date of this Evaluation.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The assigned_date of this Evaluation.
        :rtype: datetime
        """
        return self._assigned_date

    @assigned_date.setter
    def assigned_date(self, assigned_date):
        """
        Sets the assigned_date of this Evaluation.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param assigned_date: The assigned_date of this Evaluation.
        :type: datetime
        """
        
        self._assigned_date = assigned_date

    @property
    def changed_date(self):
        """
        Gets the changed_date of this Evaluation.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The changed_date of this Evaluation.
        :rtype: datetime
        """
        return self._changed_date

    @changed_date.setter
    def changed_date(self, changed_date):
        """
        Sets the changed_date of this Evaluation.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param changed_date: The changed_date of this Evaluation.
        :type: datetime
        """
        
        self._changed_date = changed_date

    @property
    def queue(self):
        """
        Gets the queue of this Evaluation.


        :return: The queue of this Evaluation.
        :rtype: Queue
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """
        Sets the queue of this Evaluation.


        :param queue: The queue of this Evaluation.
        :type: Queue
        """
        
        self._queue = queue

    @property
    def never_release(self):
        """
        Gets the never_release of this Evaluation.
        Signifies if the evaluation is never to be released. This cannot be set true if release date is also set.

        :return: The never_release of this Evaluation.
        :rtype: bool
        """
        return self._never_release

    @never_release.setter
    def never_release(self, never_release):
        """
        Sets the never_release of this Evaluation.
        Signifies if the evaluation is never to be released. This cannot be set true if release date is also set.

        :param never_release: The never_release of this Evaluation.
        :type: bool
        """
        
        self._never_release = never_release

    @property
    def resource_id(self):
        """
        Gets the resource_id of this Evaluation.
        Only used for email evaluations. Will be null for all other evaluations.

        :return: The resource_id of this Evaluation.
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """
        Sets the resource_id of this Evaluation.
        Only used for email evaluations. Will be null for all other evaluations.

        :param resource_id: The resource_id of this Evaluation.
        :type: str
        """
        
        self._resource_id = resource_id

    @property
    def resource_type(self):
        """
        Gets the resource_type of this Evaluation.
        The type of resource. Only used for email evaluations. Will be null for evaluations on all other resources.

        :return: The resource_type of this Evaluation.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this Evaluation.
        The type of resource. Only used for email evaluations. Will be null for evaluations on all other resources.

        :param resource_type: The resource_type of this Evaluation.
        :type: str
        """
        allowed_values = ["EMAIL"]
        if resource_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for resource_type -> " + resource_type
            self._resource_type = "outdated_sdk_version"
        else:
            self._resource_type = resource_type.lower()

    @property
    def redacted(self):
        """
        Gets the redacted of this Evaluation.
        Is only true when the user making the request does not have sufficient permissions to see evaluation

        :return: The redacted of this Evaluation.
        :rtype: bool
        """
        return self._redacted

    @redacted.setter
    def redacted(self, redacted):
        """
        Sets the redacted of this Evaluation.
        Is only true when the user making the request does not have sufficient permissions to see evaluation

        :param redacted: The redacted of this Evaluation.
        :type: bool
        """
        
        self._redacted = redacted

    @property
    def is_scoring_index(self):
        """
        Gets the is_scoring_index of this Evaluation.


        :return: The is_scoring_index of this Evaluation.
        :rtype: bool
        """
        return self._is_scoring_index

    @is_scoring_index.setter
    def is_scoring_index(self, is_scoring_index):
        """
        Sets the is_scoring_index of this Evaluation.


        :param is_scoring_index: The is_scoring_index of this Evaluation.
        :type: bool
        """
        
        self._is_scoring_index = is_scoring_index

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Evaluation.
        The URI for this object

        :return: The self_uri of this Evaluation.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Evaluation.
        The URI for this object

        :param self_uri: The self_uri of this Evaluation.
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

