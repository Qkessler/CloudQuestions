import app


if __name__ == '__main__':
    return_files = app.parsing_markdown('tests/SSL TLS.md')
    q_a = return_files['q_a']
    app.print_q_a(q_a)
    # app.random_question(q_a)
