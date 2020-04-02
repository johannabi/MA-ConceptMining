# read synsets from esco and search nearest neighbors in embedding
import inout.inputoutput as io
from gensim.models import KeyedVectors

ams = io.read_ams_synsets('../data/skills/AMS_CategorizedCompetences.db', True)

skills = io.read_esco_csv('../data/skills/esco_skills_de.csv', True, True)
j_path = "../data/embeddings/german_jobad.model"
j_model = KeyedVectors.load_word2vec_format(j_path, binary=True)

j_vocab = dict()

for v in j_model.vocab:
    if v.lower() in j_vocab:
        j_vocab[v.lower()].append(v)
    else:
        j_vocab[v.lower()] = [v]

ranks = set()

for synset in ams:
    # collect synsets that have vectors in word embedding
    in_model = list()
    for skill in synset:
        skill = skill.lower()
        if skill in j_vocab:
            in_model.append(skill)

    # if more than two lexems are in word embedding
    if len(in_model) > 1:
        # compute the rank between all pairs in the synset
        for l1 in in_model:
            for l2 in in_model:
                if l1 == l2:
                    continue
                # get all orthographic forms
                for o1 in j_vocab[l1]:
                    for o2 in j_vocab[l2]:
                        rank = j_model.rank(o1, o2)
                        ranks.add((o1, o2, rank))

for r in ranks:
    print(r)

print('dict size:', len(j_vocab))
print('vocab size:', len(j_model.vocab))




