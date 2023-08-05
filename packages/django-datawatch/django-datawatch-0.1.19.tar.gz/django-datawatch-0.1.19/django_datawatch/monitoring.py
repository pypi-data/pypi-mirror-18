# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import logging
import importlib
from collections import defaultdict

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import autodiscover_modules
from django.db.models import signals

from django_datawatch.defaults import defaults

logger = logging.getLogger(__name__)


class MonitoringHandler(object):
    def __init__(self):
        self._registered_checks = {}
        self._related_models = defaultdict(list)
        self._backend = None

    def autodiscover_checks(self, module_name='checks'):
        autodiscover_modules(module_name)

    def register(self, check_class):
        slug = self.get_slug(check_class.__module__, check_class.__name__)
        self._registered_checks[slug] = check_class
        check = check_class()
        for keyword, model in check.trigger_update.items():
            method_name = 'get_%s_payload' % keyword
            if not hasattr(check, method_name):
                logger.warning(
                    'Update trigger "%s" defined without implementing .%s()',
                    keyword, method_name)
                continue

            model_uid = make_model_uid(model)
            self._related_models.setdefault(model_uid, list())
            if check_class not in self._related_models[model_uid]:
                signals.post_save.connect(run_checks, sender=model,
                                          dispatch_uid='django_datawatch')
            self._related_models[model_uid].append(check_class)

        return check_class

    def get_all_registered_checks(self):
        return self._registered_checks.values()

    def get_all_registered_check_slugs(self):
        return self._registered_checks.keys()

    def get_check_class(self, slug):
        if slug in self._registered_checks:
            return self._registered_checks[slug]
        return None

    def get_checks_for_model(self, model):
        model_uid = make_model_uid(model)
        if model_uid in self._related_models:
            return self._related_models[model_uid]
        return None

    def get_slug(self, module, class_name):
        return u'{}.{}'.format(module, class_name)

    def get_backend(self):
        if self._backend is None:
            backend_module = importlib.import_module(
                getattr(settings, 'DJANGO_DATAWATCH_ASYNC_BACKEND',
                        defaults['ASYNC_BACKEND']))
            self._backend = backend_module.Backend()
        return self._backend

monitor = MonitoringHandler()


class Scheduler(object):
    def run_checks(self, force=False, slug=None):
        """
        :param force: <bool> force all registered checks to be executed
        :return:
        """
        now = timezone.now()
        checks = monitor.get_all_registered_checks()
        last_executions = self.get_last_executions()

        for check_class in checks:
            check = check_class()

            # only update a single slug if requested
            if slug and check.slug != slug:
                continue

            # check is not meant to be run periodically
            if not isinstance(check_class.run_every, relativedelta):
                continue

            # shall the check be run again?
            if not force and check.slug in last_executions:
                if now < last_executions[check.slug] + check.run_every:
                    continue

            # enqueue the check and save execution state
            check.run()

    def get_last_executions(self):
        from django_datawatch.models import CheckExecution
        return dict([(obj.slug, obj.last_run)
                     for obj in CheckExecution.objects.all()])

    def update_related(self, sender, instance):
        backend = monitor.get_backend()
        checks = monitor.get_checks_for_model(sender) or []
        for check_class in checks:
            check = check_class()
            model_uid = make_model_uid(instance.__class__)
            mapping = check.get_trigger_update_uid_map()

            if model_uid not in mapping:
                continue

            if not hasattr(check, mapping[model_uid]):
                continue

            payload = getattr(check, mapping[model_uid])(instance)
            if not payload:
                continue

            backend.run(slug=check.slug,
                        identifier=check.get_identifier(payload),
                        async=True)


def make_model_uid(model):
    """
    Returns an uid that will identify the given model class.

    :param model: model class
    :return: uid (string)
    """
    return "%s.%s" % (model._meta.app_label, model.__name__)


def run_checks(sender, instance, created, raw, using, **kwargs):
    """
    Re-execute checks related to the given sender model, only for the
    updated instance.

    :param sender: model
    :param kwargs:
    """
    if not getattr(settings, 'DJANGO_DATAWATCH_RUN_POST_SAVE_SIGNALS',
                   defaults['RUN_POST_SAVE_SIGNALS']):
        return
    Scheduler().update_related(sender, instance)
