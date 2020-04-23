from app import parsing_markdown
import random


if __name__ == '__main__':
    return_files = parsing_markdown('tests/SSL TLS.md')
    q_a = return_files['q_a']
    print(q_a)
    random_q = random.randint(0, len(q_a.keys()))
    print(random_q)
    print(list(q_a.keys())[random_q])
    key = input('Press whatever for answer: ')
    if key:
        print(list(q_a.values())[random_q])
