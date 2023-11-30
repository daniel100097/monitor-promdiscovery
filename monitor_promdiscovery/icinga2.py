# -*- coding: utf-8 -*-
"""
    Copyright (C) 2021  Opsdis AB

    This file is part of monitor-exporter.

    monitor-promdiscovery is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    monitor-promdiscovery is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with monitor-exporter.  If not, see <http://www.gnu.org/licenses/>.

"""
import json

import requests

from monitor_promdiscovery.hosts_by_hostgroup import HostByHostgroup
from monitor_promdiscovery.http_connection import factory as factory
from monitor_promdiscovery.system_request import SystemRequest as Request

requests.packages.urllib3.disable_warnings()


class Icincga2Config(HostByHostgroup):
    prefix = 'icinga2'

    def __init__(self, monitor):
        self.connection = factory(Icincga2Config.prefix, monitor)

        self.connection.headers = {'Content-Type': 'application/json', 'X-HTTP-Method-Override': 'GET'}

        self.hostgroup = monitor[Icincga2Config.prefix]['hostgroup']

    def get_hosts_by_hostgroup(self) -> list:
        """
        Get all hosts in a specific hostgroup.
        Return from Monitor is a json list e.g. [{"name":"google.se"},{"name":"sunet.se"}]
        :return:
        """

        hosts = set()
        all_hostgroups = []
        if type(self.hostgroup) == str:
            all_hostgroups.append(self.hostgroup)
        else:
            all_hostgroups = self.hostgroup

        for hostgroup in all_hostgroups:
            if hostgroup != '*':
                body = {"attrs": ["__name", "name"],
                        "filter": '\"{}\" in host.groups'.format(hostgroup) }
            else:
                body = {"attrs": ["__name", "name"]}

            request = Request(self.connection)
            response = request.post('/v1/objects/hosts', body)

            hosts_entries = json.loads(response)

            for host_entry in hosts_entries['results']:
                hosts.add(host_entry['attrs']['name'])

        return list(hosts)
