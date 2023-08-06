# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from .context_base import ContextBase


class StartWorkflowContext(ContextBase):
    """Context provided when running within :py:class:`botoflow.workflow_starter.WorkflowStarter`.

    This gives you an opportunity to get access to the worker and workflow_execution. Generally though it's used
    for storing internal states.

    .. py:attribute:: workflow_starter

        :rtype: botoflow.workflow_starting.workflow_starter

    """

    def __init__(self, worker):
        self.worker = worker

        self._workflow_options_overrides = dict()
