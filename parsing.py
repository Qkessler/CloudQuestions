import re
import markdown
import os.path
from models.topic import Topic
from data import session_factory
from question_service import same_questions


pat_headers = re.compile(r'## .*')
pat_questions = re.compile(r'- .*')
pat_answers = re.compile(r'\s{4}.*')


def line_num(line, _file):
    with open(_file) as f:
        for i, l in enumerate(f):
            if line in l:
                return i


def scrub_name(name):
    chars = []
    for c in name:
        if c == ' ':
            chars.append('_')
        elif c.isalnum():
            chars.append(c)
    return "".join(chars)


def parsing_markdown(file):
    return_file = {}
    with open(file, 'r') as f:
        file_lines = f.readlines()
    lines = file_lines
    questions = [q.strip('\n') for q in lines
                 if pat_questions.match(q)]
    q_a = get_inside(questions, file)
    return_file['q_a'] = q_a
    base_name = os.path.basename(file)
    file_name = base_name.split('.')[0]
    s_name = scrub_name(file_name)
    return_file['file_name'] = s_name

    # Getting the questions and answers in the db.
    session = session_factory.create_session()
    for q, a in q_a.items():
        if not same_questions(q, s_name):
            topic = Topic()
            topic.question = q
            topic.answer = a
            topic.topic = s_name
            session.add(topic)
    session.commit()
    session.close()

    return return_file


def get_inside(mark, file):
    mark_num = [line_num(q, file) for q in mark]
    with open(file, 'r') as f:
        lines = f.readlines()
    clean_lines = []
    last_line = len(lines)
    for line in lines:
        if line != '\n':
            line.strip('\n')
        clean_lines.append(line)
    values = []
    for _ in mark_num:
        v = []
        not_last = True
        while not_last and (pat_answers.match(clean_lines[_+1])
                            or clean_lines[_+1] == '\n'):
            not_last = (_ + 1 < (last_line - 1))
            v.append(clean_lines[_+1].strip('    '))
            _ += 1
        values.append("".join(v))
    inside = dict(zip(mark, values))
    return inside


def print_q_a(q_a):
    for key, value in q_a.items():
        print(f'{key}:')
        print(f'{value}')


def html_translator(answer):
    html = markdown.markdown(answer)
    print(html)
