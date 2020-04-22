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
    file = 'tests/SSL TLS.md'
    with open(file, 'r') as f:
        lines = f.readlines()

    # Headers will be tables in the database.
    headers = [line for line in lines if pat_headers.match(line)]
    questions = [q.strip('\n') for q in lines
                 if pat_questions.match(q)]
    # answers = [line for line in lines if pat_answers.match(line)]
    questions_num = [line_num(q, file) for q in questions]
    print(questions_num)
    for _ in questions_num:
        
