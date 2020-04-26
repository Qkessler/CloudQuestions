import pytest
import question_service


def test_questions_by_topic():
    test_dict = {'- Pregunta1':
                 'Esto es la respuesta1\nEsto es la segunda línea\n\n\n'}
    assert question_service.questions_by_topic('test') == test_dict
