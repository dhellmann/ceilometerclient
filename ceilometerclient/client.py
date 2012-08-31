"""Client wrapper
"""

import copy

import requests


class Client(object):
    """Ceilometer client.
    """

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.version = 'v1'

    def _mk_url(self, path):
        return '/'.join([self.base_url,
                         self.version,
                         path.lstrip('/'),
                         ])

    def get_projects(self):
        """Returns list of project ids known to the server."""
        r = requests.get(self._mk_url('/projects'))
        return r.json.get('projects', [])

    def get_resources(self, project_id, start_timestamp=None,
                      end_timestamp=None):
        """Returns details about the named project."""
        args = {}
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = requests.get(self._mk_url('/projects/%s/resources' % project_id),
                         params=args)
        if r.status_code == requests.codes.not_found:
            raise ValueError('Unknown project %r' % project_id)
        return r.json.get('resources', [])

    def get_events(self, resource_id, meter, start_timestamp=None,
                      end_timestamp=None):
        """Returns events about the resource in the time range."""
        args = {}
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = requests.get(self._mk_url('/resources/%s/meters/%s' % (resource_id, meter)),
                         params=args)
        if r.status_code == requests.codes.not_found:
            raise ValueError('Unknown resource %r' % resource_id)
        return r.json.get('events', [])

    def get_resource_duration_info(self, resource_id, meter,
            start_timestamp=None, end_timestamp=None,
            search_offset=0,
            ):
        """Returns duration, min, and max timestamp of the resource
        for the given meter within the time range.
        """
        args = {'search_offset': search_offset,
                }
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = requests.get(self._mk_url('/resources/%s/meters/%s/duration' % (resource_id, meter)),
                         params=args)
        if r.status_code == requests.codes.not_found:
            raise ValueError('Unknown resource %r' % resource_id)
        return copy.copy(r.json)

