from inout import inputoutput

import spacy
from nltk.tokenize import sent_tokenize

import os
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s')


def get_german_fiction_tokens(limit, nlp):
    logging.info('get german fiction tokens')
    dir = '../data/corpus-of-german-language-fiction/corpus-of-german-fiction-txt'
    all_tokens = list()
    tokens = list()
    ratio_sum = 0
    rounds = 0

    for file in os.listdir(dir):
        with open(dir + '/' + file, 'r', encoding='utf-8') as f:
            content = f.read()
            sent = sent_tokenize(content)
            for s in sent:
                doc = nlp(s)
                for t in doc:
                    lemma = t.lemma_.lower()
                    if lemma.upper().isupper():
                        tokens.append(lemma)
                        if len(tokens) == 1000:
                            ratio_sum += compute_ratio(tokens)
                            all_tokens.extend(tokens)
                            tokens = list()
                            rounds += 1

                        if len(all_tokens) >= limit:
                            ratio_avg = ratio_sum / rounds
                            types = set(all_tokens)
                            logging.info(str(len(all_tokens)) + ' tokens ' + str(len(types)) + ' types')
                            logging.info('corpus size:' + str(len(all_tokens)) + '\naverage ratio: ' + str(ratio_avg))
                            return
    # ratio_sum += compute_ratio(tokens)


def get_jobads_tokens(jobads, nlp):
    logging.info('get jobad tokens')
    # corpus_size = 0
    all_tokens = list()
    tokens = list()

    ratio_sum = 0
    rounds = 0

    for job in jobads:
        doc = nlp(job)

        for t in doc:
            lemma = t.lemma_.lower()
            if lemma.upper().isupper():
                tokens.append(lemma)
                if len(tokens) == 1000:
                    ratio_sum += compute_ratio(tokens)

                    all_tokens.extend(tokens)
                    tokens = list()
                    rounds += 1

    # print(all_tokens)
    ratio_sum += compute_ratio(tokens)
    all_tokens.extend(tokens)

    types = set(all_tokens)
    logging.info(str(len(all_tokens)) + ' tokens ' + str(len(types)) + ' types')

    ratio_avg = ratio_sum / rounds
    logging.info('corpus size:' + str(len(all_tokens)) + '\naverage ratio: ' + str(ratio_avg) + '\n\n')

    return all_tokens


def compute_ratio(tokens):
    types = set(tokens)
    ratio = len(types) / len(tokens)
    return ratio


logging.info('read jobads from sqlite')
sentences = inputoutput.read_jobads_content('../data/jobads/text_kernel_jobads.db')
logging.info(str(len(sentences)) +  ' jobads')

nlp = spacy.load('de_core_news_sm')
jobad_tokens = get_jobads_tokens(sentences, nlp)

fiction_tokens = get_german_fiction_tokens(len(jobad_tokens), nlp)