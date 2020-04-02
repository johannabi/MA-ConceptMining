import nltk.classify.decisiontree as dtree
import random
from preprocessing import preprocessing as pp

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s')


def classify_categorial(mode):
    """
    function to classify skills to be correct or incorrect extracted
    :param mode: 'dep' = depencency features (head), 'seq' = sequencial features (lemmatized neighbors)
    :return:
    """

    # t[0] = feature_vector t[1] = label t[2] = sentence
    nltk_data = pp.build_matrix(file='../data/jobads/classified_sentences.db', feature_mode=mode)
    random.shuffle(nltk_data)

    # compute training and test size
    all_sentences = len(nltk_data)
    start = 0
    train_size = int(all_sentences * 0.2)
    end = train_size

    tp = 0
    fp = 0
    fn = 0
    tn = 0

    # 5-fold cross validation
    logging.info('starting 5-fold crossvalidation for ' + mode + ' mode')
    for i in range(5):

        nltk_test = nltk_data[start:end]
        nltk_train = nltk_data[:start] + nltk_data[end:]

        # logging.info('all data: ' + str(len(nltk_data)))
        # logging.info('Training data: ' + str(len(nltk_train)))
        # logging.info('Test data: ' + str(len(nltk_test)))

        nltk_classifier = dtree.DecisionTreeClassifier
        # feature vector und label as training data
        nltk_train = [(e[0], e[1]) for e in nltk_train]

        nltk_classifier = nltk_classifier.train(nltk_train)

        # classify and evaluate each test data
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

    logging.info('TP: ' + str(tp) + ' FP: ' +  str(fp) + ' FN: '
                 + str(fn) + ' TN: ' + str(tn))

    prec = tp / (tp + fp)
    logging.info('prec: ' + str(prec))

    rec = tp / (tp + fn)
    logging.info('rec: ' +  str(rec))


# classify_categorial('seq')
# logging.info('********')
classify_categorial('dep')