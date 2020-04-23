import app

if __name__ == '__main__':
    q_a = app.parsing_markdown('tests/SSL TLS.md')
    app.print_q_a(q_a)
    # app.random_question(q_a)
