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

# XXX docs


from .context_base import ContextBase
from .start_workflow_context import StartWorkflowContext
from .activity_context import ActivityContext
from .decision_context import DecisionContext

__all__ = ('get_context', 'set_context', 'StartWorkflowContext',
           'ActivityContext', 'DecisionContext')


get_context = ContextBase.get_context
set_context = ContextBase.set_context
