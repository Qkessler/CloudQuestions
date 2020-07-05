import pytest
from src import question_service


# def test_same_questions():
#     question_str = '- Pregunta1'
#     question_wrong = '- This question doesn\'t exist'
#     assert question_service.same_questions(question_str, 'test')
#     assert not question_service.same_questions(question_wrong, 'test')


# def test_search_engine():
#     string = 'Pregunta1'
#     string_test = 'test'
#     string_error = 'Error'

#     assert question_service.search_engine(string_test) == ['test']
#     assert question_service.search_engine(string) == ['test']
#     assert question_service.search_engine(string_error) == []
