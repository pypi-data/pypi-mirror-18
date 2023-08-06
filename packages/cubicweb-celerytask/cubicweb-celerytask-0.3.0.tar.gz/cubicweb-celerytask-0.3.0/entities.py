# -*- coding: utf-8 -*-
# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-celerytask entity's classes"""
import six
import warnings

import celery
from celery.result import AsyncResult, from_serializable

from cubicweb.entities import AnyEntity, fetch_config
from cubicweb.view import EntityAdapter
from cubicweb.predicates import is_instance
from cubicweb.server.hook import DataOperationMixIn, Operation

from cw_celerytask_helpers import redislogger as loghelper

from cubes.celerytask import STATES, FINAL_STATES

_ = six.text_type

_TEST_TASKS = {}


def get_tasks():
    """Return tasks to be run (for use in cubicweb test mode)"""
    return _TEST_TASKS


def run_all_tasks(cnx=None):
    """Run all pending tasks (for use in cubicweb test mode)"""
    if cnx is None:
        warnings.warn('cnx argument should be specified to enable task '
                      'workflow synchronisation', DeprecationWarning,
                      stacklevel=2)
    results = {}
    for task_eid, task in _TEST_TASKS.items():
        results[task_eid] = task.delay()

    if cnx is not None:
        if celery.current_app.conf.CELERY_ALWAYS_EAGER:
            for task_eid, result in results.items():
                wf = cnx.entity_from_eid(task_eid).cw_adapt_to('IWorkflowable')
                transition = {
                    STATES.SUCCESS: 'finish',
                    STATES.FAILURE: 'fail',
                }[result.state]
                wf.fire_transition(transition, result.traceback)
        else:
            from cubes.celerytask.ccplugin import CeleryMonitorCommand
            CeleryMonitorCommand.on_monitor_start(cnx)
    return results


def start_async_task(cnx, task, *args, **kwargs):
    """Create and start a new task

    `task` can be either a task name, a task object or a task signature
    """
    task_name = six.text_type(celery.signature(task).task)
    entity = cnx.create_entity('CeleryTask', task_name=task_name)
    entity.cw_adapt_to('ICeleryTask').start(task, *args, **kwargs)
    return entity


def task_in_backend(task_id):
    app = celery.current_app
    if app.conf.CELERY_ALWAYS_EAGER:
        return False
    else:
        backend = app.backend
        return backend.get(backend.get_key_for_task(task_id)) is not None


class StartCeleryTaskOp(DataOperationMixIn, Operation):

    def postcommit_event(self):
        global _TEST_TASKS
        if self.cnx.vreg.config.mode == 'test':
            # In test mode, task should run explicitly with run_all_tasks()
            _TEST_TASKS = self.cnx.transaction_data.get('celerytask', {})
        else:
            for eid in self.get_data():
                task = self.cnx.transaction_data.get('celerytask', {}).get(eid)
                if task is not None:
                    task.delay()


class CeleryTask(AnyEntity):
    __regid__ = 'CeleryTask'
    fetch_attrs, cw_fetch_order = fetch_config(('task_name',))

    def dc_title(self):
        return self.task_name

    def dc_long_title(self):
        adapted = self.cw_adapt_to('ICeleryTask')
        state, finished = adapted.state, adapted.finished
        title = self.task_name or self._cw._('subtask')
        if finished:
            title = '%s (%s)' % (title, self._cw._(state))
        return title

    @property
    def progress(self):
        yield self.cw_adapt_to('ICeleryTask').progress
        for subtask in self.reverse_parent_task:
            yield subtask.progress

    @property
    def parent_tasks(self):
        yield self
        for task in self.parent_task:
            for ptask in task.parent_tasks:
                yield ptask


