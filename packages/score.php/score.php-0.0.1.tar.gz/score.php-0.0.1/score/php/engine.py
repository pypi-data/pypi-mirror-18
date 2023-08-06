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

import os
import struct
from score.tpl.engine import Engine as EngineBase, EngineRenderer


class Engine(EngineBase):
    """
    :class:`score.tpl.Engine` for mustache files.
    """

    def __init__(self, conf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conf = conf

    def create_subrenderer(self, format, rootdir, cachedir):
        return DefaultRenderer(self, format, rootdir, cachedir)


class DefaultRenderer(EngineRenderer):
    """
    The :class:`<score.tpl.EngineRenderer>` for mustache templates.
    """

    def __init__(self, engine, format, rootdir, cachedir):
        self.engine = engine
        self.format = format
        self.rootdir = rootdir
        self.cachedir = cachedir
        self.globals = {}

    def add_function(self, name, value, escape_output=True):
        pass

    def add_filter(self, name, callback, escape_output=True):
        pass

    def add_global(self, name, value):
        self.globals[name] = value

    def render_string(self, string, variables):
        return '<NOT IMPLEMENTED>'

    def render_file(self, filepath, variables):
        variables = variables.copy()
        variables.update(self.globals)
        abspath = os.path.join(self.rootdir, filepath)
        connection = self.engine.conf.connect()
        connection.sendall(struct.pack('!bh', 1, len(abspath)) +
                           abspath.encode('UTF-8'))
        return self.read_result(connection)

    def read_result(self, connection):
        result = connection.recv(4096)
        connection.close()
        return str(result, 'UTF-8')
