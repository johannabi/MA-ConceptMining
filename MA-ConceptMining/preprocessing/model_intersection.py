from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import numpy


# https://stackoverflow.com/questions/48941648/how-to-remove-a-word-completely-from-a-word2vec-model-in-gensim
def restrict_w2v(w2v, restricted_word_set):
    w2v.init_sims()

    new_vectors = []
    new_vocab = {}
    new_index2entity = []
    new_vectors_norm = []

    for i in range(len(w2v.vocab)):
        word = w2v.index2entity[i]
        vec = w2v.vectors[i]
        vocab = w2v.vocab[word]
        # vec_norm = w2v.vectors_norm[i]
        vec_norm = w2v.syn0[i]
        if word in restricted_word_set:
            vocab.index = len(new_index2entity)
            new_index2entity.append(word)
            new_vocab[word] = vocab
            new_vectors.append(vec)
            new_vectors_norm.append(vec_norm)

    w2v.vocab = new_vocab
    w2v.vectors = numpy.array(new_vectors)
    w2v.index2entity = new_index2entity
    w2v.index2word = new_index2entity
    w2v.vectors_norm = new_vectors_norm


def intersect_models(wiki_model, jobad_model):
    vocab_w = set(wiki_model.wv.vocab.keys())
    vocab_j = set(jobad_model.wv.vocab.keys())

    intersection = vocab_w.intersection(vocab_j)

    print(len(vocab_w), 'wiki')
    print(len(vocab_j), ' jobads')
    print(len(intersection), ' intersection')

    restrict_w2v(wiki_model, intersection)
    restrict_w2v(jobad_model, intersection)

    return wiki_model, jobad_model


def build_intersection():
    ## build intersection of model vocabs
    # read wikipedia news article model
    modelpath = "../data/exploration/german.model"
    w_wv_model = KeyedVectors.load_word2vec_format(modelpath, binary=True)
    # read jobad model
    modelpath = "../data/exploration/german_jobad.model"
    # j_model = Word2Vec.load(modelpath) # Word2Vec
    # j_wv_model = j_model.wv # Word2VecKeyedVectors
    j_wv_model = KeyedVectors.load_word2vec_format(modelpath, binary=True)

    w_wv_i_model, j_wv_model = intersect_models(w_wv_model, j_wv_model)

    w_wv_i_model.save_word2vec_format('../data/embeddings/german_inter2.model')
    j_wv_model.save_word2vec_format('../data/embeddings/jobad_inter2.model')


build_intersection()