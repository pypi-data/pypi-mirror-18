#!/usr/bin/env python
# Original Author: Mirantis. Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: Base class for writing Python plugins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import signal
import subprocess
import sys
import time
import traceback

class Base(object):
    
    def itermetrics(self):
        """
        Iterate over the collected metrics

        This class must be implemented by the subclass and should yield dict
        objects that represent the collected values. Each dict has 3 keys:
            - 'values', a scalar number or a list of numbers if the type
            defines several datasources.
        """
        raise NotImplemented("Must be implemented by the subclass!")

    def dispatch_metric(self, metric):
        values = metric['values']
        if not isinstance(values, list) and not isinstance(values, tuple):
            values = (values,)

        print values

    def execute(self, cmd, shell=True, cwd=None):
        """
        Executes a program with arguments.

        Args:
            cmd: a list of program arguments where the first item is the
            program name.
            shell: whether to use the shell as the program to execute (default=
            True).
            cwd: the directory to change to before running the program
            (default=None).

        Returns:
            A tuple containing the standard output and error strings if the
            program execution has been successful.

            ("foobar\n", "")

            None if the command couldn't be executed or returned a non-zero
            status code
        """
        start_time = time.time()
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=cwd,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            (stdout, stderr) = proc.communicate()
            stdout = stdout.rstrip('\n')
        except Exception as e:
            sys.stderr.write("Cannot execute command '%s': %s : %s" %
                              (cmd, str(e), traceback.format_exc()))
            return None

        returncode = proc.returncode

        if returncode != 0:
            sys.stderr.write("Command '%s' failed (return code %d): %s" %
                              (cmd, returncode, stderr))
            return None
        elapsedtime = time.time() - start_time

        sys.stderr.write("Command '%s' returned %s in %0.3fs" %
                         (cmd, returncode, elapsedtime))

        if not stdout and self.debug:
            sys.stderr.write("Command '%s' returned no output!", cmd)

        return (stdout, stderr)

    def execute_to_json(self, *args, **kwargs):
        """
        Executes a program and decodes the output as a JSON string.

        See execute().

        Returns:
            A Python object or None if the execution of the program failed.
        """
        outputs = self.execute(*args, **kwargs)
        if outputs:
            return json.loads(outputs[0])
        return
