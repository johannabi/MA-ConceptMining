import nltk.classify.decisiontree as dtree
import random
import spacy
from preprocessing import preprocessing as pp

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s')


def classify_categorial():
    # nlp = spacy.load('de_core_news_sm')

    # t[0] = feature_vector t[1] = label t[2] = sentence
    nltk_data = pp.build_matrix('../data/jobads/classified_sentences.db')
    random.shuffle(nltk_data)

    all_sentences = len(nltk_data)
    start = 0
    train_size = int(all_sentences * 0.2)
    end = train_size

    tp = 0
    fp = 0
    fn = 0
    tn = 0

    # 5-fold cross validation
    for i in range(5):

        nltk_test = nltk_data[start:end]
        nltk_train = nltk_data[:start] + nltk_data[end:]

        logging.info('all data: ' + str(len(nltk_data)))
        logging.info('Training data: ' + str(len(nltk_train)))
        logging.info('Test data: ' + str(len(nltk_test)))

        nltk_classifier = dtree.DecisionTreeClassifier
        # feature vector und label als trainingsdaten
        nltk_train = [(e[0], e[1]) for e in nltk_train]
        nltk_classifier = nltk_classifier.train(nltk_train)

        # jeder test vector wird klassifiziert
        for t in nltk_test:
            classified_label = nltk_classifier.classify(t[0])
            true_label = t[1]
            if classified_label == 1:
                if true_label == 1:
                    tp += 1
                else:
                    fp += 1
                    print(t[0], t[2], 'classified: ', classified_label, 'true: ', true_label)
            else:
                if true_label == 1:
                    fn += 1
                    print(t[0], t[2], 'classified: ', classified_label, 'true: ', true_label)
                else:
                    tn += 1

        start = end
        end = start + train_size
        if end > all_sentences:
            end = all_sentences

    print('TP:', tp, ' FP:', fp, ' FN:', fn, ' TN:', tn)

    prec = tp / (tp + fp)
    print('prec:', prec)

    rec = tp / (tp + fn)
    print('rec:', rec)


classify_categorial()