from interface import implements
from .outputter import Outputter


class ConsoleOutputter(implements(Outputter)):
    def display_output(self, output):
        # prints output
        print()
        print(output)
        print()
