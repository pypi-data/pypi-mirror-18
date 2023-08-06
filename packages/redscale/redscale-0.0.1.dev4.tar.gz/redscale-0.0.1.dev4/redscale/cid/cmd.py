# Copyright 2016 Arie Bregman
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
import argparse
import logging
from novaclient import client
import sys

from redscale.app import RedScaleApp
import redscale.exc as exc

LOG = logging.getLogger('__main__')


class CID(RedScaleApp):

    def __init__(self):
        self.parser = self.create_parser()
        super(CID, self).__init__(name='cid', parser=self.parser)

        self.auth = super(CID, self).create_auth(self.args.cloud)
        self.session = super(CID, self).create_session(self.auth)
        self.novac = client.Client(2, session=self.session)

    def can_i_deploy(self, memory, vcpu, limits):
        """Returns True if there are enough resources to deploy."""

        available_vcpu = limits['absolute']['maxTotalCores'] - limits[
            'absolute']['totalCoresUsed']
        available_ram = (limits['absolute']['maxTotalRAMSize'] - limits[
            'absolute']['totalRAMUsed']) / 1000

        LOG.info("Available VCPUs: %s", available_vcpu)
        LOG.info("Available RAM: %s", available_ram)

        return (available_ram > memory or available_vcpu > vcpu)

    def convert_to_resources(self, used_flavor, amount):
        """Returns memory and number of vcpu for given flavor

        and the amount usage of the flavor.
        """

        flavors = self.novac.flavors.list()
        for flavor in flavors:
            if flavor.name == used_flavor:
                return flavor.ram*amount, flavor.vcpus*amount
        raise exc.RedScaleException("Couldn't find the specified flavor: %s",
                                used_flavor)

    def create_parser(self):
        """Add CID unique arguments."""
        parser = argparse.ArgumentParser()

        parser.add_argument('--memory', '-m', dest='memory',
                            help='the total number of memory')
        parser.add_argument('--vcpu', '-v', dest='cpu',
                            help='the total number of vcpu')
        parser.add_argument('--flavor', '-f', dest='flavor',
                            help='the name of the flavor')
        parser.add_argument('--amount', '-a', dest='amount', type=int,
                            help='the amount of nodes using the specified \
                            flavor')

        return parser

    def run(self):
        """Run CID."""

        if (not self.args.flavor and not self.args.memory) or \
           (not self.args.amount and not self.args.cpu):
            raise exc.RedScaleException(
                "Please use (--memory and --cpu) OR \
(--flavor and --amount)")

        if self.args.flavor:
            memory, vcpu = self.convert_to_resources(
                self.args.flavor, self.args.amount)
        else:
            memory, vcpu = self.args.memory, self.args.cpu

        limits = self.novac.limits.get().to_dict()
        result = self.can_i_deploy(memory, vcpu, limits)

        if result:
            LOG.info("You may proceed :)")
        else:
            LOG.info("Stop before the lab explodes!")
            sys.exit(2)


def main():
    """CID main entry."""
    app = CID()
    app.run()

if __name__ == '__main__':
    sys.exit(main())
