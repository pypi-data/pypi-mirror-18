# Copyright (c) 2016 Huawei Technologies India Pvt.Limited.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import six

from osc_lib.command import command
from osc_lib import utils

from neutronclient.common import utils as nc_utils
from neutronclient.i18n import _

from networking_sfc.osc import common

LOG = logging.getLogger(__name__)

SFC_COMMON_PREFIX = "/sfc"
PORT_PAIR_GROUP_PATH = SFC_COMMON_PREFIX + "/port_pair_groups"
resource = 'port_pair_group'


class CreatePortPairGroup(command.ShowOne):
    """Create a Port Pair Group."""

    def get_parser(self, prog_name):
        parser = super(CreatePortPairGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='NAME',
            help=_('Name of the Port Pair Group.'))
        parser.add_argument(
            '--description',
            help=_('Description for the Port Pair Group.'))
        parser.add_argument(
            '--port-pair',
            metavar='PORT-PAIR',
            dest='port_pairs',
            default=[],
            action='append',
            help=_('ID or name of the Port Pair.'
                   'This option can be repeated.'))
        parser.add_argument(
            '--port-pair-group-parameters',
            metavar=(
                'type=TYPE[,service_type=SERVICE_TYPE'
                ',lb_fields=LB_FIELDS]'),
            type=nc_utils.str2dict,
            help=_('Dictionary of Port pair group parameters. '
                   'Currently, only service_type=[l2,l3] and '
                   '\'&\' separated string of the lb_fields '
                   'are supported.'))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        attrs = _get_common_attrs(self, self.app.client_manager, parsed_args)
        obj = common.create_sfc_resource(self, client, resource, attrs)
        columns = _get_columns(obj[resource])
        data = utils.get_dict_properties(obj[resource], columns)
        return columns, data


class UpdatePortPairGroup(command.Command):
    """Update Port Pair Group's information."""

    def get_parser(self, prog_name):
        parser = super(UpdatePortPairGroup, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='NAME',
            help=_('Name of the Port Pair Group.'))
        parser.add_argument(
            '--description',
            help=_('Description for the Port Pair Group.'))
        parser.add_argument(
            '--port-pair',
            metavar="PORT_PAIR",
            dest='port_pairs',
            default=[],
            action='append',
            help=_('ID or name of the Port Pair.'
                   'This option can be repeated.'))
        parser.add_argument(
            'port_pair_group',
            metavar="PORT_PAIR_GROUP",
            help=_("ID or name of the Port Pair Group to update."))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        id = common.find_sfc_resource(self, client, resource,
                                      parsed_args.port_pair_group)
        attrs = _get_common_attrs(self, self.app.client_manager, parsed_args,
                                  is_create=False)
        common.update_sfc_resource(self, client, resource, attrs, id)


class DeletePortPairGroup(command.Command):
    """Delete a given Port Pair Group."""

    def get_parser(self, prog_name):
        parser = super(DeletePortPairGroup, self).get_parser(prog_name)
        parser.add_argument(
            'port_pair_group',
            metavar="PORT_PAIR_GROUP",
            help=_("ID or name of the Port Pair Group to delete.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        id = common.find_sfc_resource(self, client, resource,
                                      parsed_args.port_pair_group)
        common.delete_sfc_resource(self, client, resource, id)


class ListPortPairGroup(command.Lister):
    """List Port Pair Groups."""

    def take_action(self, parsed_args):
        data = self.app.client_manager.neutronclient.list_ext(
            collection='port_pair_groups', path=PORT_PAIR_GROUP_PATH,
            retrieve_all=True)
        headers = ('ID', 'Name', 'Port Pair', 'Port Pair Group Parameters')
        columns = ('id', 'name', 'port_pairs', 'port_pair_group_parameters')
        return (headers,
                (utils.get_dict_properties(
                    s, columns,
                ) for s in data['port_pair_groups']))


class ShowPortPairGroup(command.ShowOne):
    """Show information of a given Port Pair Groups."""

    def get_parser(self, prog_name):
        parser = super(ShowPortPairGroup, self).get_parser(prog_name)
        parser.add_argument(
            'port_pair_group',
            metavar="PORT_PAIR_GROUP",
            help=_("ID or name of the Port Pair Group to display.)")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        id = common.find_sfc_resource(self, client, resource,
                                      parsed_args.port_pair_group)
        obj = common.show_sfc_resource(self, client, resource, id)
        columns = _get_columns(obj[resource])
        data = utils.get_dict_properties(obj[resource], columns)
        return columns, data


def _get_columns(item):
    return tuple(sorted(list(item.keys())))


def _get_ppg_param(attrs, ppg):
    attrs['port_pair_group_parameters'] = {}
    for key, value in six.iteritems(ppg):
        if key == 'lb_fields':
            attrs['port_pair_group_parameters'][key] = ([
                field for field in value.split('&') if field])
        else:
            attrs['port_pair_group_parameters'][key] = value
    return attrs['port_pair_group_parameters'][key]


def _get_common_attrs(self, client_manager, parsed_args, is_create=True):
    attrs = {}
    if parsed_args.name is not None:
        attrs['name'] = str(parsed_args.name)
    if parsed_args.description is not None:
        attrs['description'] = str(parsed_args.description)
    if parsed_args.port_pairs:
        attrs['port_pairs'] = [(common.find_sfc_resource(self,
                                client_manager.neutronclient, 'port_pair', pp))
                               for pp in parsed_args.port_pairs]
    if is_create is True:
        _get_attrs(client_manager, attrs, parsed_args)
    return attrs


def _get_attrs(client_manager, attrs, parsed_args):

    if ('port_pair_group_parameters' in parsed_args and
            parsed_args.port_pair_group_parameters is not None):
        attrs['port_pair_group_parameters'] = (
            _get_ppg_param(attrs, parsed_args.port_pair_group_parameters))
