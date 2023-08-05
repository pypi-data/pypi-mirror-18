# Copyright (C) 2014 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import uuid
from datetime import datetime
import json
import tempfile
import os

import zmq.green as zmq
import gevent

import beeswarm.shared
from beeswarm.server.db import database_setup
from beeswarm.server.db.entities import Honeypot, Client
from beeswarm.server.db.entities import Session
from beeswarm.drones.honeypot.models.session import Session as HoneypotSession
from beeswarm.shared.socket_enum import SocketNames
from beeswarm.shared.message_enum import Messages
from beeswarm.server.db.database_actor import DatabaseActor
from beeswarm.drones.client.models.session import BaitSession
from beeswarm.server.misc.config_actor import ConfigActor
from beeswarm.shared.helpers import send_zmq_request_socket



class ClassifierTests(unittest.TestCase):
    def setUp(self):
        beeswarm.shared.zmq_context = zmq.Context()
        fd, self.db_file = tempfile.mkstemp()
        os.close(fd)
        connection_string = 'sqlite:///{0}'.format(self.db_file)
        os.remove(self.db_file)
        database_setup.setup_db(connection_string)

    def tearDown(self):
        if os.path.isfile(self.db_file):
            os.remove(self.db_file)

    def test_matching_quick_succession(self):
        """
        Tests that attack sessions coming in quick succession are classified correctly.
        This test relates to issue #218
        """

        honeypot_id = 1
        honeypot = Honeypot(id=honeypot_id)

        db_session = database_setup.get_session()
        db_session.add(honeypot)
        db_session.commit()

        drone_data_socket = beeswarm.shared.zmq_context.socket(zmq.PUB)
        drone_data_socket.bind(SocketNames.DRONE_DATA.value)

        # startup session database
        database_actor = DatabaseActor(999, delay_seconds=2)
        database_actor.start()
        gevent.sleep(1)

        for x in xrange(0, 100):
            honeypot_session = HoneypotSession(source_ip='192.168.100.22', source_port=52311, protocol='pop3', users={},
                                               destination_port=110)
            honeypot_session.add_auth_attempt('plaintext', True, username='james', password='bond')
            honeypot_session.honeypot_id = honeypot_id
            drone_data_socket.send('{0} {1} {2}'.format(Messages.SESSION_HONEYPOT.value, honeypot_id,
                                                            json.dumps(honeypot_session.to_dict(), default=json_default,
                                                            ensure_ascii=False)))

        gevent.sleep(1)
        database_actor_request_socket = beeswarm.shared.zmq_context.socket(zmq.REQ)
        database_actor_request_socket.connect(SocketNames.DATABASE_REQUESTS.value)
        sessions = send_zmq_request_socket(database_actor_request_socket, '{0}'.format(Messages.GET_SESSIONS_ALL.value))

        for session in sessions:
            self.assertEqual(session['classification'], 'Bruteforce')

        self.assertEqual(len(sessions), 100)

    def test_bait_classification_honeypot_first(self):
        """
        Tests that bait sessions are paired correctly with their honeypot counter parts when honeypot message arrives
        first.
        """

        self.populate_bait(True)
        # TODO: Use message request - not orm access!
        db_session = database_setup.get_session()
        sessions = db_session.query(Session).all()
        for session in sessions:
            self.assertEqual(session.classification_id, 'bait_session')

        self.assertEqual(len(sessions), 1)

    def test_bait_classification_client_first(self):
        """
        Tests that bait sessions are paired correctly with their honeypot counter parts when client message arrives
        first.
        """

        self.populate_bait(False)
        # TODO: Use message request - not orm access!
        db_session = database_setup.get_session()
        sessions = db_session.query(Session).all()
        for session in sessions:
            self.assertEqual(session.classification_id, 'bait_session')

        self.assertEqual(len(sessions), 1)

    def populate_bait(self, honeypot_first):
        honeypot_id = 1
        client_id = 2
        honeypot = Honeypot(id=honeypot_id)
        client = Client(id=client_id)

        db_session = database_setup.get_session()
        db_session.add(honeypot)
        db_session.add(client)
        db_session.commit()

        drone_data_socket = beeswarm.shared.zmq_context.socket(zmq.PUB)
        drone_data_socket.bind(SocketNames.DRONE_DATA.value)

        fd, config_file = tempfile.mkstemp()
        os.close(fd)
        os.remove(config_file)
        # persistence actor needs to communicate with on config REQ/REP socket
        config_actor = ConfigActor(config_file, '')
        config_actor.start()

        # startup session database
        database_actor = DatabaseActor(999, delay_seconds=2)
        database_actor.start()
        gevent.sleep(1)

        BaitSession.client_id = client_id

        honeypot_session = HoneypotSession(source_ip='192.168.100.22', source_port=52311, protocol='pop3', users={},
                                           destination_port=110)
        honeypot_session.add_auth_attempt('plaintext', True, username='james', password='bond')
        honeypot_session.honeypot_id = honeypot_id

        bait_session = BaitSession('pop3', '1234', 110, honeypot_id)
        bait_session.add_auth_attempt('plaintext', True, username='james', password='bond')
        bait_session.honeypot_id = honeypot_id
        bait_session.did_connect = bait_session.did_login = bait_session.alldone = bait_session.did_complete = True

        if honeypot_first:
            drone_data_socket.send('{0} {1} {2}'.format(Messages.SESSION_HONEYPOT.value, honeypot_id,
                                                        json.dumps(honeypot_session.to_dict(), default=json_default,
                                                        ensure_ascii=False)))
            drone_data_socket.send('{0} {1} {2}'.format(Messages.SESSION_CLIENT.value, client_id,
                                                        json.dumps(bait_session.to_dict(), default=json_default,
                                                        ensure_ascii=False)))
        else:
            drone_data_socket.send('{0} {1} {2}'.format(Messages.SESSION_CLIENT.value, client_id,
                                                        json.dumps(bait_session.to_dict(), default=json_default,
                                                        ensure_ascii=False)))
            drone_data_socket.send('{0} {1} {2}'.format(Messages.SESSION_HONEYPOT.value, honeypot_id,
                                                        json.dumps(honeypot_session.to_dict(), default=json_default,
                                                        ensure_ascii=False)))


        # some time for the session actor to work
        gevent.sleep(2)
        config_actor.stop()
        database_actor.stop()
        if os.path.isfile(config_file):
            os.remove(config_file)


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    else:
        return None
