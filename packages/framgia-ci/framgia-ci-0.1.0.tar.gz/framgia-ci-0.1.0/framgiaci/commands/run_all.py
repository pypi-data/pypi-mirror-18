import sys
import os

from cleo import Command


class RunAllCommand(Command):
    """
    Running test, report, finish command

    run
    """

    def handle(self):
        self.app.check_configure_file_exists()
        for command in ['test', 'report', 'finish']:
            try:
                self.call(command)
            except SystemExit as exception:
                if exception.code:
                    sys.exit(exception.code)

        sys.exit(0)
