import os
import parsing
from pytest import raises


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
                  'Esto es la respuesta1\nEsto es la segunda línea\n'},
                 'file_name': 'test'}
    assert parsing.parsing_markdown('test_files/test.md') == test_dict
    assert raises(FileNotFoundError,
                  parsing.parsing_markdown, 'file_not_existent')


def tests_get_inside():
    test_dict = {'- Pregunta1':
                 'Esto es la respuesta1\nEsto es la segunda línea\n'}
    file_name = 'test_files/test.md'
    questions = ['- Pregunta1']
    assert raises(FileNotFoundError,
                  parsing.get_inside, [], 'file_not_existent')
    assert parsing.get_inside(questions, file_name) == test_dict


def test_print_q_a(capfd):
    test_dict = {'- Pregunta1':
                 'Esto es la respuesta1\nEsto es la segunda línea\n'}
    parsing.print_q_a(test_dict)
    out, err = capfd.readouterr()
    assert out == """- Pregunta1:
Esto es la respuesta1
Esto es la segunda línea\n\n"""
