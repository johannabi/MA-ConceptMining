# ams skills zählen, wörter pro skill
# esco skills zählen, wörter pro skill
import inout.inputoutput as io


def expore_taxonomie(mode):
    if mode == 'esco':
        skills = io.read_esco_csv('../data/skills/esco_skills_de.csv', False, False)
    else:
        skills = io.read_ams_synsets('../data/skills/AMS_CategorizedCompetences.db', False, False)
    print(len(skills), ' skills in ', mode)
    print(len(set(skills)), 'types')

    token_freq = list()
    for s in skills:
        skill_len = len(s.split(' '))
        token_freq.append(skill_len)
        # if skill_len == 2:
        #     print(s)

    for c in set(token_freq):
        print(c, token_freq.count(c))

    avg = sum(token_freq) / len(token_freq)
    print('average:', avg)


expore_taxonomie('ams')
expore_taxonomie('esco')
