import re
import random
import markdown

pat_headers = re.compile(r'## .*')
pat_questions = re.compile(r'- .*')
pat_answers = re.compile(r'\s{4}.*')


def line_num(line, _file):
    with open(_file) as f:
        for i, l in enumerate(f):
            if line in l:
                return i


def parsing_markdown(file):
    return_file = {}
    with open(file, 'r') as f:
        file_lines = f.readlines()
    lines = file_lines
    questions = [q.strip('\n') for q in lines
                 if pat_questions.match(q)]
    q_a = get_inside(questions, file)
    return_file['q_a'] = q_a
    return_file['file_name'] = 
    return return_file


def finalline_file(file):
    with open(file, 'r') as f:
        return len(f.readlines())


def get_inside(mark, file):
    mark_num = [line_num(q, file) for q in mark]
    print(mark_num)
    with open(file, 'r') as f:
        lines = f.readlines()
    clean_lines = []
    for line in lines:
        if line == '\n':
            line.strip('\n')
        clean_lines.append(line)
    values = []
    for _ in mark_num:
        v = []
        while (_ + 1 != finalline_file(file)) and (pat_answers.match(clean_lines[_+1])
                                                   or clean_lines[_+1] == '\n'):
            v.append(clean_lines[_+1].strip('    '))
            _ += 1
        values.append("".join(v))
    inside = dict(zip(mark, values))
    return inside


def random_question(q_a):
    random_q = random.randint(0, len(q_a.keys())-1)
    print(list(q_a.keys())[random_q])
    key = input('Press <ENTER> for answer: ')
    while key != '':
        key = input('Press <ENTER> for answer: ')
    print(list(q_a.values())[random_q])


def print_q_a(q_a):
    for key, value in q_a.items():
        print(f'{key}:')
        print(f'{value}')


def html_transalor(answer):
    html = markdown.markdown(answer)
    print(html)
