import sqlite3 as sql
from collections import defaultdict
import spacy
from nltk.corpus import stopwords
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s')

sw_set = set(stopwords.words('german'))

# alle als Elternelemente relevanten POS-Tags
rel_pos = ['PROPN', 'NOUN', 'ADJ', 'VERB', 'AUX', 'ADV', 'X']

# alle Modi für die Merkmalsauswahl
modes = ['dep', 'seq', 'comp']


def get_dependency_features(sentence, comp):
    comp_pos = ''
    verb = ''
    head = ''

    # Auswahl der Merkmale für den Satz
    for t in sentence:
        if t.lemma_.lower() == comp:
            comp_pos = t.pos_
            comp_index = t.i
            # falls Kompetenz selbst Teil von Konjunkt ist
            if t.dep_ == 'cj':
                head = t.head.head.head
            else:
                head = t.head

            # Dependenzbaum aufwärts bis zu relevanter Wortart
            while head.pos_ not in rel_pos:
                head = head.head
                if head == sentence.root:
                    break

            head = head.lemma_

            # print(t, head, '\t', doc)

        if t.pos_ == 'VERB':
            verb = t.lemma_
    features = dict(comp=comp, head=head)
    return features


def get_sequencial_features(sentence, comp, doc):
    # keep only content tokens and identify index of competence
    content_tokens = list()
    for t in sentence:
        if t.lemma_.lower() not in sw_set:
            content_tokens.append(t)
            if t.lemma_.lower() == comp.lower():
                comp_index = len(content_tokens) - 1

    context = list()

    if comp_index == -1:
        logging.info('no comp in doc: ' + comp + ' ** ' + doc)
        for i in range(4):
            context.append('')

    else:
        for i in range(comp_index - 2, comp_index + 3):
            if i < 0:
                context.append('_empty')

            elif i != comp_index:
                try:
                    context.append(content_tokens[i].lemma_)
                except IndexError:
                    context.append('_empty_')
    features = dict(cm2=context[0], cm1=context[1], cp1=context[2], cp2=context[3])
    return features


def process_row(doc, comp, feature_mode):

    if feature_mode not in modes:
        logging.info('unknown mode. switch to dependency mode')
        feature_mode = 'dep'

    sentence = None

    sentences = list(doc.sents)
    # if more than one sentence chose the one containing competence
    if len(sentences) > 1:
        for s in sentences:
            for t in s:
                if t.lemma_.lower() == comp.lower():
                    sentence = s
                    break
    else:
        sentence = sentences[0]

    if feature_mode == 'dep':
        return get_dependency_features(sentence, comp)
    elif feature_mode == 'seq':
        return get_sequencial_features(sentence, comp, doc)
    elif feature_mode == 'comp':
        return dict(comp=comp)


def build_matrix(file, feature_mode):
    """
    creates a matrix with all manually annotated sentences

    :param file: SQLite-DB with classified sentences (0 or 1)
    :param feature_mode: "seq" = neighbor lemmas "dep" = dependency head
    :return: list of tuples containing featurelist, label, sentence
    """

    nlp = spacy.load('de_core_news_sm')

    conn = sql.connect(file)

    sql_select = """SELECT COMP, ISCOMP, SENTENCE FROM sentences WHERE ISCOMP!=-1"""

    c = conn.cursor()
    c.execute(sql_select)

    rows = c.fetchall()

    nltk_data = list()

    for r in rows:
        comp = r[0]
        label = r[1]
        sentence = r[2]

        sentence = sentence.replace('<comp>', '')
        sentence = sentence.replace('</comp>', '')
        doc = nlp(sentence)

        features = process_row(doc, comp, feature_mode)

        nltk_tuple = (features, label, sentence)
        nltk_data.append(nltk_tuple)

    return nltk_data