import parsing
from data.session_factory import global_init
import question_service


if __name__ == '__main__':
    return_file = parsing.parsing_markdown('tests/B4 2.md')
    global_init()
    print(question_service.questions_by_topic('SSL_TLS'))
