import re
import os.path
import questions.src.question_service as question_service
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import markdown


# Patterns for parsing the markdown file.
pat_headers = re.compile(r"## .*")
pat_questions1 = re.compile(r"- .*")
pat_questions2 = re.compile(r"\t.*")
pat_answers = re.compile(r"\s{4}.*")
pat_images = re.compile(r".*\!\[.*\].*")


# Function to create a tmp file to push into the db through
# the parsing_markdown function
def handling_uploaded_file(uploaded, user):
    tmp_path = f"tmp/{uploaded.name}"
    default_storage.save(tmp_path, ContentFile(uploaded.file.read()))
    full_tmp_path = os.path.join(settings.BASE_DIR, tmp_path)
    with open(full_tmp_path, "wb") as f:
        for chunk in uploaded.chunks():
            f.write(chunk)
    return_dict = parsing_markdown(full_tmp_path, user)
    default_storage.delete(full_tmp_path)
    return return_dict


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
        if c == "_":
            chars.append(" ")
        else:
            chars.append(c)
    return "".join(chars)


# Scrubs the name given to make sure it's compatible in the db.
def scrub_name(name):
    chars = []
    for c in name:
        if c == " ":
            chars.append("_")
        elif c.isalnum():
            chars.append(c)
    return "".join(chars)


# Given a file as parameter, reads the lines and gets the questions,
# being the markdown toggles. After that, parses for each question,
# the answer below.
def parsing_markdown(file, user):
    return_file = {}
    with open(file, "r") as uploaded_file:
        file_lines = uploaded_file.readlines()
    lines = file_lines
    questions = [
        " ".join(q.strip("\n").split(" ")[1:])
        for q in lines
        if pat_questions1.match(q) or pat_questions2.match(q)
    ]
    base_name = os.path.basename(file)
    file_name = base_name.split(".")[0]
    s_name = scrub_name(file_name)
    return_file["file_name"] = s_name
    if questions:
        q_a = get_inside(questions, file)
        return_file["q_a"] = q_a
        return_file["topic_id"] = question_service.include_questions(q_a, s_name, user)
    return return_file


# Given a list of questions, we calculate the line numbers and add to
# the dictionary all that matches the answer pattern (4 spaces).
def get_inside(question_list, file):
    question_num = [line_num(q, file) for q in question_list]
    with open(file, "r") as markdown_f:
        lines = markdown_f.readlines()
    clean_lines = []
    for line in lines:
        if line != "\n":
            line.strip("\n")
        if pat_images.match(line):
            continue
        clean_lines.append(line)
    answers = []
    last_line = len(clean_lines)
    for _ in question_num:
        answer = []
        not_last = True
        while not_last and (
            pat_answers.match(clean_lines[_ + 1]) or clean_lines[_ + 1] == "\n"
        ):
            not_last = _ + 1 < (last_line - 1)
            answer.append(clean_lines[_ + 1].strip("    "))
            _ += 1
        answers.append(markdown.markdown("".join(answer)))
    inside = dict(zip(question_list, answers))
    return inside


# Basic print function for a dict.
def print_q_a(q_a):
    for key, value in q_a.items():
        print(f"{key}:")
        print(f"{value}")
