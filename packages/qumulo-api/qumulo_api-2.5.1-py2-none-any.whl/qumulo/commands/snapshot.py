# Copyright (c) 2016 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
import datetime
import re

import qumulo.lib.opts
import qumulo.rest.snapshot as snapshot

EXPIRATION_HELP_MSG_TEMPLATE = "Time at which to expire the snapshot. " \
    "Providing an empty string {}indicates the snapshot should never be " \
    "expired. Format according to RFC 3339, which is a normalized subset of " \
    "ISO 8601. See http://tools.ietf.org/rfc/rfc3339.txt, section 5.6 for ABNF."

TTL_HELP = "Time to live for the snapshot in the form '#D' where # is a " \
    "positive number and D specifies the unit for #. Choices for D are "\
    "w -> weeks, d -> days, h -> hours, and m -> minutes."

DELTAMAP = {'w': 'weeks', 'd': 'days', 'h': 'hours', 'm': 'minutes'}

def expiration_msg(is_create):
    omit_msg = ""
    if (is_create):
        omit_msg = "or omitting this argument "
    return EXPIRATION_HELP_MSG_TEMPLATE.format(omit_msg)

# XXX scott: this will go away when we can send intervals to qfsd
def ttl_to_expiration(timetolive):
    match = re.match(r"([1-9]\d*)([wdhm])$", timetolive)
    if not match:
        raise argparse.ArgumentTypeError("Invalid format")
    deltaspec = { DELTAMAP[match.group(2)]: int(match.group(1)) }
    delta = datetime.timedelta(**deltaspec)
    expiration = datetime.datetime.utcnow() + delta
    return expiration.isoformat('T') + 'Z'

class CreateSnapshotCommand(qumulo.lib.opts.Subcommand):
    NAME = "snapshot_create_snapshot"

    DESCRIPTION = "Create a new snapshot."

    @staticmethod
    def options(parser):
        parser.add_argument("-n", "--name", type=str, default=None,
            help="Name of the snapshot.")
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument("-e", "--expiration", type=str, default=None,
            help=expiration_msg(True))
        group.add_argument("-t", "--timetolive", type=str, default=None,
            help=TTL_HELP)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.timetolive is not None:
            args.expiration = ttl_to_expiration(args.timetolive)

        print snapshot.create_snapshot(
            conninfo, credentials, args.name, args.expiration)

class ModifySnapshotCommand(qumulo.lib.opts.Subcommand):
    NAME = "snapshot_modify_snapshot"

    DESCRIPTION = "Modify an existing snapshot."

    @staticmethod
    def options(parser):
        parser.add_argument("-i", "--id", type=str, required=True,
            help="ID of the snapshot.")
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument("-e", "--expiration", type=str, default=None,
            help=expiration_msg(False))
        group.add_argument("-t", "--timetolive", type=str, default=None,
            help=TTL_HELP)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.timetolive is not None:
            args.expiration = ttl_to_expiration(args.timetolive)

        print snapshot.modify_snapshot(
            conninfo, credentials, args.id, args.expiration)

class ListAllSnapshotsCommand(qumulo.lib.opts.Subcommand):
    NAME = "snapshot_list_snapshots"

    DESCRIPTION = "Lists all snapshots."

    @staticmethod
    def main(conninfo, credentials, _args):
        print snapshot.list_snapshots(conninfo, credentials)

class ListSnapshotCommand(qumulo.lib.opts.Subcommand):
    NAME = "snapshot_list_snapshot"

    DESCRIPTION = "Lists a single snapshot."

    @staticmethod
    def options(parser):
        parser.add_argument("-i", "--id", type=int, required=True,
            help="Identifier of the snapshot to list.")

    @staticmethod
    def main(conninfo, credentials, args):
        print snapshot.list_snapshot(conninfo, credentials, args.id)

class DeleteSnapshotCommand(qumulo.lib.opts.Subcommand):
    NAME = "snapshot_delete_snapshot"

    DESCRIPTION = "Deletes a single snapshot."

    @staticmethod
    def options(parser):
        parser.add_argument("-i", "--id", type=int, required=True,
            help="Identifier of the snapshot to delete.")

    @staticmethod
    def main(conninfo, credentials, args):
        snapshot.delete_snapshot(conninfo, credentials, args.id)
