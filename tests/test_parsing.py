import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from parsing import line_num, unscrub_name


def test_line_num():
    abs_path = os.path.abspath('tests/test_files/test.md')
    assert line_num('Pregunta 1', abs_path) is None
    assert line_num('Pregunta1', abs_path) == 0


def test_unscrub_name():
    assert unscrub_name('test_name') == 'test name'
