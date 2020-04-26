import os
import parsing


def test_line_num():
    abs_path = os.path.abspath('test_files/test.md')
    assert parsing.line_num('Pregunta 1', abs_path) is None
    assert parsing.line_num('Pregunta1', abs_path) == 0


def test_unscrub_name():
    assert parsing.unscrub_name('test_name') == 'test name'
    assert parsing.unscrub_name('test___name') == 'test   name'


def test_scrub_name():
    assert parsing.scrub_name('test%&$"  ') == 'test__'
    assert parsing.scrub_name('__$%tests___') == 'tests'
    assert parsing.scrub_name('REAL NAME') == 'REAL_NAME'


def test_parsing_markdown():
    test_dict = {'q_a':
                 {'- Pregunta1':
                  'Esto es la respuesta1\nEsto es la segunda línea\n\n\n'},
                 'file_name': 'test'}

    assert parsing.parsing_markdown('test_files/test.md') == test_dict
    assert parsing.parsing_markdown('non_existent_file')
