# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from pyoko.fields import DATE_FORMAT
from datetime import datetime
from zengine.lib.decorators import view, bg_job
from zengine.models import TaskInvitation, BPMNWorkflow


@view()
def mark_offline_user(current):
    current.user.is_online(False)


@view()
def get_task_types(current):
    """
           List task types for current user


           .. code-block:: python

               #  request:
                   {
                   'view': '_zops_get_task_types',
                   }

               #  response:
                   {
                   'task_types': [
                       {'name': string, # wf name
                        'title': string,  # title of workflow
                        },]
                        }
    """
    current.output['task_types'] = [{'name': bpmn_wf.name,
                                     'title': bpmn_wf.title}
                                    for bpmn_wf in BPMNWorkflow.objects.filter()
                                    if current.has_permission(bpmn_wf.name)]


@view()
def get_task_detail(current):
    """
           Show task details

           .. code-block:: python

               #  request:
                   {
                   'view': '_zops_get_task_detail',
                   'key': key,
                   }

               #  response:
                   {
                   'task_title': string,
                   'task_detail': string, # markdown formatted text
                    }
    """
    task_inv = TaskInvitation.objects.get(current.input['key'])
    obj = task_inv.instance.get_object()
    current.output['task_title'] = task_inv.instance.task.name
    current.output['task_detail'] = """Explain: %s
    State: %s""" % (obj.__unicode__() if obj else '', task_inv.progress)


@view()
def get_task_actions(current):
    """
           List task types for current user


           .. code-block:: python

               #  request:
                   {
                   'view': '_zops_get_task_actions',
                   'key': key,
                   }

               #  response:
                   {
                   'key': key,
                   'actions': [('name_string', 'cmd_string'),]
                    }
    """
    task_inv = TaskInvitation.objects.get(current.input['key'])
    current.output['key'] = task_inv.key
    current.output['actions'] = [(task_inv.instance.name, task_inv.wf_name), ]


@view()
def get_tasks(current):
    """
        List task invitations of current user


        .. code-block:: python

            #  request:
                {
                'view': '_zops_get_tasks',
                'state': string, # one of these:
                                 # "active", "future", "finished", "expired"
                'inverted': boolean, # search on other people's tasks
                'query': string, # optional. for searching on user's tasks
                'wf_type': string, # optional. only show tasks of selected wf_type
                'start_date': datetime, # optional. only show tasks starts after this date
                'finish_date': datetime, # optional. only show tasks should end before this date
                }

            #  response:
                {
                'task_list': [
                    {'token': key, # wf token (key of WFInstance)
                    {'key': key, # wf token (key of TaskInvitation)
                     'title': string,  # name of workflow
                     'wf_type': string,  # unread message count
                     'title': string,  # task title
                     'state': int,  # state of invitation
                                    # zengine.models.workflow_manager.TASK_STATES
                     'start_date': string,  # start date
                     'finish_date': string,  # end date

                     },]
                }
        """
    # TODO: Also return invitations for user's other roles
    # TODO: Handle automatic role switching

    STATE_DICT = {
        'active': [20, 30],
        'future': 10,
        'finished': 40,
        'expired': 90
    }
    state = STATE_DICT[current.input['state']]
    if isinstance(state, list):
        queryset = TaskInvitation.objects.filter(progress__in=state)
    else:
        queryset = TaskInvitation.objects.filter(progress=state)

    if 'inverted' in current.input:
        # show other user's tasks
        allowed_workflows = [bpmn_wf.name for bpmn_wf in BPMNWorkflow.objects.filter()
                             if current.has_permission(bpmn_wf.name)]
        queryset = queryset.exclude(role_id=current.role_id).filter(wf_name__in=allowed_workflows)
    else:
        # show current user's tasks
        queryset = queryset.filter(role_id=current.role_id)

    if 'query' in current.input:
        queryset = queryset.filter(search_data__contains=current.input['query'].lower())
    if 'wf_type' in current.input:
        queryset = queryset.filter(wf_name=current.input['wf_type'])
    if 'start_date' in current.input:
        queryset = queryset.filter(start_date__gte=datetime.strptime(current.input['start_date'], "%d.%m.%Y"))
    if 'finish_date' in current.input:
        queryset = queryset.filter(finish_date__lte=datetime.strptime(current.input['finish_date'], "%d.%m.%Y"))
    current.output['task_list'] = [
        {
            'token': inv.instance.key,
            'key': inv.key,
            'title': inv.title,
            'wf_type': inv.wf_name,
            'state': inv.progress,
            'start_date': inv.instance.task.start_date.strftime(DATE_FORMAT),
            'finish_date': inv.instance.task.finish_date.strftime(DATE_FORMAT)}
        for inv in queryset
        ]
