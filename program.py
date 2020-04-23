import app

if __name__ == '__main__':
    return_file = app.parsing_markdown('tests/SSL TLS.md')
    q_a = return_file['q_a']
    print(return_file)
    app.print_q_a(q_a)
    app.random_question(q_a)
