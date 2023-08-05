'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

from collections import defaultdict
from itertools import product
from typing import Optional, Dict, Any, Iterable, Tuple  # noqa

import six
from requests import Response  # noqa

from sxclient.operations.base import BaseOperation
from sxclient.models.query_parameters import QueryParameters


__all__ = ['GetVolumeACL', 'UpdateVolumeACL', 'SetVolumeACL']


def _dict_of_lists_to_tuples(dict_of_lists):
    # type: (Dict[Any, Iterable]) -> Iterable[Tuple[Any, Any]]
    for key, value_list in six.iteritems(dict_of_lists):
        for value in value_list:
            yield key, value


class GetVolumeACL(BaseOperation):
    '''
    Get volume's access control list.

    Required access: user with any kind of permissions for the volume.

    Query specific parameters:
      - volume -- name of the volume to get ACL of
    '''

    def _generate_query_params(self, volume):
        # type: (str) -> QueryParameters
        return QueryParameters(
            sx_verb='GET',
            path_items=[volume],
            bool_params={'manager'},
            dict_params={'o': 'acl'}
        )


class UpdateVolumeACL(BaseOperation):
    '''
    Update volume's access control list.

    Required access: volume manager.

    Query specific parameters:
      - volume -- name of the volume to change ACL of
      - actions -- dictionary consisting of at least one of 'grant-read',
        'grant-write', 'grant-manager', 'revoke-read', 'revoke-write',
        'revoke-manager' as keys, each having a list of user names as a value.
        Actions described in the dictionary will be applied on top of the
        existing ACL.
    '''

    def _generate_body(self, volume, actions):
        # type: (str, dict) -> dict
        return actions

    def _generate_query_params(self, volume, actions):
        # type: (str, dict) -> QueryParameters
        return QueryParameters(
            sx_verb='JOB_PUT',
            path_items=[volume],
            dict_params={'o': 'acl'}
        )


class SetVolumeACL(UpdateVolumeACL):
    '''
    Set volume's access control list, replacing the permissions for the
    specified users.

    Required access: volume manager.

    Query specific parameters:
      - volume -- name of the volume to change ACL of
      - permissions -- dictionary describing new permission sets for a group of
        users, containing usernames as keys and lists of permission names
        ('read', 'write', 'manager') as values.
    '''

    def _get_entries(self, users, permissions):
        # type: (Iterable, dict) -> Tuple[Iterable, set]
        perms = ('read', 'write', 'manager')
        possible_entries = product(users, perms)
        new_entries = set(_dict_of_lists_to_tuples(permissions))
        return possible_entries, new_entries

    def _generate_actions(self, possible_entries, new_entries):
        # type: (Iterable, set) -> dict
        actions = defaultdict(set)  # type: dict
        for entry in possible_entries:
            user, perm = entry
            if entry in new_entries:
                action = 'grant-'
            else:
                action = 'revoke-'
            actions[action + perm].add(user)

        return {
            key: list(value) for key, value in six.iteritems(actions)
        }

    def call(self, volume, permissions):
        # type: (str, dict) -> Response
        users = six.iterkeys(permissions)
        possible_entries, new_entries = self._get_entries(users, permissions)
        actions = self._generate_actions(possible_entries, new_entries)
        return super(SetVolumeACL, self).call(volume, actions)
