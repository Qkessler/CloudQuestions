import re

pat_headers = re.compile(r'## .*')
pat_questions = re.compile(r'- .*')
pat_answers = re.compile(r'\s{4}.*')


def line_num(line, _file):
    with open(_file) as f:
        for i, l in enumerate(f):
            if line in l:
                return i


def parsing_markdown():
    with open('tests/SSL TLS.md', 'r') as f:
        lines = f.readlines()

    # Headers will be tables in the database.
    headers = [line for line in lines if pat_headers.match(line)]
    questions = [line for line in lines if pat_questions.match(line)]
    questions_stripped = [q.strip('\n') for q in questions]
    answers = [line for line in lines if pat_answers.match(line)]
    
