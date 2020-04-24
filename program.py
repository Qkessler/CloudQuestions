import parsing
from data.session_factory import global_init

if __name__ == '__main__':
    return_file = parsing.parsing_markdown('tests/SSL TLS.md')
    # q_a = return_file['q_a']
    # print(return_file)
    # parsing.print_q_a(q_a)
    # parsing.random_question(q_a)
    global_init()