class ICeleryTask(EntityAdapter):
    __regid__ = 'ICeleryTask'
    __abstract__ = True

    def start(self, name, *args, **kwargs):
        eid = self.entity.eid
        task = self.get_task(name, *args, **kwargs)
        self._cw.transaction_data.setdefault('celerytask', {})[eid] = task
        StartCeleryTaskOp.get_instance(self._cw).add_data(eid)

    def get_task(self, name, *args, **kwargs):
        """Should return a celery task / signature or None

        This method run in a precommit event
        """
        return celery.signature(name, args=args, kwargs=kwargs)

    @staticmethod
    def on_event(cnx, event):
        """Triggered by celery-monitor"""
        pass

    @staticmethod
    def on_monitor_start(cnx):
        """Triggered by celery-monitor"""
        pass

    @property
    def task_id(self):
        raise NotImplementedError

    @property
    def task_name(self):
        raise NotImplementedError

    @property
    def logs(self):
        return loghelper.get_task_logs(self.task_id) or b''

    @property
    def result(self):
        return AsyncResult(self.task_id)

    @property
    def progress(self):
        if celery.current_app.conf.CELERY_ALWAYS_EAGER:
            return 1.
        result = self.result
        if result.info and 'progress' in result.info:
            return result.info['progress']
        elif self.entity.reverse_parent_task:
            children = self.entity.reverse_parent_task
            return sum(child.cw_adapt_to('ICeleryTask').progress
                       for child in children) / len(children)
        elif result.state == STATES.SUCCESS:
            return 1.
        else:
            return 0.

    @property
    def state(self):
        return self.result.state

    @property
    def finished(self):
        return self.state in FINAL_STATES


def get_task_id(task):
    if hasattr(task, 'freeze'):
        # false for ASyncResult
        result = task.freeze()
    else:
        result = task
    if hasattr(result, 'task_id'):
        return result.task_id
    elif hasattr(result, 'id'):
        return result.id
    else:
        # Group
        return get_task_id(task.tasks[-1])


