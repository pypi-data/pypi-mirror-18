import re
import textwrap
import os
"""
    Allows the execution of python code within any file.
    Requirements:
    The program will execute any code written within the two brackets
    <?python
        *code goes here*
    ?>

    Requires an empty line followed by a newline character after "<?python" and an empty line
    following a newline character before "?>"

    That is:
     *anything* <?python *optional empty space* *newline*
        *python code* *newline*
     *optional empty space* ?> *anything else*

     This will then be replaced by:
     *anything* *printed strings from the python code* *anything else*
"""


class Webbed:
    # regex for finding <?python .. ?>
    regex = '''<\?python([\t ]*\n)(?P<code>[\s\S]*?)\n[\t ]*\?>'''

    def __init__(self, path, globals=None):
        """
        Args:
            path (str): Path to file
            custom_vars (dict): Global variables to send to the file
        """
        self.path = path

        if globals is None:
            self.globals = {}
        else:
            self.globals = globals

        self.globals['print'] = self.print

        self._echo = ''

    def __call__(self, match):
        """ Used by re.sub
        Args:
            match: The match object
        """
        code = match.group('code')
        code = textwrap.dedent(code)

        exec(code, self.globals)

        replaced = match.expand(self._echo)
        self._echo = ''

        return replaced

    def execute(self):
        """
        Returns (str): The file with all python code executed
        """
        with open(self.path, 'r') as file:
            text = file.read()
        head, tail = os.path.split(os.path.abspath(self.path))
        primary_dir = os.getcwd()
        os.chdir(head)
        new_text = re.sub(self.regex, self, text)
        os.chdir(primary_dir)
        return new_text

    def print(self, *args, sep=' ', end='\n'):
        """ Used by the external file to tell what text to replace the python code with
        Args:
            sep (str):   string inserted between values, default a space.
            end (str):   string appended after the last value, default a newline.
        """

        self._echo += sep.join(map(str, args)) + end


def webbed(path, globals=None):
    return Webbed(path, globals).execute()
