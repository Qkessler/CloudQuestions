import parsing
from data.session_factory import global_init
import os


if __name__ == '__main__':
    dir_name = 'tests'
    files = os.listdir('tests')
    for f in files:
        parsing.parsing_markdown("/".join([dir_name, f]))
    global_init()
