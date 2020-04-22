import re

pat_headers = re.compile(r'## .*')


def parsing_markdown():
    with open('tests/SSL TLS.md', 'r') as f:
        lines = f.readlines()
    headers = [line for line in lines if pat_headers.match(line)]
