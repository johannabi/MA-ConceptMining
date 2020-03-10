import sqlite3 as sql
from collections import defaultdict
import spacy
from nltk.corpus import stopwords

sw_set = set(stopwords.words('german'))


def process_row(doc, comp):

    # features to collect
    comp_pos = ''
    verb = ''
    head = ''
    index = -1

    # alle als Elternelemente relevanten POS-Tags
    rel_pos = ['PROPN', 'NOUN', 'ADJ', 'VERB', 'AUX', 'ADV', 'X']

    sentence = None

    sentences = list(doc.sents)
    # falls die Zeile mehrere Sätze enthält, wird der mit der Kompetenz ausgewählt
    if len(sentences) > 1:
        for s in sentences:
            for t in s:
                if t.lemma_.lower() == comp.lower():
                    sentence = s
                    break
    else:
        sentence = sentences[0]

    if sentence == None:
        print('****', comp, doc)

    # Auswahl der Merkmale für den Satz
    for t in sentence:
        if t.lemma_.lower() == comp:
            comp_pos = t.pos_
            index = t.i
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

    # for t in doc:
    #     if t.lemma_.lower() == comp:
    #         comp_pos = t.pos_
    #         index = t.i
    #         # falls Kompetenz selbst Teil von Konjunkt ist
    #         if t.dep_ == 'cj':
    #             # print(t.head, '\t\t', doc)
    #             head = t.head.head.head
    #             # print(t, head)
    #         else:
    #             head = t.head
    #
    #         while head.pos_ not in rel_pos:
    #             print(head.pos_)
    #             head = head.head
    #             if head == doc.root:
    #                 break
    #
    #         head = head.lemma_
    #
    #         print(t, head, '\t', doc)
    #
    #     if t.pos_ == 'VERB':
    #         verb = t.lemma_

    # print("text: ", doc.text)

    context = list()

    if index == -1:
        for i in range(4):
            context.append('')

    # print(index-2, ' ', index+2)
    else:

        content_tokens = list()
        for t in sentence:
            if t.lemma_.lower() not in sw_set:
                content_tokens.append(t)
                if t.lemma_.lower() == comp.lower():
                    index = len(content_tokens) - 1

        for i in range(index-2, index+3):

            if i < 0:
                context.append('_empty')

            elif i != index:
                try:
                    context.append(content_tokens[i].lemma_)
                except IndexError:
                    context.append('_empty_')

    # print("kontext: ", context)

    return comp, verb, head, comp_pos, context


def build_matrix(file):
    nlp = spacy.load('de_core_news_sm')

    conn = sql.connect(file)

    sql_select = """SELECT COMP, ISCOMP, SENTENCE FROM sentences WHERE ISCOMP!=-1"""

    c = conn.cursor()
    c.execute(sql_select)

    rows = c.fetchall()

    sentences = list()
    sentence_labels = list()

    features_dict = defaultdict(list)
    nltk_data = list()

    for r in rows:
        comp = r[0]
        label = r[1]
        sentence = r[2]

        sentences.append(sentence)
        sentence_labels.append(r[1])

        sentence = sentence.replace('<comp>', '')
        sentence = sentence.replace('</comp>', '')
        doc = nlp(sentence)

        comp, verb, head, comp_pos, context = process_row(doc, comp)

        # t[0] = vector t[1] = label t[2] = sentence
        # features = dict(comp=comp, head=head, pos=comp_pos)
        features = dict(comp=comp, head=head)
        # features = dict(cm2=context[0], cm1=context[1], cp1=context[2], cp2=context[3])
        # features = dict(comp=comp, verb=verb, head=head, pos=comp_pos, cm2=context[0], cm1=context[1], cp1=context[2], cp2=context[3])
        nltk_tuple = (features, label, sentence)
        # print(nltk_tuple)
        # print(nltk_tuple)
        nltk_data.append(nltk_tuple)

    return nltk_data