class CeleryTaskAdapter(ICeleryTask):
    """Base adapter that store task call args in the transaction"""

    __select__ = ICeleryTask.__select__ & is_instance('CeleryTask')

    tr_map = {
        'task-failed': 'fail',
        'task-succeeded': 'finish',
        'task-received': 'enqueue',
        'task-started': 'start',
        'task-revoked': 'fail',
    }

    def attach_task(self, task, seen, parent=None):
        task_id = six.text_type(get_task_id(task))
        if parent is None:
            parent = self.entity
        if self.entity.task_id is None:
            self.entity.cw_set(task_id=task_id)
        elif task_id not in seen:
            task_name = six.text_type(task.task)
            parent = self._cw.create_entity('CeleryTask',
                                            task_id=six.text_type(task_id),
                                            task_name=task_name,
                                            parent_task=parent)
        seen.add(task_id)
        if hasattr(task, 'body'):
            self.attach_task(task.body, seen, parent)
        if hasattr(task, 'tasks'):
            for subtask in task.tasks:
                self.attach_task(subtask, seen, parent)

    def get_task(self, name, *args, **kwargs):
        task = super(CeleryTaskAdapter, self).get_task(
            name, *args, **kwargs)
        self.attach_task(task, set())
        return task

    @property
    def task_id(self):
        return self.entity.task_id

    @property
    def task_name(self):
        return self.entity.task_name

    def attach_result(self, result):
        def tree(result, seen=None):
            if seen is None:
                seen = set()
            if result.parent:
                for r in tree(result.parent, seen):
                    yield r
            for child in result.children or []:
                for r in tree(child, seen):
                    yield r

            if isinstance(result, AsyncResult):
                try:
                    rresult = from_serializable(result.result)
                except:
                    CeleryTaskAdapter.info(
                        'Cannot deserialize task result %s: %s',
                        result, result.result)
                else:
                    for r in tree(rresult, seen):
                        yield r

                if result.task_id not in seen:
                    seen.add(result.task_id)
                yield result

        for asr in tree(result):
            task_id = six.text_type(asr.id)
            rset = self._cw.find('CeleryTask', task_id=task_id)
            if rset:
                cwtask = rset.one()
            else:
                self.info("create a CeleryTask for %s" % task_id)
                cwtask = self._cw.create_entity(
                    'CeleryTask',
                    task_name=six.text_type(''),
                    task_id=six.text_type(task_id))
            if not cwtask.parent_task and self.entity is not cwtask:
                self.info('Set %s parent_task to %s (%s)', cwtask.task_id,
                          self.entity, self.entity.task_id)
                cwtask.cw_set(parent_task=self.entity)

    @staticmethod
    def on_event(cnx, event):
        # handle weaving of parent_task relations
        if event['type'] in ('task-received', 'task-sent'):
            # may create the cw task entity, if needed
            rset = cnx.find('CeleryTask', task_id=event['uuid'])
            if not rset:  # and 'name' in event:
                CeleryTaskAdapter.info("create CeleryTask for %s (%s)",
                                       event['uuid'], event['name'])
                entity = cnx.create_entity(
                    'CeleryTask',
                    task_id=six.text_type(event['uuid']),
                    task_name=six.text_type(event['name']),
                    )
                cnx.commit()
            else:
                entity = rset.one()
                CeleryTaskAdapter.info(
                    "using existing CeleryTask %s for %s (%s)",
                    entity, event['uuid'], event['name'])
            if entity.task_name != event['name']:
                if entity.task_name:
                    CeleryTaskAdapter.warning(
                        '<CeleryTask %s (task_id %s)> already has a name: %s',
                        entity.eid, entity.task_id, entity.task_name)
                CeleryTaskAdapter.info('set %s name to %s', entity.task_id,
                                       event['name'])
                entity.cw_set(task_name=event['name'])
            cnx.commit()

        elif event['type'] == 'task-succeeded':
            rset = cnx.find('CeleryTask', task_id=event['uuid'])
            if rset:
                asresult = AsyncResult(event['uuid'])
                CeleryTaskAdapter.info(
                    "Task %s:\n  asresult=%s\n  event.result=%s",
                    event['uuid'], asresult.result, event['result'])
                root = rset.one()
                root.cw_adapt_to('ICeleryTask').attach_result(asresult)
                cnx.commit()
            else:
                CeleryTaskAdapter.warning(
                    'Cannot find a cw entity for %s', event['uuid'])

        # manage workflow
        tr_map = CeleryTaskAdapter.tr_map
        if event['type'] in tr_map:
            rset = cnx.find('CeleryTask', task_id=event['uuid'])
            if not rset:
                CeleryTaskAdapter.warning(
                    '<CeleryTask (task_id %s)> not found in database; '
                    'cannot set it\'s state',
                    event['uuid'])
                return
            entity = rset.one()
            transition = tr_map[event['type']]
            CeleryTaskAdapter.fire_task_transition(
                entity, transition, event.get('exception'))

    @staticmethod
    def on_monitor_start(cnx):
        for task_eid, task_id in cnx.execute((
            'Any T, TID WHERE '
            'T is CeleryTask, T task_id TID, T in_state S, '
            'S name in ("waiting", "queued", "running")'
        )):
            result = AsyncResult(task_id)
            transition = {
                STATES.SUCCESS: 'finish',
                STATES.FAILURE: 'fail',
                STATES.STARTED: 'running',
            }.get(result.state)
            if transition is not None:
                CeleryTaskAdapter.fire_task_transition(
                    cnx.entity_from_eid(task_eid),
                    transition, result.traceback)

    @staticmethod
    def fire_task_transition(cnx, task, transition, traceback):
        try:
            wf = task.cw_adapt_to('IWorkflowable')
            wf.fire_transition_if_possible(
                transition, traceback)
            cnx.commit()
            CeleryTaskAdapter.info('<CeleryTask %s (task_id %s)> %s',
                                   task.eid, task.task_id, transition)
        except Exception as exc:
            CeleryTaskAdapter.error(
                '<CeleryTask %s (task_id %s)> failed to fire %s:\n%s',
                task.eid, task.task_id, transition, exc)
            cnx.rollback()

    @property
    def logs(self):
        task_logs = self.entity.task_logs
        if task_logs is not None:
            task_logs.seek(0)
            return task_logs.read()
        else:
            return super(CeleryTaskAdapter, self).logs

    @property
    def state(self):
        db_state = self.entity.cw_adapt_to('IWorkflowable').state
        db_final_state_map = {'done': STATES.SUCCESS, 'failed': STATES.FAILURE}
        if db_state in db_final_state_map:
            return db_final_state_map[db_state]
        elif task_in_backend(self.task_id):
            return super(CeleryTaskAdapter, self).state
        return _('unknown state')
