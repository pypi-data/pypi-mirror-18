#
# Copyright (c) 2016, Nimbix, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Nimbix, Inc.
#

from collections import OrderedDict
from mimetypes import MimeTypes
import simplejson as json
import os
import base64


class AppDef():
    '''
    AppDef class - see method documentation below
    '''
    data = OrderedDict()

    def new(self, name, desc, author, licensed=True, machines=['*'],
            classifications=['Uncategorized'],
            vaults=['FILE', 'BLOCK', 'OBJECT'], image=None, templatefile=None):
        '''
        Creates a new AppDef initialized with meta data

        Required parameters:
            name(string):   the short name of the application
            desc(string):   the description of what the application does
            author(string): the author or vendor name for this application

        Optional parameters:
            licensed(bool):         True if the application contains license
                                    (if applicable);
                                    default: True
            machines(list):         list of machine types or wildcards
                                    the application can run on;
                                    default: *
            classifications(list):  list of classifications/categories the
                                    application belongs under;
                                    default: Uncategorized
            vaults(list):           list of vault types supported;
                                    default: FILE, BLOCK, and OBJECT
                                    also valid: NONE (for no vault) and
                                    BLOCK_ARRAY (for distributed FS)
            image(string):          graphic file with icon to embed (max 64kb)
                                    default: no graphic
                                    must be either png or jpg
            templatefile(string):   if set, load an existing JSON file as
                                    a baseline, rather than starting with
                                    a blank object
        '''
        assert(type(machines) == list and type(classifications) == list
               and type(vaults) == list)
        if templatefile:
            self.load(templatefile)
        else:
            self.data = OrderedDict()

        if 'commands' not in self.data:
            self.data['commands'] = OrderedDict()

        self.data['name'] = name
        self.data['description'] = desc
        self.data['author'] = desc
        self.data['licensed'] = licensed
        self.data['machines'] = machines
        self.data['classifications'] = classifications
        self.data['vault-types'] = vaults
        if image:
            self.image(image)
        elif 'image' not in self.data:
            self.data['image'] = OrderedDict()
            self.data['image']['type'] = 'image/png'
            self.data['image']['data'] = ''

    def load(self, filename):
        '''
        Creates an AppDef from an existing JSON file

        Required parameters:
            filename(string): file name to load
        '''
        with open(filename, 'r') as f:
            self.data = json.load(f, object_pairs_hook=OrderedDict)

    def image(self, filename):
        '''
        Encodes application image into AppDef

        Required parameters:
            filename(string):   image file name - must be png or jpg and <=64K
        '''
        m = MimeTypes()
        mime, other = m.guess_type(filename)
        assert(mime == 'image/png' or mime == 'image/jpeg')
        assert(os.stat(filename).st_size <= 65536)
        self.data['image'] = OrderedDict()
        self.data['image']['type'] = mime
        with open(filename, 'r') as f:
            self.data['image']['data'] = base64.encodestring(f.read())

    def cmd(self, id, desc, path, interactive=True, name=None, args=[]):
        '''
        Adds a command with some optional constant positional arguments.
        A command maps an executable (and arguments) to an API endpoint with
        optional parameters.

        Required parameters:
            id(string):         command ID (should not have spaces)
            desc(string):       the description of what the command does

        Optional parameters:
            interactive(bool):  True if users should be able to reach the
                                runtime environment by public IP while running;
                                default: True
            name(string):       user-facing short name of the command
                                default: same as id
            args(list):         positional arguments for command
                                default: none

        Notes:
            - for security, set interactive=False for any command which does
              not require user interaction while running; stdout and stderr
              will still be available to user via API and web interface
            - positional arguments should be separated as if using exec()
              e.g.:
                ls -l /data
              should be added like this:
                cmd(<id>, <desc>, False, args=['-l', '/data'])
        '''
        self.data['commands'][id] = OrderedDict()
        self.data['commands'][id]['description'] = desc
        self.data['commands'][id]['interactive'] = interactive
        self.data['commands'][id]['name'] = name if name else id
        params = OrderedDict()
        index = 0
        if args:
            for i in args:
                arg = OrderedDict()
                argname = '__arg%d' % index
                index = index + 1
                arg['name'] = argname
                arg['description'] = argname
                arg['type'] = 'CONST'
                arg['value'] = i
                arg['positional'] = True
                arg['required'] = True
                params[argname] = arg
        self.data['commands'][id]['parameters'] = params

    def param(self, cmd, flag, paramdef):
        '''
        Adds a parameter to a command.

        Required parameters:
            cmd(string):                command name to add to (from cmd())
            flag(string):               flag name of parameter
            paramdef(string or dict):   parameter definition (JSON or dict)

        For parameter dictionary specification please see:
            https://www.nimbix.net/jarvice-application-deployment-guide/
        '''
        if type(paramdef) == str:
            paramdef = json.loads(paramdef)
        self.data['commands'][cmd]['parameters'][flag] = paramdef

    def dump(self, f=None):
        '''
        Dumps an appdef object as JSON either to a stream or a string.

        Optional parameters:
            f(stream):      stream to dump AppDef to;
                            default: return as string instead

        Returns:
            string without pretty-printing if f=None,
            or AppDef dumped if f is set
        '''
        if f is None:
            return json.dumps(self.data)
        else:
            json.dump(self.data, f, indent=4)
