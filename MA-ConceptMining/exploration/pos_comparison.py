import os
import spacy
from nltk.tokenize import sent_tokenize
from inout import inputoutput


def read_german_fiction(limit, nlp):
    # directory = os.fsencode('../data/corpus-of-german-language-fiction/corpus-of-german-fiction-txt')
    dir = '../data/corpus-of-german-language-fiction/corpus-of-german-fiction-txt'

    pos_tags = list()
    for file in os.listdir(dir):
        if '(19' not in file:
            continue
        with open(dir+'/'+file, 'r', encoding='utf-8') as f:
            content = f.read()
            sent = sent_tokenize(content)
            for s in sent:
                doc = nlp(s)
                for token in doc:
                    pos_tags.append(token.pos_)
                if len(pos_tags) >= limit:
                    return pos_tags
    return pos_tags


def process_text(jobads, nlp):
    pos_tags = list()
    x_tokens = set()
    for job in jobads:
        doc = nlp(job)
        for token in doc:
            if (token.pos_ == 'X'):#  & (len(token.text) < 2):
                x_tokens.add(token.text)
            # else:
            pos_tags.append(token.pos_)
    for x in x_tokens:
        print(x)

    return pos_tags


def compare_pos_tags():
    nlp = spacy.load('de_core_news_sm')

    print('read jobads from sqlite')
    jobads = inputoutput.read_jobads_content('../data/jobads/text_kernel_replaced_dev.db')
    # jobads = jobads[:300]
    job_pos = process_text(jobads, nlp)
    print(len(job_pos), ' job pos')
    print('read gutenberg corpus from .txt-files')
    gutenberg_pos = read_german_fiction(len(job_pos), nlp)

    job_set = set(job_pos)
    for s in job_set:
        count = job_pos.count(s)
        print(s, count)
    print('***************')
    print(len(gutenberg_pos), ' cglf')
    gut_set = set(gutenberg_pos)
    for s in gut_set:
        count = gutenberg_pos.count(s)
        print(s, count)


def get_pos_tokens(pos_tag):
    nlp = spacy.load('de_core_news_sm')

    tokens = list()
    print('read jobads')
    jobads = inputoutput.read_jobads_content('../data/jobads/text_kernel_replaced_dev.db')
    # jobads = jobads[:300]

    for job in jobads:
        doc = nlp(job)
        for t in doc:
            if t.pos_ == pos_tag:
                tokens.append(t.lemma_)

    return tokens

# compare_pos_tags()
adj = get_pos_tokens('ADJ')
adj_set = set(adj)
adj_dict = dict()

for a in adj_set:
    adj_dict[a] = adj.count(a)

sort = sorted(adj_dict.items(), key=lambda item: item[1])
for s in sort:
    print(s)

print('all ADJ:', len(adj))