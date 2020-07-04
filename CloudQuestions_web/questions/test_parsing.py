import os
from src import parsing
from pytest import raises


def test_line_num():
    path = 'test_files/test.md'
    dir_path = os.path.dirname(os.path.abspath(__file__))
    test_path = '/'.join([dir_path, path])
    assert parsing.line_num('Pregunta 1', test_path) is None
    assert parsing.line_num('Pregunta1', test_path) == 0


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
    path = 'test_files/test.md'
    dir_path = os.path.dirname(os.path.abspath(__file__))
    test_path = '/'.join([dir_path, path])
    assert parsing.parsing_markdown(test_path) == test_dict
    assert raises(FileNotFoundError,
                  parsing.parsing_markdown, 'file_not_existent')


def tests_get_inside():
    test_dict = {'- Pregunta1':
                 'Esto es la respuesta1\nEsto es la segunda línea\n'}
    path = 'test_files/test.md'
    dir_path = os.path.dirname(os.path.abspath(__file__))
    test_path = '/'.join([dir_path, path])
    questions = ['- Pregunta1']
    assert raises(FileNotFoundError,
                  parsing.get_inside, [], 'file_not_existent')
    assert parsing.get_inside(questions, test_path) == test_dict


def test_print_q_a(capfd):
    test_dict = {'- Pregunta1':
                 'Esto es la respuesta1\nEsto es la segunda línea\n'}
    parsing.print_q_a(test_dict)
    out, err = capfd.readouterr()
    assert out == """- Pregunta1:
Esto es la respuesta1
Esto es la segunda línea\n\n"""
