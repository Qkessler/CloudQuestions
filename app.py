import re

pat_headers = re.compile(r'## .*')
pat_questions = re.compile(r'- .*')
pat_answers = re.compile(r'\s{4}.*')


def line_num(line, _file):
    with open(_file) as f:
        for i, l in enumerate(f):
            if line in l:
                return i


def parsing_markdown(file):
    return_files = {}
    with open(file, 'r') as f:
        file_lines = f.readlines()
    lines = []
    for line in file_lines:
        # if line != '\n':
        #     line = line.strip('\n')
        lines.append(line)
    headers = [line for line in lines if pat_headers.match(line)]
    return_files['headers'] = headers
    questions = [q.strip('\n') for q in lines
                 if pat_questions.match(q)]
    questions_num = [line_num(q, file) for q in questions]
    print(questions_num)
    answers = []
    for _ in questions_num[:9]:
        answer = []
        while pat_answers.match(lines[_+2]) or lines[_+2] == '\n':
            answer.append(lines[_+2].strip('    '))
            _ += 1
        answers.append("".join(answer))
    q_a = dict(zip(questions, answers))
    return_files['q_a'] = q_a
    return return_files
