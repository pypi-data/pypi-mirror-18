# Copyright (c) 2016 Huawei Technologies India Pvt.Limited.
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
#
# Borrowed from nova code base, more utilities will be added/borrowed as and
# when needed.

from neutronclient.common import exceptions
from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronV20


def _resolve_resource_path(self, resource):
    """Returns sfc resource path."""

    if resource == 'port_pair':
        RESOURCE_PATH = "/sfc/port_pairs"

    elif resource == 'port_pair_group':
        RESOURCE_PATH = "/sfc/port_pair_groups"

    elif resource == 'port_chain':
        RESOURCE_PATH = "/sfc/port_chains"

    elif resource == 'flow_classifier':
        RESOURCE_PATH = "/sfc/flow_classifiers"

    return RESOURCE_PATH


def create_sfc_resource(self, client, resource, props):
    """Returns created sfc resource record."""
    path = _resolve_resource_path(self, resource)
    record = client.create_ext(path, {resource: props})
    return record


def update_sfc_resource(self, client, resource, prop_diff, resource_id):
    """Returns updated sfc resource record."""

    path = _resolve_resource_path(self, resource)
    return client.update_ext(path + '/%s', resource_id,
                                    {resource: prop_diff})


def delete_sfc_resource(self, client, resource, resource_id):
    """Deletes sfc resource record and returns status."""

    path = _resolve_resource_path(self, resource)
    return client.delete_ext(path + '/%s', resource_id)


def show_sfc_resource(self, client, resource, resource_id):
    """Returns specific sfc resource record."""

    path = _resolve_resource_path(self, resource)
    return client.show_ext(path + '/%s', resource_id)


def find_sfc_resource(self, client, resource, name_or_id):
    """Returns the id and validate sfc resource."""

    path = _resolve_resource_path(self, resource)

    try:
        record = client.show_ext(path + '/%s', name_or_id)
        return record.get(resource).get('id')
    except exceptions.NotFound:
        res_plural = resource + 's'
        record = client.list_ext(collection=res_plural,
                                 path=path, retrieve_all=True)
        record1 = record.get(res_plural)
        rec_chk = []
        for i in range(len(record1)):
            if (record1[i].get('name') == name_or_id):
                rec_chk.append(record1[i].get('id'))
        if len(rec_chk) > 1:
            raise exceptions.NeutronClientNoUniqueMatch(resource=resource,
                                                        name=name_or_id)
        elif len(rec_chk) == 0:
            not_found_message = (_("Unable to find %(resource)s with name "
                                   "or id '%(name_or_id)s'") %
                                 {'resource': resource,
                                  'name_or_id': name_or_id})
            raise exceptions.NotFound(message=not_found_message)
        else:
            return rec_chk[0]


def get_id(client, id_or_name, resource):
    return neutronV20.find_resourceid_by_name_or_id(
        client, resource, str(id_or_name))
