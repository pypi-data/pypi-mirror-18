# Copyright © 2015,2016 STRG.AT GmbH, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

import score.serve
import os
import subprocess
import sys


class Worker(score.serve.Worker):

    def __init__(self, conf, host, port):
        self.conf = conf
        self.host = host
        self.port = port

    def prepare(self):
        """
        Implements the transition from STOPPED to PAUSED.
        """

    def start(self):
        """
        Implements the transition from PAUSED to RUNNING.
        """
        # TODO: host/port
        file = '%s/server/start.php' % os.path.dirname(__file__)
        self.process = subprocess.Popen(
            ['php', file], stdout=sys.stdout, stderr=sys.stderr)

    def stop(self):
        """
        Implements the transition from PAUSED to STOPPED.
        """

    def pause(self):
        """
        Implements the transition from RUNNING to PAUSED.
        """
        self.process.kill()

    def cleanup(self, exception):
        """
        Called when an exception occured. Due to the nature of threading, it is
        not entirely clear, in which state the worker was, when this specific
        exception occurred.
        """
