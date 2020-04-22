import re

pat_headers = re.compile(r'## .*')
pat_questions = re.compile(r'- .*')


def parsing_markdown():
    with open('tests/SSL TLS.md', 'r') as f:
        lines = f.readlines()
    headers = [line for line in lines if pat_headers.match(line)]
    # questions = pat_questions.findall(str(lines))
    questions = [line for line in lines if pat_questions.match(line)]
    print([i.strip('\n') for i in questions])
    # questions_stripped = []
    # for q in questions:
    #     if q != '\\n':
    #         questions_stripped.append(q)
    # print(questions_stripped)
