from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from inout import inputoutput as io
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


def load_and_compare():
    # load intersected models as KeyedVectors
    w_path = "../data/embeddings/german_inter2.model"
    j_path = "../data/embeddings/jobad_inter2.model"

    w_model = KeyedVectors.load_word2vec_format(w_path)
    j_model = KeyedVectors.load_word2vec_format(j_path)

    # skills = io.read_wordlist('../data/skills/competences.txt', only_unigrams=True)
    # skills = io.read_esco_csv('../data/skills/skills_de.csv', only_unigrams=True, synsets=False)
    # skills = io.read_ams('../data/skills/CategorizedCompetences.db', level=3, only_unigrams=True).keys()

    m_vocab = w_model.vocab

    no_intersect = list() # 0%
    low_intersect = list() # 1-29%
    middle_intersect = list() # 30-69%
    high_intersect = list() # 70-100%

    topn = 5

    low = 0.3 * topn
    high = 0.7 * topn

    print('low intersection means equal neighbors <', low)
    print('high intersection means equal neighbors >=', high)

    for word in m_vocab:
        jobad_sim = j_model.wv.most_similar(word, topn=topn)
        j_set = set()
        for k, v in jobad_sim:
            j_set.add(k)

        wiki_sim = w_model.most_similar(word, topn=topn)
        w_set = set()
        for k, v in wiki_sim:
            w_set.add(k)

        # intersection
        intersection = w_set.intersection(j_set)
        inter_tuple = (word, j_set, w_set, intersection)

        if len(intersection) == 0:
            no_intersect.append(inter_tuple)
        elif len(intersection) < low:
            low_intersect.append(inter_tuple)
        elif len(intersection) >= high:
            high_intersect.append(inter_tuple)
        else:
            middle_intersect.append(inter_tuple)

    for h in no_intersect:
        print(h[0], '\n', h[1], '\n', h[2], '\n', h[3], '\n')

    for h in no_intersect:
        print(h[0])

    print('words with high intersection:', len(high_intersect))
    print('words with middle intersection:', len(middle_intersect))
    print('words with low intersection:', len(low_intersect))
    print('words without intersection:', len(no_intersect))

    print('\ntotal vectors:', len(w_model.vocab))


load_and_compare()





