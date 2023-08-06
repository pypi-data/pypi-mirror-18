"""
Copyright (c) 2016 cloudover.io

This file is part of Thunder project.

cloudover.coreCluster is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from corecluster.utils.decorators import register
from corenetwork.utils.logger import log
from thunderscript.drivers.driver_corecluster import DriverCoreCluster
from thunderscript.drivers.driver_dummy import DriverDummy
from thunderscript.exceptions import *
from thunderscript.models.thunder import Call


@register(log=True, auth='token')
def call(context, script, variables):
    c = Call()
    c.script_name = script
    c.script_params = '\n'.join([str(p.key()) + '=' + str(p.value()) for p in variables])
    c.user = context.user
    c.state = 'init'
    c.save()

    d = DriverCoreCluster()
    d.variables = variables
    d.context = context
    d.debug = True
    d.recursion = 0

    c.state = 'in progress'
    c.save()
    try:
        d.cmd_require([script])
        c.state = 'done'
        c.variables = '\n'.join([str(p.key()) + '=' + str(p.value()) for p in d.variables])
        c.log = d.log
        c.save()
        return {'finished': 'script_done', 'log': d.log, 'variables': d.variables}
    except ScriptDone as e:
        d.cmd_require([script])
        c.state = 'done'
        c.variables = '\n'.join([str(p.key()) + '=' + str(p.value()) for p in d.variables])
        c.log = d.log
        c.save()
        return {'finished': 'script_done', 'log': d.log, 'variables': d.variables}
    except ScriptFailed as e:
        d.cmd_require([script])
        c.state = 'failed'
        c.variables = '\n'.join([str(p.key()) + '=' + str(p.value()) for p in d.variables])
        c.log = d.log
        c.save()
        return {'finished': str(e), 'log': d.log, 'variables': d.variables}
    except VariableException as e:
        d.cmd_require([script])
        c.state = 'variable missing'
        c.variables = '\n'.join([str(p.key()) + '=' + str(p.value()) for p in d.variables])
        c.log = d.log
        c.save()
        return {'finished': str(e), 'log': d.log, 'variables': d.variables}
    except Exception as e:
        d.cmd_require([script])
        c.state = 'failed'
        c.variables = '\n'.join([str(p.key()) + '=' + str(p.value()) for p in d.variables])
        c.log = d.log
        c.save()
        log(msg='Script failed', exception=e, tags=('thunder', 'error'))
        return {'finished': 'failed', 'log': d.log, 'variables': d.variables}


@register(log=True, auth='token')
def variables(context, script):
    d = DriverDummy()
    d.context = context
    d.debug = True
    d.recursion = 0
    d.variables = {}
    try:
        d.cmd_require([script])
    except:
        pass

    return {'log': d.log, 'variables': d.variables}
