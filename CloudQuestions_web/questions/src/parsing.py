import re
import os.path
from models.topic import Topic
from db_folder import session_factory
import questions.src.question_service as question_service
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pdb


# Patterns for parsing the markdown file.
pat_headers = re.compile(r'## .*')
pat_questions = re.compile(r'- .*')
pat_answers = re.compile(r'\s{4}.*')


# Function to create a tmp file to push into the db through
# the parsing_markdown function
def handling_uploaded_file(uploaded):
    tmp_path = f'tmp/{uploaded.name}'
    default_storage.save(tmp_path, ContentFile(uploaded.file.read()))
    full_tmp_path = os.path.join(settings.BASE_DIR, tmp_path)
    with open(full_tmp_path, 'wb') as f:
        for chunk in uploaded.chunks():
            f.write(chunk)
        print(full_tmp_path)
        parsing_markdown(full_tmp_path)
    default_storage.delete(full_tmp_path)


# Gets the line number of the line that contains the string given.
def line_num(string, _file):
    with open(_file) as f:
        for i, l in enumerate(f):
            if string in l:
                return i


# Unscrubs the name given.
def unscrub_name(name):
    chars = []
    for c in name:
        if c == '_':
            chars.append(' ')
        else:
            chars.append(c)
    return "".join(chars)


# Scrubs the name given to make sure it's compatible in the db.
def scrub_name(name):
    chars = []
    for c in name:
        if c == ' ':
            chars.append('_')
        elif c.isalnum():
            chars.append(c)
    return "".join(chars)


# Given a file as parameter, reads the lines and gets the questions,
# being the markdown toggles. After that, parses for each question,
# the answer below.
def parsing_markdown(file):
    # pdb.set_trace()
    return_file = {}
    with open(file, 'r') as f:
        file_lines = f.readlines()
    lines = file_lines
    questions = [q.strip('\n') for q in lines
                 if pat_questions.match(q)]
    base_name = os.path.basename(file)
    file_name = base_name.split('.')[0]
    s_name = scrub_name(file_name)
    return_file['file_name'] = s_name
    if questions:
        q_a = get_inside(questions, file)
        return_file['q_a'] = q_a
        include_questions(q_a, s_name)
    return return_file


# Inserting the questions and answers in the db.
def include_questions(q_a, topic_name):    # pragma: no cover
    session = session_factory.create_session()
    for q, a in q_a.items():
        if not question_service.same_questions(q, topic_name):
            topic = Topic()
            topic.question = q
            topic.answer = a
            topic.topic = topic_name
            session.add(topic)
    session.commit()
    session.close()


# Given a list of questions, we calculate the line numbers and add to
# the dictionary all that matches the answer pattern (4 spaces).
def get_inside(question_list, file):
    question_num = [line_num(q, file) for q in question_list]
    with open(file, 'r') as f:
        lines = f.readlines()
    clean_lines = []
    last_line = len(lines)
    for line in lines:
        if line != '\n':
            line.strip('\n')
        clean_lines.append(line)
    values = []
    for _ in question_num:
        v = []
        not_last = True
        while not_last and (pat_answers.match(clean_lines[_+1])
                            or clean_lines[_+1] == '\n'):
            not_last = (_ + 1 < (last_line - 1))
            v.append(clean_lines[_+1].strip('    '))
            _ += 1
        values.append("".join(v))
    inside = dict(zip(question_list, values))
    return inside


# Basic print function for a dict.
def print_q_a(q_a):
    for key, value in q_a.items():
        print(f'{key}:')
        print(f'{value}')
