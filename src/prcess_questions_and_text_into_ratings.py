file = 'questions'

questions = []
texts = []

lines = open(file).readlines()
for line in lines:
    if line.startswith('question: '):
        line = line.replace('question: ', '')
        questions.append(line)
    if line.startswith('text: '):
        line = line.replace('text: ', '')
        texts.append(line)

assert len(texts) == len(questions)


def process_question(q):
    q = q.replace("'", "`").replace(',', ';;').replace('\n', '')
    return f'<h4><b>{q}?</b></h4>'



def process_text(t):
    return t.replace("'", "`").replace(',', ';;').replace('\n', '')


print('\n'.join([process_question(q) + process_text(t) for q, t in zip(questions, texts)]))
