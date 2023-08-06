from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

import logging

from flexget import plugin
from flexget.config_schema import one_or_more
from flexget.event import event
from flexget.plugin import PluginWarning
from flexget.utils.template import RenderError, get_template

log = logging.getLogger('notify')

ENTRY_CONTAINERS = ['entries', 'accepted', 'rejected', 'failed', 'undecided']
DEFAULT_DICTS = {
    'task': {
        'message': 'Task returned {{ task.accepted|length }} accepted entries',
        'title': '{{ task_name }}',
        'url': ''
    },

    'entries': {
        'message': '{% if series_name is defined %}'
                   '{{ tvdb_series_name|d(series_name) }} '
                   '{{series_id}} {{tvdb_ep_name|d('')}}'
                   '{% elif imdb_name is defined %}'
                   '{{imdb_name}} {{imdb_year}}'
                   '{% elif title is defined %}'
                   '{{ title }}'
                   '{% endif %}',
        'url': '{% if imdb_url is defined %}'
               '{{imdb_url}}'
               '{% endif %}',
        'title': '{{ task_name }}'
    }
}


class Notify(object):
    schema = {
        'type': 'object',
        'properties': {
            'to': {'type': 'array', 'items':
                {'allOf': [
                    {'$ref': '/schema/plugins?group=notifiers'},
                    {'maxProperties': 1,
                     'error_maxProperties': 'Plugin options within notify plugin must be indented '
                                            '2 more spaces than the first letter of the plugin name.',
                     'minProperties': 1}]}},
            'scope': {'type': 'string', 'enum': ['task', 'entries'], 'default': 'entries'},
            'what': one_or_more({'type': 'string', 'enum': ENTRY_CONTAINERS}),
            'title': {'type': 'string'},
            'message': {'type': 'string'},
            'url': {'type': 'string'},
            'file_template': {'type': 'string'}
        },
        'required': ['to'],
        'additionalProperties': True
    }

    def prepare_config(self, config):
        config.setdefault('scope', 'entries')
        config.setdefault('what', ['accepted'])
        if not isinstance(config['what'], list):
            config['what'] = [config['what']]
        config.setdefault('title', DEFAULT_DICTS[config['scope']]['title'])
        config.setdefault('message', DEFAULT_DICTS[config['scope']]['message'])
        config.setdefault('url', DEFAULT_DICTS[config['scope']]['url'])
        return config

    @staticmethod
    def render_value(entity, data, attribute, default_dict, plugin_name=None):
        """
        Tries to render a template, fallback to default template and just value if unsuccessful

        :param entity: The entity to operate on, either `Entry` or `Task`
        :param data: The text to be rendered
        :param attribute: Attribute name to be fetched from the defaults
        :param default_dict: The default dict, depending on entity type
        :return: A rendered value or original value
        """
        result = data

        # Handles file templates
        if attribute == 'file_template':
            try:
                data = get_template(data, plugin_name)
            except ValueError as e:
                log.warning(e.args[0])
                return

        try:
            result = entity.render(data)
        except (RenderError, ValueError) as e:
            log.debug('failed to render: %s. Trying to fall back to default', e.args[0])
            try:
                if attribute in default_dict:
                    result = entity.render(default_dict[attribute])
            # Render error on defaults should not happen
            except RenderError as e:
                log.warning('default dict failed to render: %s. Reverting to original value.', e.args[0])
        else:
            log.debug('successfully rendered `%s` to %s', attribute, result)
        return result

    def send_notification(self, task, config):
        config = self.prepare_config(config)
        scope = config.pop('scope')
        what = config.pop('what')
        notifiers = config.pop('to')

        # Creating iterator based on config scope
        iterate_on = [getattr(task, container) for container in what] if scope == 'entries' else [[task]]

        for notifier in notifiers:
            for notifier_name, notifier_config in notifier.items():
                notifier = plugin.get_plugin_by_name(notifier_name).instance

                for container in iterate_on:
                    for entity in container:
                        notification_data = {}

                        # Iterate over all of Notify plugin attributes first
                        for attribute, value in config.items():
                            notification_data[attribute] = self.render_value(entity, value, attribute,
                                                                             DEFAULT_DICTS[scope])

                        # Iterate over specific plugin config, overriding any previously set attribute in message data
                        for attribute, value in notifier_config.items():
                            notification_data[attribute] = self.render_value(entity, value, attribute,
                                                                             DEFAULT_DICTS[scope], notifier_name)

                        # If a template was used, pass it to `message` attribute. This will allow all notifiers to use
                        # templates generically
                        if notification_data.get('file_template') is not None:
                            notification_data['message'] = notification_data.pop('file_template')

                        if not task.options.test:
                            log.debug('Sending a notification to `%s`', notifier_name)
                            try:
                                notifier.notify(**notification_data)
                            except PluginWarning as e:
                                log.warning('Error while sending notification to `%s`: %s', notifier_name, e.value)
                            else:
                                log.verbose('Successfully sent a notification to `%s`', notifier_name)
                        else:
                            log.info('Test mode, would have sent notification to `%s`:', notifier_name)
                            for attribute, data in notification_data.items():
                                log.info('%10s: %s', attribute, data)

    def on_task_start(self, task, config):
        # Suppress warnings about missing output plugins
        if 'output' not in task.suppress_warnings:
            task.suppress_warnings.append('output')

    on_task_exit = send_notification


@event('plugin.register')
def register_plugin():
    plugin.register(Notify, 'notify', api_ver=2)
