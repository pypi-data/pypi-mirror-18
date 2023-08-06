#!venv/bin/python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    my_app add <numberA> <numberB>
    my_app sub <numberA> <numberB>
    my_app div <numberA> <numberB>
    my_app multi <numberA> <numberB>
    my_app (-i | --interactive)
    my_app (-h | --help)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from functions import division, multiplication, subtraction, summation


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Mathematics(cmd.Cmd):
    intro = 'Welcome to my interactive program!'
    prompt = '<<MathKimo>> '
    file = None

    @docopt_cmd
    def do_add(self, arg):
        """Usage: add <numberA> <numberB>"""
        print(summation(arg['<numberA>'], arg['<numberB>']))

    @docopt_cmd
    def do_sub(self, arg):
        """Usage: sub <numberA> <numberB>"""
        print(subtraction(arg['<numberA>'], arg['<numberB>']))

    @docopt_cmd
    def do_div(self, arg):
        """Usage: div <numberA> <numberB>"""
        print(division(arg['<numberA>'], arg['<numberB>']))

    @docopt_cmd
    def do_multi(self, arg):
        """Usage: multi <numberA> <numberB>"""
        print(multiplication(arg['<numberA>'], arg['<numberB>']))

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        print(__doc__)
        Mathematics().cmdloop()
    except KeyboardInterrupt:
        print("Exiting App")
