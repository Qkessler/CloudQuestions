import parsing
from data.session_factory import global_init
import os
from question_service import search_engine, questions_by_topic


if __name__ == '__main__':
    # dir_name = 'tests'
    # files = os.listdir('tests')
    # for f in files:
    #     parsing.parsing_markdown("/".join([dir_name, f]))
    # global_init()
    # topics = search_engine('test')
    # print(topics)
    # test_dict = parsing.parsing_markdown('test_files/test.md')
    # print(test_dict)
    file_name = 'test_files/test.md'
    test_dict = {'- Pregunta1':
                 'Esto es la respuesta1\nEsto es la segunda línea\n'}
    parsing.print_q_a(test_dict)
